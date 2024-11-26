import subprocess
import shlex
import sys

def get_user_info(username):
    # Escape and quote the username to prevent command injection
    safe_username = shlex.quote(username)
    
    # Construct the command with safe username
    command = f"grep {safe_username} /etc/passwd"
    
    # Execute the command securely without using a shell
    try:
        result = subprocess.run(command, shell=False, check=True, text=True, capture_output=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        return None

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 secure_user_info.py <username>", file=sys.stderr)
        sys.exit(1)
    
    username = sys.argv[1]
    user_info = get_user_info(username)
    
    if user_info:
        print(user_info)
    else:
        print(f"No information found for user: {username}")

if __name__ == "__main__":
    main()

