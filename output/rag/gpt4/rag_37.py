import subprocess
import shlex

# Define an allowlist of characters that are allowed in the arguments
ALLOWLIST_CHARS = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_. /')

# Define an allowlist of commands that are allowed to be executed
ALLOWED_COMMANDS = ['ls']

def is_input_safe(input_string):
    """Check if the input string contains only allowlisted characters."""
    return all(c in ALLOWLIST_CHARS for c in input_string)

def execute_command(command, *args):
    """Execute a command with arguments if it's on the allowlist and the arguments are safe."""
    # Ensure the command is in the allowlist
    if command not in ALLOWED_COMMANDS:
        raise ValueError("Command not allowed")

    # Ensure all arguments are safe
    safe_args = []
    for arg in args:
        if not is_input_safe(arg):
            raise ValueError("Invalid character in argument")
        safe_args.append(arg)

    # Use shlex to quote the arguments safely
    quoted_args = [shlex.quote(arg) for arg in safe_args]

    # Construct the command with the quoted arguments
    full_command = [command] + quoted_args

    # Execute the command safely
    result = subprocess.run(full_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Check for errors
    if result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, full_command, output=result.stdout, stderr=result.stderr)

    return result.stdout

def print_and_execute(format_string, *args):
    """Prints a formatted string and executes the command."""
    # Construct the string with the format and arguments
    command_string = format_string % args

    # Split the command string into command and arguments
    command_parts = command_string.split()

    # Execute the command with the arguments
    output = execute_command(*command_parts)
    print(output)

# Example usage
try:
    # This should work
    print_and_execute("ls %s", "-la")
    
    # This should raise an error due to an unsafe character
    print_and_execute("ls %s", "; rm -rf /")
except ValueError as e:
    print(f"Error: {e}")
except subprocess.CalledProcessError as e:
    print(f"Command execution failed: {e}")

