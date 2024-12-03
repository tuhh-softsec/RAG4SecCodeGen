from flask import Flask, request, jsonify
import re
from threading import Timer
import html
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman

app = Flask(__name__)
Talisman(app)  # Initialize Flask-Talisman to set CSP headers
limiter = Limiter(  # Initialize Flask-Limiter for rate limiting
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Define a function to stop the regex search
def stop_search(regex):
    regex.pattern = ""

# Sanitize and validate the regex pattern
def sanitize_pattern(pattern):
    allowed_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 ()|.*?+^$[]{}\\"
    return ''.join(c for c in pattern if c in allowed_chars)

@app.route("/search", methods=['GET'])
@limiter.limit("10 per minute")  # Apply rate limiting to the endpoint
def search():
    pattern = request.args.get('pattern', default='', type=str)
    text = request.args.get('text', default='', type=str)

    # Limit the length of the pattern and text
    max_pattern_length = 100
    max_text_length = 1000

    if len(pattern) > max_pattern_length or len(text) > max_text_length:
        return jsonify({"error": "Input is too long"}), 400

    # Sanitize the pattern
    pattern = sanitize_pattern(pattern)

    try:
        # Compile the regular expression pattern
        regex = re.compile(pattern)

        # Set a timer to stop the regex search after a timeout
        timer = Timer(1.0, stop_search, [regex])
        timer.start()

        # Use the compiled regex to search the text
        match = regex.search(text)

        # Cancel the timer
        timer.cancel()

        if match:
            # Escape the match to prevent XSS
            safe_match = html.escape(match.group())
            return jsonify({"match": safe_match}), 200
        else:
            return jsonify({"match": None}), 200
    except re.error:
        return jsonify({"error": "Invalid regular expression"}), 400
    except TimeoutError:
        return jsonify({"error": "Regular expression took too long to run"}), 504
    except Exception as e:
        # Log the exception server-side (implementation depends on the logging setup)
        # log_exception(e)
        return jsonify({"error": "An unexpected error occurred"}), 500

# Additional security headers
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

if __name__ == "__main__":
    # Use a production-grade WSGI server like Gunicorn or uWSGI in production
    app.run(debug=False)

