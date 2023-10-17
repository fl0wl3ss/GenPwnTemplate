#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import subprocess
from jinja2 import Template
import os
def generate_exploit(executable, target, port, debugger, remote, libc, locallib):
    script_dir = os.path.dirname(os.path.abspath(__file__))

    template_path = os.path.join(script_dir, "tmp.py")

    with open(template_path, "r") as template_file:
        template_content = template_file.read()
        template = Template(template_content)

    # debugger
    if debugger == "pwndbg":
        debugger = 0
    elif debugger == "peda":
        debugger = 1
    elif debugger == "gef": 
        debugger = 2
    else :
        debugger = 0

    exploit_text = template.render(executable=executable , target=target, port=port, remote=remote, debugger=debugger, libc=libc, locallib=locallib)

    return exploit_text

def get_library_paths(executable_path):
    try:
        ldd_output = subprocess.check_output(["ldd", executable_path], text=True, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        return 

    library_paths = []
    for line in ldd_output.splitlines():
        if "=>" in line and "not found" not in line:
            parts = line.split()
            if len(parts) > 2:
                library_path = parts[2]
                if library_path.startswith("/"):
                    library_paths.append(library_path)

    return library_paths



def save_exploit_to_file(exploit_text, output):
    with open(output, "w") as exploit_file:
        exploit_file.write(exploit_text)

def main():
    parser = argparse.ArgumentParser(description="Exploit Template Generator")
    parser.add_argument("-t", "--target", default="127.0.0.1", help="Target IP address")
    parser.add_argument("-p", "--port", default=4444, type=int, help="Target port")
    parser.add_argument("-d", "--debugger", default="gef", help="Select debugger (vanilla,peda,gef)")
    parser.add_argument("-b", "--bin",dest="executable", required=True, help="Executable to Exploit")
    parser.add_argument("-r", "--remote", action="store_true", help="Set remote mode (True/False)")
    parser.add_argument("-l", "--libc", default="", help="Linked libc" )
    parser.add_argument("-o", "--output", default='exploit.py', help="Output")

    args = parser.parse_args()

    executable_path = "args.executable"
    library_paths = get_library_paths(args.executable)
    locallib = "___"
    if library_paths:
        for path in library_paths:
            locallib=path

    exploit_text = generate_exploit(args.executable, args.target, args.port, args.debugger, args.remote, args.libc,locallib)

    #print(exploit_text)
    save_exploit_to_file(exploit_text, args.output)

if __name__ == "__main__":
    main()

