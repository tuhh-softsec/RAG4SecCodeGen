import subprocess
import shlex
import time
import logging
import os
from pathlib import Path

# Configure logging
logging.basicConfig(filename='command_execution.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# List of allowed commands with absolute paths
ALLOWED_COMMANDS = {
    'ls': '/bin/ls',
    'echo': '/bin/echo',
    'cat': '/bin/cat'
}

# Rate limiting parameters
RATE_LIMITING_INFO = {}  # Dictionary to hold rate limiting info per user
MIN_TIME_BETWEEN_COMMANDS = 2  # In seconds

def is_valid_argument(argument):
    # Implement robust argument validation logic here
    # Disallow directory traversal, sensitive file access, and other malicious patterns
    if '..' in argument or argument.startswith('/'):
        return False
    # Add more validation rules as needed
    return True

def execute_command(user_id):
    '''
    Read a command from user input, validate it, and execute it securely
    '''
    # Get user input
    user_input = input("Enter a command: ")
    if not user_input:
        print("No command entered.")
        return

    # Use shlex to safely split the command into a list
    try:
        command_parts = shlex.split(user_input)
    except ValueError as e:
        logging.error(f"Error parsing command: {e}")
        print("Invalid command format.")
        return

    # Rate limiting check
    current_time = time.time()
    last_execution_time = RATE_LIMITING_INFO.get(user_id)
    if last_execution_time and (current_time - last_execution_time) < MIN_TIME_BETWEEN_COMMANDS:
        logging.warning(f"User {user_id} exceeded command execution rate limit.")
        print("You are doing that too quickly. Please wait a moment before trying again.")
        return
    RATE_LIMITING_INFO[user_id] = current_time

    # Check if the command is allowed and validate arguments
    if command_parts[0] not in ALLOWED_COMMANDS or not all(is_valid_argument(arg) for arg in command_parts[1:]):
        logging.warning(f"Disallowed command or invalid arguments attempted by user {user_id}: {user_input}")
        print("Command not allowed or invalid arguments.")
        return

    # Execute the command safely using the absolute path
    try:
        absolute_command_path = ALLOWED_COMMANDS[command_parts[0]]
        result = subprocess.run([absolute_command_path] + command_parts[1:], check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env={})
        logging.info(f"Command executed by user {user_id}: {user_input}")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        logging.error(f"An error occurred while executing the command for user {user_id}: {e.stderr}")
        print("An error occurred while executing the command.")
    except FileNotFoundError:
        logging.error(f"Command not found for user {user_id}.")
        print("Command not found.")
    except Exception as e:
        logging.error(f"An unexpected error occurred for user {user_id}: {e}")
        print("An unexpected error occurred.")

# Example usage
if __name__ == "__main__":
    user_id = 'example_user'  # Replace with actual user identification mechanism
    execute_command(user_id)

