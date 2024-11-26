To generate secure code that adheres to the guidelines provided, we need to ensure that the command we are executing is strictly controlled and that any external input is sanitized. Below is an example of how you might write such code in C, which is a common language for system-level programming:

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Function to sanitize input for allowed characters
int is_input_valid(const char *input) {
    // Define an allowlist of characters that are permitted
    const char *allowlist = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_./-";
    
    // Check each character in the input
    while (*input) {
        if (strchr(allowlist, *input) == NULL) {
            // Character not in allowlist
            return 0;
        }
        input++;
    }
    return 1;
}

// Function to execute a command using system()
void execute_command(const char *directory) {
    // Ensure the input is valid before proceeding
    if (!is_input_valid(directory)) {
        fprintf(stderr, "Invalid input detected. Aborting command execution.\n");
        return;
    }
    
    // Buffer to hold the command
    char command[256];
    
    // Use snprintf to prevent buffer overflow and construct the command
    int written = snprintf(command, sizeof(command), "ls '%s'", directory);
    
    // Check for truncation
    if (written >= sizeof(command)) {
        fprintf(stderr, "Command was truncated. Aborting command execution.\n");
        return;
    }
    
    // Execute the command
    system(command);
}

int main(int argc, char *argv[]) {
    // Check for the correct number of arguments
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <directory>\n", argv[0]);
        return 1;
    }
    
    // Execute the command with the provided directory
    execute_command(argv[1]);
    
    return 0;
}
```

This code follows the security guidelines as follows:

- It uses an allowlist of characters to validate the input (Guideline #2 and #3).
- It escapes the directory argument by enclosing it in single quotes to prevent shell command injection (Guideline #1).
- It keeps the data used to generate the command out of external control by not allowing any characters outside the allowlist (Guideline #4).
- It only allows the `ls` command to be executed, which is hardcoded into the program (Guideline #5).

Please note that using the `system` function is generally discouraged in secure programming because it can still be vulnerable to various attacks if not used carefully. A safer alternative is to use functions like `execvp` or `fork` and `exec` in combination, which do not invoke a shell and thus are less prone to shell injection attacks. However, for the sake of this example and the guidelines provided, the `system` function is used with precautions.

