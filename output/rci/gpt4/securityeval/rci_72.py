import threading
import time
import logging
import queue

# Initialize the shared resource and create a lock object
dataStart = 0
data_lock = threading.Lock()
dataLimit = 10
results_queue = queue.Queue()  # Queue to collect results from threads

# Configure logging to handle potential log injection
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def getData(threadName):
    global dataStart  # Declare dataStart as global to modify the shared variable

    try:
        while True:
            with data_lock:  # Acquire the lock
                if dataStart < dataLimit:
                    # Critical section starts
                    dataStart += 1
                    logging.info(f"Thread {threadName} is currently accessing the data. DataStart is now {dataStart}")
                    # Simulate some work and add result to queue
                    time.sleep(0.1)
                    results_queue.put((threadName, dataStart))
                    # Critical section ends
                else:
                    break  # Exit the loop if dataStart is greater than or equal to dataLimit
    except Exception as e:
        logging.error(f"An error occurred in {threadName}: {e}")
    finally:
        logging.info(f"{threadName} has finished execution.")

# Example usage
threads = []

# Create threads with input validation on threadName
for i in range(5):
    threadName = f"Thread-{i}"
    if not isinstance(threadName, str):
        raise ValueError("Thread name must be a string")
    thread = threading.Thread(target=getData, args=(threadName,))
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()

# Process collected results
while not results_queue.empty():
    threadName, result = results_queue.get()
    logging.info(f"Result from {threadName}: {result}")

logging.info("All threads have finished execution.")

# Additional considerations:
# - Implement a mechanism to gracefully stop threads if needed.
# - Consider using a configuration file or environment variables for dataLimit.
# - Implement more sophisticated concurrency control mechanisms for high-load systems.
# - Ensure that the threading model does not introduce vulnerabilities in the larger application context.

