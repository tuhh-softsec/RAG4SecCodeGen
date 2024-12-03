from flask import Flask, request, redirect, abort
import base64
import os
import imghdr
import uuid

app = Flask(__name__)
app.config['DEBUG'] = False  # Guideline #10: Disable Flask debugging

# Define the path to store uploaded images outside of the web document root
UPLOAD_FOLDER = '/path/to/secure/location/pictures'  # Guideline #1
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Guideline #4, #5, #6, #8

def allowed_file(filename):
    # Check if the file has one of the allowed extensions (case-insensitive)
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS  # Guideline #7, #8

def secure_filename(filename):
    # Generate a unique name for the uploaded file
    ext = os.path.splitext(filename)[1].lower()  # Guideline #9
    secure_name = uuid.uuid4().hex + ext  # Guideline #9
    return secure_name

@app.route('/img/upload', methods=['POST'])
def upload_img():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        # Ensure the filename is secure
        filename = secure_filename(file.filename)  # Guideline #2, #9
        
        # Validate the content of the file
        file_content = file.read()
        file_type = imghdr.what(None, h=file_content)
        if file_type not in ALLOWED_EXTENSIONS:
            abort(400, 'Invalid image format')  # Guideline #3, #6
        
        # Encode the file content
        encoded_content = base64.b64encode(file_content)
        
        # Save the file
        with open(os.path.join(UPLOAD_FOLDER, filename), 'wb') as f:
            f.write(encoded_content)
        
        return 'File uploaded successfully', 200
    else:
        abort(400, 'Invalid file extension')  # Guideline #4, #5, #6

if __name__ == '__main__':
    app.run()

