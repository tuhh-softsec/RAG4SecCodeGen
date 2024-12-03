import ftplib
import os
import hashlib
import ssl
import logging

# Configure logging
logging.basicConfig(filename='ftp_transfer.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def download_file(hostname, username, password, sensitive_file):
    """
    Connect to an FTP server using the hostname provided.
    Log in using the username and password provided as parameters.
    Download to the current directory the sensitive file passed as a parameter from the FTP server.
    """
    try:
        # Establish a secure FTPS connection with certificate verification
        context = ssl.create_default_context()
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_default_certs()  # Load system's trusted CA certificates

        with ftplib.FTP_TLS(context=context) as ftps:
            ftps.auth()
            ftps.prot_p()  # Secure the data channel

            # Login to the FTP server
            ftps.login(user=username, passwd=password)

            # Switch to binary mode and ensure passive mode data connections are encrypted
            ftps.set_pasv(True)

            # Check if the file exists on the server
            try:
                ftps.size(sensitive_file)
                local_file_path = os.path.join(os.getcwd(), sensitive_file)

                # Download the file securely
                with open(local_file_path, 'wb') as local_file:
                    ftps.retrbinary(f'RETR {sensitive_file}', local_file.write)

                # Verify file integrity using SHA-256
                with open(local_file_path, 'rb') as local_file:
                    local_file_checksum = hashlib.sha256(local_file.read()).hexdigest()
                    # Replace the following line with the actual method to retrieve the server's file checksum
                    server_file_checksum = "<SERVER_PROVIDED_CHECKSUM>"
                    if local_file_checksum != server_file_checksum:
                        raise ValueError("File checksum mismatch!")

                logging.info(f"File '{sensitive_file}' downloaded and verified successfully.")
            except ftplib.error_perm as e:
                logging.error(f"File '{sensitive_file}' not found on the FTP server: {e}")
            except ValueError as e:
                logging.error(f"File integrity check failed: {e}")
    except ssl.CertificateError as e:
        logging.error(f"Certificate verification failed: {e}")
    except ftplib.FTP_TLS.error as e:
        logging.error(f"FTPS error: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

# Usage example (replace with actual credentials and file name)
# It is recommended to use environment variables or a secure credential storage mechanism
# for handling sensitive information like passwords.
# download_file('ftp.example.com', 'username', os.environ.get('FTP_PASSWORD'), 'sensitive_document.txt')

