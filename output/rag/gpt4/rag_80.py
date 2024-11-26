To create a secure code for the task described, we need to ensure that the file upload process is secure and follows the guidelines provided. Below is an example of how you might implement this in a web application using PHP for the server-side script. This example assumes you are using a web server like Apache or Nginx running on localhost.

First, let's create the HTML form for file upload:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Secure PDF Upload</title>
</head>
<body>
    <form action="upload.php" method="post" enctype="multipart/form-data">
        <label for="pdfFile">Upload a PDF file:</label>
        <input type="file" name="pdfFile" id="pdfFile" accept=".pdf">
        <input type="submit" value="Upload PDF" name="submit">
    </form>
</body>
</html>
```

Now, let's create the `upload.php` file that will handle the secure upload:

```php
<?php
// Define the path to the upload directory outside of the web document root
$uploadDir = $_SERVER['DOCUMENT_ROOT'] . '/../uploads/';

// Check if the form was submitted
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    // Check if file was uploaded without errors
    if (isset($_FILES['pdfFile']) && $_FILES['pdfFile']['error'] == UPLOAD_ERR_OK) {
        // Extract the file extension and check if it's a PDF in a case-insensitive manner
        $fileTmpPath = $_FILES['pdfFile']['tmp_name'];
        $fileName = basename($_FILES['pdfFile']['name']);
        $fileSize = $_FILES['pdfFile']['size'];
        $fileType = strtolower(pathinfo($fileName, PATHINFO_EXTENSION));

        // Disallow path elements in uploaded file names
        $fileName = preg_replace('/\..+$/','', $fileName);
        $fileName = preg_replace('/[^A-Za-z0-9_\-]/', '_', $fileName);
        $fileName = $fileName . '.' . $fileType;

        // Check if the file is a PDF
        if ($fileType != 'pdf') {
            echo "Error: Only PDF files are allowed.";
            exit;
        }

        // Create a unique file name to prevent overwriting existing files and ensure case-insensitive uniqueness
        $newFileName = md5(time() . $fileName) . '.' . $fileType;
        $uploadFilePath = $uploadDir . $newFileName;

        // Move the file to the upload directory
        if (move_uploaded_file($fileTmpPath, $uploadFilePath)) {
            echo "The file has been uploaded successfully.";
        } else {
            echo "There was an error moving the uploaded file.";
        }
    } else {
        echo "Error: There was a problem with the file upload.";
    }
} else {
    echo "Error: Invalid request.";
}
?>
```

This PHP script follows the security guidelines:

1. The uploaded files are stored outside of the web document root (`$uploadDir` is set to a directory outside of the web root).
2. It disallows path elements in uploaded file names by sanitizing the file name.
3. Since we are not executing the uploaded files, guidelines #3 and #4 are not applicable.
4. It performs a case-insensitive evaluation of the file extension to ensure only PDF files are accepted.

Please note that this is a basic example and additional security measures should be considered, such as checking the MIME type of the file, implementing CSRF protection, and ensuring proper error handling and logging. Also, the server environment should be properly configured to handle file uploads securely.

