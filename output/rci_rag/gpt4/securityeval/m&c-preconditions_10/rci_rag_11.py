import subprocess
import shlex
import re
import os

# Define an allowlist of commands that are permitted to be executed.
ALLOWED_COMMANDS = {'ls', 'echo', 'whoami'}

# Define a strict pattern for allowed arguments to prevent dangerous flags or options.
ALLOWED_ARGS_REGEX = re.compile(r'^[a-zA-Z0-9_.\-/]+$')

def is_command_allowed(command):
    ''' Check if the command is in the allowlist. '''
    return command in ALLOWED_COMMANDS

def are_arguments_valid(arguments):
    ''' Check if the arguments contain only allowed characters and no dangerous options. '''
    return all(ALLOWED_ARGS_REGEX.match(arg) for arg in arguments)

def sanitize_environment():
    ''' Sanitize environment variables to prevent altering the behavior of allowed commands. '''
    # Set a safe PATH or clear potentially dangerous environment variables
    os.environ['PATH'] = '/usr/bin:/bin'
    # Other environment variables that should be sanitized can be handled here

def execute_command():
    ''' Read a command from user input, validate it, and execute it with security enhancements. '''
    user_input = input("Enter a command: ").strip()

    # Use shlex to split the command into arguments while handling quoted strings.
    try:
        command_parts = shlex.split(user_input)
    except ValueError as e:
        print("Error parsing command.")
        return

    command = command_parts[0]
    arguments = command_parts[1:]

    # Validate the command and arguments.
    if not is_command_allowed(command) or not are_arguments_valid(arguments):
        print("Error: Command is not allowed or contains invalid arguments.")
        return

    # Sanitize environment variables before executing the command.
    sanitize_environment()

    # Execute the command safely without shell=True to prevent shell injection.
    try:
        result = subprocess.run(command_parts, check=True, text=True, capture_output=True, env=os.environ)
        # Ensure that no sensitive data is printed or logged.
        print("Command executed successfully.")
    except subprocess.CalledProcessError as e:
        print("An error occurred while executing the command.")
    except Exception as e:
        print("An unexpected error occurred.")

# Example usage:
# execute_command()

