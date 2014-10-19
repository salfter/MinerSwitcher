#!/usr/bin/env python
# coding=iso-8859-1

import sys
sys.path.insert(0, './ProfitLib/')
from ProfitLib import ProfitLib
sys.path.insert(0, './pycgminer/')
from pycgminer import CgminerAPI
import time
import json
import pprint

def SwitchPool(hostname, port, pool_url, pool_worker, pool_passwd):
  a=CgminerAPI(hostname, port)
  # add pool
  a.addpool(pool_url+","+pool_worker+","+pool_passwd)
  time.sleep(1)
  # wait for the connection
  live=0
  while (live==0):
    for i, pool in enumerate(a.pools()["POOLS"]):
      if (pool["URL"]==pool_url and pool["Status"]=="Alive"):
        live=1
    if (live==0):
      time.sleep(1)
  # switch to new pool and find 
  pools=a.pools()["POOLS"]
  delete_list=[]
  found=0
  for i, pool in enumerate(pools):
    if (pool["URL"]==pool_url and found==0):
      found=1
      a.switchpool(pool["POOL"])
    else:
      delete_list.append(pool["POOL"])
  # remove other pool entries
  delete_list.sort(reverse=True)
  for i, num in enumerate(delete_list):
    a.removepool(num)

# load config files

miners=json.loads(open("miner_config.json").read())
pools=json.loads(open("pool_config.json").read())
pl=ProfitLib(json.loads(open("profit_config.json").read()))

# main loop

while (0==0):
  print "running ProfitLib"
  #profit=pl.Calculate()
  print "sleep"
  time.sleep(1800)
  #SwitchPool("miner1", 4029, "stratum+tcp://stratum.wemineftc.com:4444", "salfter.miner1", "x")
