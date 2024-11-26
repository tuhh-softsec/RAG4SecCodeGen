import subprocess
import re

# Define an allowlist of safe characters for the directory argument
ALLOWLIST_PATTERN = re.compile(r'^[a-zA-Z0-9_\-./]*$')

# Define an allowlist of allowed commands
ALLOWED_COMMANDS = ['ls']

def execute_command(command, directory):
    # Ensure the command is in the allowlist
    if command not in ALLOWED_COMMANDS:
        raise ValueError("Command not allowed")

    # Validate the directory against the allowlist pattern
    if not ALLOWLIST_PATTERN.match(directory):
        raise ValueError("Invalid characters in directory argument")

    # Safely construct the command with proper quoting
    safe_command = [command, directory]

    # Execute the command safely
    try:
        result = subprocess.run(safe_command, check=True, text=True, capture_output=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while executing the command: {e}")

# Example usage:
# This should print the contents of the current directory
execute_command('ls', '.')

# This should raise an error due to invalid characters
# execute_command('ls', '; rm -rf /')

# This should raise an error due to an unauthorized command
# execute_command('rm', '.')

