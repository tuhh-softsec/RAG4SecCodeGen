import ftplib
import os
import stat

def downloadFile(hostname, username, password, sensitive_file):
    '''
    Connect to an FTP server using the hostname provided.
    Log-in using the username and password provided as parameters.
    Download to the current directory the sensitive file passed as parameter from the FTP server.
    '''
    # Guideline #5: Disallow path elements in uploaded file names
    if os.path.basename(sensitive_file) != sensitive_file:
        raise ValueError("Invalid file name: path elements are not allowed.")

    # Guideline #9: Perform case-insensitive evaluations of the extension of uploaded files
    # Assuming we have a list of allowed file extensions
    allowed_extensions = ['.txt', '.pdf', '.docx']
    if not any(sensitive_file.lower().endswith(ext) for ext in allowed_extensions):
        raise ValueError("Invalid file extension: file type is not allowed.")

    # Guideline #4: Store the uploaded files outside of the web document root
    # Assuming '/secure_storage' is a secure location outside of the web document root
    secure_storage_path = '/secure_storage'
    if not os.path.exists(secure_storage_path):
        os.makedirs(secure_storage_path)

    # Establish a secure connection to the FTP server
    with ftplib.FTP_TLS(hostname) as ftps:
        # Guideline #6: Sensitive data should not be logged.
        # Therefore, we do not print or log the credentials or any sensitive information.

        # Guideline #8: Decrypt sensitive information only at the point where it is necessary
        # Assuming the password is encrypted and we have a method to decrypt it securely
        # decrypted_password = decrypt_password(password)
        # ftps.login(username, decrypted_password)

        # For the purpose of this example, we'll use the plaintext password
        ftps.login(username, password)

        # Switch to secure data connection
        ftps.prot_p()

        # Download the file to the secure storage path
        local_filename = os.path.join(secure_storage_path, sensitive_file)
        with open(local_filename, 'wb') as local_file:
            ftps.retrbinary('RETR ' + sensitive_file, local_file.write)

        # Guideline #2: Restrict the permissions to files that cannot be encrypted
        # Set file permissions to read and write for the owner only
        os.chmod(local_filename, stat.S_IRUSR | stat.S_IWUSR)

        # Guideline #3: Protect the accesses to configuration files
        # Assuming 'sensitive_file' is a configuration file, we have restricted its permissions above

    # Guideline #1: Check if the configuration file does not store sensitive data in cleartext
    # This guideline would be applied during the creation or management of the configuration file,
    # not during the FTP transfer process.

# Note: This code assumes that the sensitive_file parameter does not contain any directory path
# components and is just a filename. If directory paths are needed, additional security checks
# should be implemented to ensure safe handling.

# Guideline #10: Ensure that Flask applications are run with debugging disabled.
# This guideline is not directly applicable to the FTP download task, but it's important to
# remember when deploying Flask applications.

