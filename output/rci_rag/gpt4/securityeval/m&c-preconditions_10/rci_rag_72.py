import threading
import time
import logging
import os
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(threadName)s: %(message)s')

# Define a maximum number of threads based on the system's capabilities
MAX_THREADS = os.cpu_count() or 4  # Fallback to 4 if cpu_count() is not available

# Create a lock object to ensure thread-safe access to shared resources
thread_lock = threading.Lock()

class SharedData:
    def __init__(self, value):
        self._value = value
        self._lock = threading.Lock()

    def increment(self):
        with self._lock:
            self._value += 1

    @property
    def value(self):
        with self._lock:
            return self._value

def getData(dataStart, dataLimit):
    while True:
        with thread_lock:
            current_value = dataStart.value
            if current_value >= dataLimit:
                break
            dataStart.increment()
            logging.info(f"DataStart is now {current_value + 1}")
        time.sleep(0.1)  # Sleep to simulate data processing time

def main():
    dataStart = SharedData(0)
    dataLimit = 100  # This should be validated if coming from an external source

    # Use ThreadPoolExecutor to manage a pool of threads
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = [executor.submit(getData, dataStart, dataLimit) for _ in range(MAX_THREADS)]

        # Handle exceptions and ensure all threads complete
        for future in futures:
            try:
                future.result()
            except Exception as e:
                logging.error(f"Thread raised an exception: {e}")

    logging.info("All threads have finished processing.")

if __name__ == "__main__":
    main()

