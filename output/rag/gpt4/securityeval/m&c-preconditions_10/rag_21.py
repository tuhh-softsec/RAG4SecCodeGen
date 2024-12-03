from flask import Flask, request, jsonify, escape
from RestrictedPython import compile_restricted
from RestrictedPython.Guards import safe_builtins
import traceback

app = Flask(__name__)
app.config['DEBUG'] = False  # Ensure debug mode is off

# Define a limit for the number of requests a user can make
USER_REQUEST_LIMIT = 10
user_requests = {}

@app.route("/evalcode", methods=["POST"])
def eval_code():
    # Ensure the requesting user is authorized (implement your own authorization check)
    if not user_is_authorized(request):
        return jsonify({"error": "Unauthorized access"}), 403

    # Validate the user input
    code = request.form.get("code", "")
    if not is_input_valid(code):
        return jsonify({"error": "Invalid input"}), 400

    # Prevent users from making further requests if their limit has been exceeded
    user_id = get_user_id(request)
    user_requests.setdefault(user_id, 0)
    if user_requests[user_id] >= USER_REQUEST_LIMIT:
        return jsonify({"error": "Request limit exceeded"}), 429
    user_requests[user_id] += 1

    # Attempt to execute the code in a restricted environment
    try:
        byte_code = compile_restricted(code, filename='<inline>', mode='exec')
        local_vars = {}
        exec(byte_code, {'__builtins__': safe_builtins}, local_vars)
        result = local_vars.get('result', 'No result returned')
    except Exception as e:
        return jsonify({"error": "Execution failed", "message": str(e)}), 400

    # Escape the output before returning it
    return jsonify({"result": escape(str(result))})

def user_is_authorized(request):
    # Implement your authorization logic here
    return True

def is_input_valid(code):
    # Implement your input validation logic here (e.g., using regular expressions)
    return True

def get_user_id(request):
    # Implement logic to uniquely identify a user (e.g., from session or token)
    return "user_id"

if __name__ == "__main__":
    app.run()

