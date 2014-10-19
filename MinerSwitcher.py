#!/usr/bin/env python
# coding=iso-8859-1

# MinerSwitcher.py: profitability-based mining farm switcher
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
sys.path.insert(0, './ProfitLib/')
from ProfitLib import ProfitLib
sys.path.insert(0, './pycgminer/')
from pycgminer import CgminerAPI
import time
import json
from decimal import *
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
        
        pool_url=pools[pool[0]]["url"]
        pool_worker=pools[pool[0]]["worker_prefix"]+pools[pool[0]]["worker_separator"]+miner
        pool_worker_pass=pools[pool[0]]["worker_password"]
        if (k==0):
          clear=1
        else:
          clear=0

        print now()+": switching "+miner+" to "+pool[0]

        SwitchPool(miner, rpc_port, pool_url, pool_worker, pool_worker_pass, clear)

# get current date & time
def now():
  return time.strftime("%c")

# dump ProfitLib results as a table
# (cribbed from ProfitLib/profit.py)

def MakeTable(algo):
  result={}

  for i, coin in enumerate(profit):
    if (profit[coin]["algo"]==algo and profit[coin]["merged"]==[]):
      result[coin]=Decimal(profit[coin]["daily_revenue_btc"])/100000000
      for j, mergecoin in enumerate(profit):
        if (profit[mergecoin]["algo"]==algo and profit[mergecoin]["merged"]!=[]):
          for k, basecoin in enumerate(profit[mergecoin]["merged"]):
            if (basecoin==coin):
              result[coin]+=Decimal(profit[mergecoin]["daily_revenue_btc"])/100000000

  sorted_result=sorted(result.items(), key=operator.itemgetter(1), reverse=True)

  for i, r in enumerate(sorted_result):
    print r[0]+" "+str(r[1])

# load config files

miners=json.loads(open("miner_config.json").read())
pools=json.loads(open("pool_config.json").read())
pl=ProfitLib(json.loads(open("profit_config.json").read()))

# main loop

last_coin={}
while (0==0):
  print now()+": running ProfitLib"
  profit=pl.Calculate()

  # find algo types

  algos={}
  for i, coin in enumerate(profit):
    algos[profit[coin]["algo"]]=profit[coin]["algo"]
    try:
      z=last_coin[profit[coin]["algo"]] # see if it exists
    except:
      last_coin[profit[coin]["algo"]]="" # create it if it doesn't

  # loop on available algos
    
  for i, algo in enumerate(algos):
  
    # find most profitable coin
    
    max=0
    coin_max=""
    for j, coin in enumerate(profit):
      if (profit[coin]["algo"]==algo and profit[coin]["daily_revenue_btc"]>max):
        max=profit[coin]["daily_revenue_btc"]
        coin_max=coin

    # print profitability table

    MakeTable(algo)
    
    # do we need to switch?
    
    if (last_coin[algo]!=coin_max):
      SwitchCoin(coin_max, algo, miners, pools)
      
    last_coin[algo]=coin_max
    
  # wait 30 minutes

  print now()+": sleep for 30 minutes"
  time.sleep(1800)
