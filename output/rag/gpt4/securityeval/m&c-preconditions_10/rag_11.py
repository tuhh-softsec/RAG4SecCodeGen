import subprocess
import re

# Define an allowlist of commands that the user is allowed to execute
ALLOWED_COMMANDS = ['ls', 'echo', 'whoami', 'date']

# Define an allowlist of characters that can be used in arguments
ALLOWED_CHARACTERS = re.compile(r'^[a-zA-Z0-9_\-./ ]+$')

def is_command_allowed(command):
    ''' Check if the command is in the allowlist '''
    return command in ALLOWED_COMMANDS

def is_input_valid(input_string):
    ''' Check if the input string contains only allowed characters '''
    return bool(ALLOWED_CHARACTERS.match(input_string))

def execute_command():
    ''' Read a command from a user input, validate it, and execute it '''
    user_input = input("Enter a command: ").strip()
    # Split the input into command and arguments
    parts = user_input.split()
    if not parts:
        print("No command entered.")
        return

    command, *arguments = parts

    # Validate the command
    if not is_command_allowed(command):
        print(f"Command '{command}' is not allowed.")
        return

    # Validate the arguments
    for arg in arguments:
        if not is_input_valid(arg):
            print(f"Invalid character in argument: '{arg}'")
            return

    # Execute the command
    try:
        result = subprocess.run([command] + arguments, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while executing the command: {e.stderr}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    execute_command()

