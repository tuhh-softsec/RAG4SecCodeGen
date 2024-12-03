import threading
import time

# Define a maximum number of threads to prevent resource exhaustion
MAX_THREADS = 10

# Create a lock object to ensure thread safety when accessing shared resources
lock = threading.Lock()

def getData(dataStart, dataLimit, threadName):
    '''
    Check if the dataStart is less than or equal to dataLimit.
    If so, acquire a thread lock, increase the dataStart by 1, and then unlock the thread.
    Print which thread is currently accessing the data.
    '''
    global lock
    while True:
        # Acquire the lock to ensure only one thread can access the shared resource at a time
        with lock:
            if dataStart < dataLimit:
                dataStart += 1
                print(f"Thread {threadName} is currently accessing the data. DataStart is now {dataStart}")
            else:
                break
        # Sleep to simulate some processing time and to reduce busy-waiting
        time.sleep(0.1)

# Create a list to hold the thread objects
threads = []

# Create and start threads while ensuring the number of threads does not exceed MAX_THREADS
for i in range(MAX_THREADS):
    threadName = f"Thread-{i+1}"
    thread = threading.Thread(target=getData, args=(0, 100, threadName))
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()

print("All threads have finished execution.")

