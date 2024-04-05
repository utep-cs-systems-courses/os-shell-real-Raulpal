#! /usr/bin/env python3
import os,re

# Run the commands passed
def run_command(command):
    try:
        os.execve(command[0], command, os.environ)  # Try to execute command, replace current VM memory with specified command
    except FileNotFoundError:
        pass
    
    for dir in re.split(":", os.environ['PATH']):   # try each directory in the path
        program = "%s/%s" % (dir, command[0])       # Construct full path to program
        try:
            os.execve(program, command, os.environ) # try to exec program
        except FileNotFoundError:             
            pass                              
    os.write(2, ("%s: Command not found\n" % command[0]).encode())
    exit(1)     