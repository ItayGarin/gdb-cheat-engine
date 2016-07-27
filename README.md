GDB Cheat Engine
------------------

Finds and uses cheats via the PythonGDB API

This is a utility class that uses PythonGDB's
memory I/O functionality to aid in finding variables
that can be used for cheats.

The I/O facilities are exposed through the PythonGDB's
Inferior class.
https://sourceware.org/gdb/onlinedocs/gdb/Inferiors-In-Python.html

Setup
-----

```python
$ gdb
  (gdb) source gdb_ce.py
  (gdb) python-interactive
  >>> ce = GdbCheatEngine(...)
```

Example
-------
The following procedure demonstrates how to find
the counter that holds a character's HP (health points).
One might leverage this variable to implement a god-mode cheat.

```python
>>> import gdb
>>> inferior = gdb.inferiors()[0]
>>> ram_addr, ram_size = (0x02000000, 1024 * 256)
>>> ce = GdbCheatEngine(inferior, ram_addr, ram_size)

>>> initial_hp = "\x00\x64" # 100 HP. Assumes that the counter is an unsigned 16bits variable
>>> ce.search_ram(initial_hp)
set([0x02000004, 0x0200..., ....])

# Reduce the HP...

>>> new_hp = "\x00\x60"
>>> ce.search_ram_again(new_hp)
set([0x02000004])

>>> hp_counter_addr = 0x02000004
```


More Docs
---------
For further documentaiton, check out this blogpost -
http://garin.io/TODO
