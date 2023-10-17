#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from os import path
import sys

# ==========================[ Information
DIR = path.dirname(path.abspath(__file__))
EXECUTABLE = "/{{executable}}"
TARGET = DIR + EXECUTABLE 
HOST, PORT = "{{target}}", {{port}}
REMOTE, LOCAL = {{remote}}, False

# ==========================[ Tools
elf = ELF(TARGET)
elfROP = ROP(elf)

# ==========================[ Configuration
context.update(
    arch=["i386", "amd64", "aarch64"][1],
    endian="little",
    os="linux",
    log_level = ['debug', 'info', 'warn'][2],
    terminal = ['tmux', 'split-window', '-h'],
)
#context.binary = elf
# ==========================[ Exploit

def exploit(io, libc=null):
    if LOCAL==True:
        #raw_input("Fire GDB!")
        if len(sys.argv) > 1 and sys.argv[1] == "d":
            choosen_gdb = [
                "source /home/mydata/tools/gdb/gdb-pwndbg/gdbinit.py",     # 0 - pwndbg
                "source /home/mydata/tools/gdb/gdb-peda/peda.py",          # 1 - peda
                #"source /home/mydata/tools/gdb/gdb-gef/.gdbinit-gef.py",    # 2 - gef
                "source /home/fl0wl3ss/Github/gef/gef.py"    # 2 - gef
                ][{{debugger}}]
            cmd = choosen_gdb + """
            
            """
            gdb.attach(io, gdbscript=cmd)
#--------------------------------------------
#------------------EXPLOIT-------------------
#--------------------------------------------

    payload = b""
    io.sendline(payload)
    io.interactive()

if __name__ == "__main__":
    io, libc = null, null

    if args.REMOTE:
        REMOTE = True
        io = remote(HOST, PORT)
        # libc = ELF("{{libc}}")
        
    else:
        LOCAL = True
        io = process(
            [TARGET, ],
            env={
            #     "LD_PRELOAD":"{{locallib}}",
            #     "LD_LIBRARY_PATH":"{{locallib}}",
            },
        )
        # libc = ELF("{{locallib}}")
    exploit(io, libc)
