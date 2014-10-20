#!/usr/bin/env python
# coding=iso-8859-1

# SwitchCoin.py: manually switch miners to a coin
#
# Copyright © 2014 Scott Alfter
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import sys
sys.path.insert(0, './pycgminer/')
from pycgminer import CgminerAPI
import json
import operator

# reconfigure a cgminer/bfgminer instance to mine on another pool
# (by default, remove all other pools)

def SwitchPool(hostname, port, pool_url, pool_worker, pool_passwd, clear=1):
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

  # switch to new pool and find it 

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

  if (clear==1):
    delete_list.sort(reverse=True)
    for i, num in enumerate(delete_list):
      a.removepool(num)

# switch all miners of a given type to a different coin

def SwitchCoin(coin, algo, miners, pools):

  # enumerate compatible miners

  for i, miner in enumerate(miners):
    if (miners[miner]["algo"]==algo):
      hostname=miners[miner]["hostname"]
      rpc_port=miners[miner]["rpc_port"]

      # enumerate available pools
      
      pool_priorities={}
      for j, pool in enumerate(pools):
        if (pools[pool]["coin"]==coin):
          pool_priorities[pool]=pools[pool]["priority"]
      sorted_priorities=sorted(pool_priorities.items(), key=operator.itemgetter(1))
      for k, pool in enumerate(sorted_priorities):
        
        # switch a miner to the pool
        
        pool_url=pools[pool[0]]["protocol"]+"://"+pools[pool[0]]["hostname"]+":"+str(pools[pool[0]]["port"])
        pool_worker=pools[pool[0]]["worker_prefix"]+pools[pool[0]]["worker_separator"]+miner
        pool_worker_pass=pools[pool[0]]["worker_password"]
        if (k==0):
          clear=1
        else:
          clear=0

        print "switching "+miner+" to "+pool[0]

        try:
          SwitchPool(miner, rpc_port, pool_url, pool_worker, pool_worker_pass, clear)
        except:
          print "unable to switch "+miner+" to "+coin+"...miner down?"

# C-style main() gets rid of global scope

def main(argc, argv):

  if (argc!=2):
    print "Usage: "+argv[0]+" COIN"
    sys.exit(1)

  # load config files

  miners=json.loads(open("miner_config.json").read())
  pools=json.loads(open("pool_config.json").read())
  coins=json.loads(open("profit_config.json").read())

  SwitchCoin(argv[1], coins[argv[1]]["algo"], miners, pools)

main(len(sys.argv), sys.argv)
