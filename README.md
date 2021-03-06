MinerSwitcher
=============

This is a profitability-based mining farm pool switcher.  For the set of
coins you have configured, it will determine how many of each you can
produce given your hardware, and determine what they're worth in Bitcoin. 
It will then reconfigure all of your miners accordingly.  MinerSwitcher is
algorithm-agnostic: you can have a mix of sha256 miners, scrypt miners,
etc., and each will be switched to whatever is most profitable for it to
mine.

Sometimes pools go down without much notice.  Before switching coins,
MinerSwitcher verifies that at least one of your configured pools is still
up.  If it isn't, it prints a warning and moves on to the next most
profitable pool.

MinerSwitcher can be configured to send Pushover notifications if a miner is
down or the pools for a coin aren't responding.

Setup
-----

The configuration files need to be copied from
./*_config_example.json to ./*_config.json and edited 
appropriately.  In addition to exchange API credentials, you will 
need RPC access to coin daemons for the coins you want to switch 
between.  Setting hashrates in daemon_config.json is unnecessary; 
hashrates will be populated with values calculated from the miner
configuration (below).  If you don't want to check a particular exchange,
remove its section from exchange_config.json.

For multiple-algorithm coins, you can create multiple entries in
daemon_config.json to evaluate suitability for whatever types of mining
hardware you use.  Here's an example, using Digitalcoin for both SHA256 and
scrypt...note the label with the algo after an underline:

```
  "DGC_sha256" : {
    "username" : "salfter",
    "passwd" : "rpc_password_goes_here",
    "host" : "localhost",
    "port" : 7998,
    "active" : 1,
    "hashespersec" : 580000000000,
    "algo" : "sha256",
    "merged" : [],
    "daemonuser" : "digitalcoin",
    "daemon" : "digitalcoind",
    "client" : "digitalcoind"
  },
  "DGC_scrypt" : {
    "username" : "salfter",
    "passwd" : "rpc_password_goes_here",
    "host" : "localhost",
    "port" : 7998,
    "active" : 1,
    "hashespersec" : 8000000,
    "algo" : "scrypt",
    "merged" : [],
    "daemonuser" : "digitalcoin",
    "daemon" : "digitalcoind",
    "client" : "digitalcoind"
  }
```

The pool configuration needs to be copied from ./pool_config_example.json to
./pool_config.json and edited with the credentials for the pools you use.
The priority field determines the order in which pools are fed to the miner;
the pool with the highest priority is added last, so the miner switches to
it.  In the example configuration, for instance, Eligius is given a priority
of 10 and BTC Guild is given a priority of 0.  MinerSwitch will remove
whatever other pools are configured, send the configuration for BTC Guild,
and then send the configuration for Eligius.  When it's all done, the miner
will be aiming its shares at Eligius (unless it's down).

The miner configuration needs to be copied from ./miner_config_example.json
to ./miner_config.json and edited with the connection details for your
cgminer and/or bfgminer instances.  Read/write access needs to be enabled
for each instance.  Average hashrate for each miner should be set for best
results.  url_suffix is appended to the URL sent to the miner; it's intended
to pass extra options to the miner (such as to disable the "coinbase check"
in recent versions of bfgminer that causes problems with some pools).

To enable Pushover notifications, copy ./pushover_config_example.json to
./pushover_config.json and fill it in with your credentials.  Your user key
is on their homepage when you're logged in; copy it to the user_key field. 
You'll need to create an application API key; go to
https://pushover.net/apps/build, fill in the blanks.  If you want, you may
use the included icon file (mining-icon-red.png) with your configuration. 
Click "Create Application." Copy the application key Pushover gives you to
the app_key field.

If you don't want to use Pushover, no configuration is needed.

Usage
-----

I recommend running MinerSwitcher inside a screen session:

http://www.gnu.org/software/screen

Invocation is simple:

```
screen -dmS MinerSwitcher ./MinerSwitcher.py
```

To see what it's doing, use this:

```
screen -dr MinerSwitcher
```

To put MinerSwitcher back in the background, press Ctrl-A Ctrl-D.

Dependencies
------------

ProfitLib:
  https://github.com/salfter/ProfitLib

pycgminer:
  https://github.com/tsileo/pycgminer

python-nmap
  http://xael.org/norman/python/python-nmap/

python-pushover
  http://pythonhosted.org/python-pushover

python-bitcoinrpc
  https://github.com/jgarzik/python-bitcoinrpc

jsonrpc
  http://json-rpc.org/wiki/python-json-rpc

pycurl
  https://github.com/pycurl/pycurl

tabulate
  https://pypi.python.org/pypi/tabulate

Also, you will need exchange API credentials and a running *coind for each
coin you want to consider mining.  Whether you mine solo or with a pool is
up to you, but you'll need pool credentials (or *coind RPC credentials) in
the pool configuration.  Multiple pools may be configured for a coin for
redundancy.

A Pushover account is optional.  With it, MinerSwitcher can notify you of
problems with your setup.

Donations
=========

Donations are always welcome if you find this useful...hit the tipjar!

bitcoin://1TipsGocnz2N5qgAm9f7JLrsMqkb3oXe2
