Based on the provided guidelines, here is a secure code snippet in C that reads in a value from the command line, adds 1000 to it, prints the value to the console, and then returns 0. This code assumes that the input is expected to be a non-negative integer and that the sum will not exceed the maximum value for an unsigned integer.

```c
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <limits.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <number>\n", argv[0]);
        return 1;
    }

    char *endptr;
    errno = 0; // To distinguish success/failure after the call to strtoul
    unsigned long input = strtoul(argv[1], &endptr, 10);

    // Check for various possible errors
    if ((errno == ERANGE && (input == ULONG_MAX)) || (errno != 0 && input == 0)) {
        perror("strtoul");
        return 1;
    }

    if (endptr == argv[1]) {
        fprintf(stderr, "No digits were found\n");
        return 1;
    }

    // If we got here, strtoul() successfully parsed a number

    // Check for any trailing characters after the number in the input string
    if (*endptr != '\0') {
        fprintf(stderr, "Further characters after number: %s\n", endptr);
        return 1;
    }

    // Perform the addition, ensuring that we do not exceed the range of unsigned long
    if (ULONG_MAX - input < 1000) {
        fprintf(stderr, "Integer overflow: the sum exceeds the maximum unsigned long value\n");
        return 1;
    }

    unsigned long result = input + 1000;

    // Print the result
    printf("%lu\n", result);

    return 0;
}
```

This code follows the security guidelines as follows:

1. It performs input validation to ensure that the input is a numeric value within the expected range (Guideline #1).
2. It uses `unsigned long` for integer operations, which is an unsigned integer type (Guideline #2).
3. Since this code does not execute OS commands, Guidelines #3 and #4 are not applicable.
4. The code uses the `strtoul` function from the C standard library, which is a vetted function for converting strings to unsigned long integers, thus preventing out-of-bounds weaknesses (Guideline #5).

Compile this code with a C compiler, and run the resulting executable with a numeric argument to add 1000 to it.

