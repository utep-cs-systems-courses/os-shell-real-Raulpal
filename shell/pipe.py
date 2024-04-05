#! /usr/bin/env python3
import os
from command import run_command

#  Handle Pipe commands  ... | ...
def pipes(command):
    
    index = command.index('|')      # Get pipe character index
    leftSide = command[0:index]     # Get left side command of pipe index
    rightSide = command[index+1:]   # Get Right side command of pip index

    pipeReader,pipeWriter = os.pipe() # Using pipe() function we get back 2 FD one for reading from pipe and the other writing to the pipe

    rc = os.fork()                  # Fork child process

    if rc < 0:                      # Error occurred
        exit(1)
    elif rc ==0:                    # I am the child
        os.close(1)                 # Close standard output FD
        os.dup(pipeWriter)          # Duplicate pipWriter FD onto file descriptor 1. Redirects stdout to write to pipe.
        os.set_inheritable(1,True)  # Want stdout to be inheritable by child process

        for fd in (pipeWriter, pipeReader): # Close pipe file descriptors in child process, not needed
            os.close(fd)
        run_command(leftSide)       # Execute command, sending its output to the pipe.
    else:                           # I am parent
        os.close(0)                 # Close stdin FD
        os.dup(pipeReader)          # Duplicate FD pipeReader, Redirects stdin to read from pipe
        os.set_inheritable(0,True)  # Want stdin to be inheritable by child process
        
        for fd in (pipeWriter, pipeReader): # Close pipe FD in Parent process, not needed
            os.close(fd)
        run_command(rightSide)      # Execute command, using the piped data from the pipe as its input
