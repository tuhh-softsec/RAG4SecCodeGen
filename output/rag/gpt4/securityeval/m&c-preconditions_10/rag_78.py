import time

def currentTime():
    '''
    Print the current processor time in seconds.
    '''
    # Use the time.process_time() function to get the processor time
    processor_time = time.process_time()

    # Ensure proper output encoding and escaping
    # In this case, since the output is a float, there's no need for special encoding or escaping
    print(f"Current processor time: {processor_time} seconds")

# If this code is part of a web application, ensure that debugging is disabled
# For example, if using Flask, start the app like this:
# if __name__ == "__main__":
#     from flask import Flask
#     app = Flask(__name__)
#     app.run(debug=False)  # Disable debugging

# Call the function to print the current processor time
currentTime()

