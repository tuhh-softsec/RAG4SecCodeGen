import json
from typing import Any, Dict

class SafePayload(object):
    def __init__(self, data: Dict[str, Any]):
        # Perform initial data validation and sanitization
        if not isinstance(data, dict):
            raise ValueError("Data must be a dictionary")
        # Additional validation logic to ensure data conforms to expected format
        self.data = data

    def to_json(self) -> str:
        # Convert the data to JSON format, ensuring it is safe to serialize
        return json.dumps(self.data)

    @staticmethod
    def from_json(json_data: str) -> 'SafePayload':
        try:
            # Attempt to parse the JSON data
            data = json.loads(json_data)
            # Perform data validation and sanitization after parsing
            # This could include checking data types, patterns, and value ranges
            if not isinstance(data, dict):
                raise ValueError("Deserialized data is not a dictionary")
            # Additional validation logic here
            return SafePayload(data)
        except json.JSONDecodeError as e:
            # Handle JSON decoding error (e.g., logging, raising an exception)
            raise ValueError("Invalid JSON data") from e

# Example usage:
try:
    safe_payload = SafePayload({"key": "value"})
    json_data = safe_payload.to_json()
    print(json_data)  # Output: {"key": "value"}

    # To deserialize:
    deserialized_payload = SafePayload.from_json(json_data)
    print(deserialized_payload.data)  # Output: {'key': 'value'}
except ValueError as e:
    # Handle the error appropriately
    print(e)

