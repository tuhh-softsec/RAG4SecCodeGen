import os
import signal

def is_valid_process_id(process_id):
    """
    Check if the process ID is an integer and within the valid range for PIDs.
    """
    try:
        pid = int(process_id)
        # On Unix systems, PID 0 is reserved for the scheduler and PID 1 for the init process.
        # PIDs must be positive integers.
        return pid > 1
    except ValueError:
        return False

def kill_process(process_id):
    """
    Kill the process with the given process_id in a secure manner.
    """
    if not is_valid_process_id(process_id):
        raise ValueError("Invalid process ID provided.")

    try:
        # Send SIGTERM signal to the process
        os.kill(process_id, signal.SIGTERM)
    except OSError as e:
        # Handle specific error cases here, such as permission issues or process not found
        print(f"Error killing process {process_id}: {e}")
        raise

# Example usage:
# kill_process(1234)  # Replace 1234 with the actual process ID you want to kill

