MinerSwitcher
=============

TODO: content

Setup
-----

This project has nested submodules, and one submodule needs a path fix so
it'll be included properly.  Use the following to fix everything up:

```
git submodule update --init --recursive
patch -p0 <ProfitLib-path-fix.patch
```

The ProfitLib configuration needs to be copied from
./ProfitLib/profit_config_example.json to ./profit_config.json and edited
appropriately.  In addition to Cryptsy API credentials, you will need RPC
access to coin daemons for the coins you want to switch between.

The pool configuration needs to be copied from ./pool_config_example.json to
./pool_config.json and edited with the credentials for the pools you use.

The miner configuration needs to be copied from ./miner_config_example.json
to ./miner_config.json and edited with the connection details for your
cgminer and/or bfgminer instances.  Read/write access needs to be enabled
for each instance.

Dependencies
------------

ProfitLib (included as a submodule):
  https://github.com/salfter/ProfitLib

pycgminer (included as a submodule):
  https://github.com/tsileo/pycgminer

PyCryptsy (included as a submodule of ProfitLib):
  https://github.com/salfter/PyCryptsy    
