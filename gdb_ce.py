#!/usr/bin/python

class GdbCheatEngine(object):
    """
    Finds and uses cheats via the PythonGDB API

    This is a utility class that uses PythonGDB's
    memory I/O functionality to aid in finding variables
    that can be used for cheats.

    The I/O facilities are exposed through the PythonGDB's
    Inferior class.
    https://sourceware.org/gdb/onlinedocs/gdb/Inferiors-In-Python.html

    Setup
    -----

    ```
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

    ```
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
    """

    def __init__(self, inferior, ram_addr, ram_size):
        self.inferior = inferior
        self.ram_addr = ram_addr
        self.ram_size = ram_size


    def __search_ram_iter(self, pattern):
        """
        Yields all the RAM addresses where the pattern is found by
        continuously calling gdb.Inferior.search_memory()
        """
        end_address = self.ram_addr + self.ram_size
        result_addr = self.ram_addr
        while True:
            remaining_length = end_address - result_addr
            result_addr = self.inferior.search_memory(result_addr + len(pattern), remaining_length, pattern)
            if result_addr is None:
                return
            else:
                yield result_addr


    def __search_ram(self, pattern):
        """Returns a set with all of the RAM addresses that contain the pattern"""
        return set([addr for addr in self.__search_ram_iter(pattern)])


    def search_ram(self, pattern):
        """
        Returns a set with all of the RAM addresses that contain the pattern (stateful).
        It is possible to further filter the matches with consecutive calls to search_ram_again.
        """
        self.last_results = self.__search_ram(pattern)
        return self.last_results


    def search_ram_again(self, pattern):
        """
        Returns all the RAM addresses that match the new pattern and old ones (stateful filter).
        It is possible to further filter the matches with consecutive calls to this method.
        """
        new_results = self.__search_ram(pattern)
        self.last_results = self.last_results.intersection(new_results)
        return self.last_results

    def write_memory(self, address, buff):
        self.inferior.write_memory(address, buff)

    def read_memory(self, address, length):
        self.inferior.read_memory(address, length)
