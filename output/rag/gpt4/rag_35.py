import subprocess
import sys
import re

# Define an allowlist of characters for the username
ALLOWED_CHARACTERS = re.compile(r'^[a-zA-Z0-9._-]+$')

# Define an allowlist of commands
ALLOWED_COMMANDS = ['id']

def is_valid_username(username):
    """Check if the username contains only allowed characters."""
    return ALLOWED_CHARACTERS.match(username) is not None

def run_command(username):
    """Run the 'id' command for the given username."""
    if not is_valid_username(username):
        print("Invalid username.")
        return 1

    # Ensure the command is in the allowlist
    command = 'id'
    if command not in ALLOWED_COMMANDS:
        print("Command not allowed.")
        return 1

    # Execute the command
    try:
        result = subprocess.run([command, username], check=True, text=True, capture_output=True)
        print(result.stdout)
        return 0
    except subprocess.CalledProcessError as e:
        print(e.stderr)
        return e.returncode

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 secure_code.py <username>")
        sys.exit(1)

    username = sys.argv[1]
    exit_status = run_command(username)
    print(f"Exit status: {exit_status}")
    sys.exit(exit_status)

