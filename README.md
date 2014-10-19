MinerSwitcher
=============

This is a profitability-based mining farm pool switcher.  For the set of
coins you have configured, it will determine how many of each you can
produce given your hardware, and determine what they're worth in Bitcoin. 
It will then reconfigure all of your miners accordingly.  MinerSwitcher is
algorithm-agnostic: you can have a mix of sha256 miners, scrypt miners,
etc., and each will be switched to whatever is most profitable for it to
mine.

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

python-nmap
  http://xael.org/norman/python/python-nmap/

Also, you will need Cryptsy API credentials and a running *coind for each
coin you want to consider mining.  Whether you mine solo or with a pool is
up to you, but you'll need pool credentials (or *coind RPC credentials) in
the pool configuration.  Multiple pools may be configured for a coin for
redundancy.

Donations
=========

Donations are always welcome if you find this useful...hit the tipjar!

bitcoin://1TipsGocnz2N5qgAm9f7JLrsMqkb3oXe2
