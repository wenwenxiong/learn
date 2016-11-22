#!/usr/bin/env python

file_abs="/proc/meminfo"
namespace="qvm"
region="gz"
secretId="AKIDUBnDA0ijMBsOhpAV2Vpz2yiHpIaAkop2"
secretKey="DE2ds1176yeBZlmdVxSioiU4TggVQHwQ"
metricName="mem_usage"

# get local(lan) ip
import socket
import fcntl
import struct
 
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

myaddr=get_ip_address("eth0")
print myaddr

# compute mem_usage
with open(file_abs, "r") as f:
    poet_list = f.readlines()

for i in poet_list:
    if (i.startswith("MemTotal")):
        print i
        print i.split()[1]
        totol_mem=i.split()[1]
    if (i.startswith("MemFree")):
        print i
        print i.split()[1]
        free_mem=i.split()[1]

mem_usage=float(free_mem)/float(totol_mem)
print mem_usage
# build url arg
import datetime
import time
currentTime=time.mktime(datetime.datetime.now().timetuple())
print currentTime
urlBase="http://receiver.monitor.tencentyun.com:8080/report.cgi?"
requestHost="receiver.monitor.tencentyun.com"
requestUri="/report.cgi"

import random
import sys
import os

params={}
params['Data'] = [{'dimensions':{'lanip':myaddr},'value':mem_usage,'metricName':metricName}]
print params
params['Nonce'] = random.randint(1, sys.maxint)
params['Timestamp'] = currentTime
params['Region'] = region
params['Namespace'] = namespace
params['SecretId'] = secretId
print params

sys.path.append(os.path.split(os.path.realpath(__file__))[0] + os.sep)
print sys.path
from common.request import Request

request = Request(secretId, secretKey)
url = request.generateUrl(requestHost, requestUri , params)
print 'end url: ' + url

import urllib2
req = urllib2.Request(url)
print req

res_data = urllib2.urlopen(req)
res = res_data.read()
print res
