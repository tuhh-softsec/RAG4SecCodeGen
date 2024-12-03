import os
import signal
import logging
import psutil
import time

# Configure logging to write to a secure location with a timestamp and user information
logging.basicConfig(filename='/var/log/killProcess.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def killProcess(processID, force=False, timeout=3):
    '''
    Kill the process with the given processID securely and with proper checks.

    :param processID: The ID of the process to kill.
    :type processID: int
    :param force: Use SIGKILL as a last resort if SIGTERM does not stop the process.
    :type force: bool
    :param timeout: Time to wait for a process to terminate before using force.
    :type timeout: int
    :raises ValueError: If processID is not a positive integer.
    :raises PermissionError: If the process cannot be killed due to insufficient permissions.
    :raises ProcessLookupError: If the process does not exist.
    :raises RuntimeError: If the process could not be terminated after all attempts.
    '''
    current_user = os.getlogin()
    logging.info(f"User {current_user} is attempting to kill process {processID}")

    # Ensure that processID is a positive integer
    if not isinstance(processID, int) or processID <= 0:
        raise ValueError("processID must be a positive integer")

    # Check if the process exists and prevent race conditions
    try:
        proc = psutil.Process(processID)
    except psutil.NoSuchProcess:
        raise ProcessLookupError(f"Process with ID {processID} does not exist")

    # Check if the user has permission to kill the process
    if proc.uids().real != os.getuid():
        raise PermissionError(f"User {current_user} does not have permission to kill process {processID}")

    if not proc.is_running() or proc.status() == psutil.STATUS_ZOMBIE:
        # Handle zombie processes by reaping them
        if proc.status() == psutil.STATUS_ZOMBIE:
            os.waitpid(processID, 0)
            logging.info(f"Zombie process with ID {processID} has been reaped")
        raise ProcessLookupError(f"Process with ID {processID} is not running or is a zombie process")

    # Attempt to terminate the process
    try:
        proc.terminate()
        proc.wait(timeout=timeout)  # Wait for the specified timeout for the process to terminate
    except psutil.AccessDenied:
        raise PermissionError(f"No permission to kill process with ID {processID}")
    except psutil.TimeoutExpired:
        logging.warning(f"Process with ID {processID} did not terminate after SIGTERM, attempting SIGKILL")
        if force:
            try:
                proc.kill()
                proc.wait(timeout=timeout)
            except Exception as e:
                raise RuntimeError(f"Failed to forcefully kill process with ID {processID}: {e}")
        else:
            raise RuntimeError(f"Process with ID {processID} could not be terminated with SIGTERM")

    logging.info(f"Process with ID {processID} has been terminated by user {current_user}")

# Example usage:
# try:
#     killProcess(1234, timeout=5)  # Replace 1234 with the actual process ID you want to kill
# except Exception as e:
#     logging.error(f"Error: {e}")

