import time

def current_processor_time():
    """
    Return the current processor time in seconds.

    This function retrieves the processor time, which is the sum of the system
    and user CPU time of the current process. It does not include time elapsed
    during sleep and is useful for performance testing or benchmarking.

    Returns:
        float: The current processor time in seconds.

    Raises:
        OSError: If the processor time cannot be retrieved due to a system-related error.

    Note:
        The `time.process_time()` function is available in Python 3.3 and later.
        If you are using an older version of Python, you might need to use a
        different function to measure processor time.
    """
    try:
        # Get the current processor time
        processor_time = time.process_time()
        return processor_time
    except OSError as e:
        raise RuntimeError(f"An error occurred while retrieving processor time: {e}")

# Example usage of the function
if __name__ == "__main__":
    try:
        # Call the function and print the current processor time
        processor_time = current_processor_time()
        print(f"Current processor time: {processor_time} seconds")
    except RuntimeError as error:
        print(error)

