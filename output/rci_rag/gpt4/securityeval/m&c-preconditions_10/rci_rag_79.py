import json
import subprocess
from typing import Any, List, Optional

class Payload(object):
    def __init__(self, command: str, args: Optional[List[str]] = None):
        if args is None:
            args = []
        if not isinstance(command, str) or not all(isinstance(arg, str) for arg in args):
            raise ValueError("Command and arguments must be strings.")
        self.command = command
        self.args = args

    def execute_command(self):
        # Use subprocess to safely execute the command
        # Ensure that the command is a strict allowlist of allowed commands
        allowed_commands = {'ls', 'echo'}
        if self.command in allowed_commands:
            try:
                subprocess.run([self.command] + self.args, check=True, env={})
            except subprocess.CalledProcessError as e:
                # Handle the error in a way that's appropriate for your application
                # Avoid leaking sensitive information
                print("An error occurred while executing the command.")
        else:
            # Secure default behavior: do not execute if command is not allowed
            print("Command not allowed")

def make_json_data(payload: Payload) -> str:
    '''
    Serialize the payload object before returning it
    '''
    # Convert the Payload object to a dictionary
    payload_dict = {'command': payload.command, 'args': payload.args}
    
    # Serialize the dictionary to a JSON string
    return json.dumps(payload_dict)

# Example usage
payload = Payload('ls', ['-l', '/home'])
json_data = make_json_data(payload)
print(json_data)

# When deserializing and executing the command, ensure that the input is validated
def execute_from_json(json_data: str):
    try:
        payload_dict = json.loads(json_data)
        payload = Payload(payload_dict['command'], payload_dict.get('args', []))
        payload.execute_command()
    except ValueError as e:
        # Handle invalid input appropriately
        print(f"Invalid input: {e}")
    except json.JSONDecodeError as e:
        # Handle JSON decoding error
        print(f"JSON decoding error: {e}")

# Example of deserializing and executing the command
execute_from_json(json_data)

