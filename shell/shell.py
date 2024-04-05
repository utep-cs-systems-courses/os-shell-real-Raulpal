#! /usr/bin/env python3
import os, readline
from redirection import redirection
from pipe  import pipes
from command import run_command

# Prompt input from user
def promptCommand():
    prompt = os.getenv('PS1', '$ ')     # Get PS1 Environment variable 

    print(prompt, end='', flush=True)   # Print the prompt
    
    return input()                      # Return command

while True:                                                 # Run forever

    command = promptCommand().strip()                       # Get command

    if command == '':                                       # If nothing continue
        print()
        continue
    if command.lower() == 'exit':                           # If command is exit terminate
        exit(0)

    command = list(filter(None,command.split(' ')))         # Split and Filter Command

    if command[0].lower() == 'cd':                          # If command is change directories 'cd'
        if len(command) >= 2:                               # Check if at least length two
            if command[1] == '..':                          # Want to go back a directory
                os.chdir('..')                              # Change to parent directory
            else:
                try:
                    os.chdir(command[1])                    # Try to run desired cd directory name
                except FileNotFoundError:
                    os.write(2, f"bash: cd: {command[1]}: No such file or directory\n".encode())
        else:
            os.chdir(os.environ['HOME'])                    # If length one, go to HOME directory
        continue
    
    rc = os.fork()                                          # create a child process

    wait = True

    if command[-1] == '&':
        wait = False
        command.pop()
        
    if rc < 0:                                              # Fork failed
        exit(1)
    elif rc == 0:                                           # I am child
        if '|' in command:                                  # Check if pipe command
            pipes(command)                                  # Handle pipe command
        elif '>' in command or '<' in command:
            if not redirection(command):                    # Check if redirection command
                os.write(2, "Invalid redirection\n".encode())   # If redirection invalid
                continue
        run_command(command)                                # Execute command
            
    else:                                                   # I am parent (forked ok)
        if wait:
            childPidCode = os.wait()                            # Wait for child process to terminate  


    