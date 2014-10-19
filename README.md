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

Dependencies
------------

ProfitLib (included as a submodule):
  https://github.com/salfter/ProfitLib

pycgminer (included as a submodule):
  https://github.com/tsileo/pycgminer

PyCryptsy (included as a submodule of ProfitLib):
  https://github.com/salfter/PyCryptsy    
