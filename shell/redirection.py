#! /usr/bin/env python3
import os

# Handle redirection command   ... > ... or  ... < ...
def redirection(command):

    if '>' in command:              # Goes into operator
        index = command.index('>')  # Get index of '>'
        command.pop(index)          # Remove it

        os.close(1)                 # disconnect FD stdout 
        os.open(command.pop(index), os.O_CREAT | os.O_WRONLY)   # Open/create file specified fro writing
        os.set_inheritable(1,True)  # Set FD stdout to be inheritable by child process
        return True                 # If everything good, return true
        
    if '<' in command:              # Comes out of operator
        index = command.index('<')  # Get index of '<'
        command.pop(index)          # Remove it

        os.close(0)                 # Close FD stdin
        os.open(command.pop(index), os.O_RDONLY)    # Open specified file for reading
        os.set_inheritable(0,True)  # Set FD stdin to be inheritable by child process
        return True                 # If everything good, return true
    return False                    # If got '>' or '<' error return false