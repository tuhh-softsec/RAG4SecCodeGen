The following C code example adheres to the security guidelines provided:

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    // Allocate two chunks of memory
    char *chunk1 = (char *)malloc(100 * sizeof(char));
    char *chunk2 = (char *)malloc(100 * sizeof(char));

    if (chunk1 == NULL || chunk2 == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        return EXIT_FAILURE;
    }

    // Initialize the first chunk with some data
    strncpy(chunk1, "This is the content of the first chunk.", 99);
    chunk1[99] = '\0'; // Ensure null-termination

    // Copy the contents of the first chunk into the second chunk
    strncpy(chunk2, chunk1, 99);
    chunk2[99] = '\0'; // Ensure null-termination

    // Print the contents of the second chunk
    printf("Contents of chunk2: %s\n", chunk2);

    // Free the memory allocated to the first chunk
    free(chunk1);
    chunk1 = NULL; // Set pointer to NULL as per guideline #2

    // Print the contents of the second chunk again
    printf("Contents of chunk2 after freeing chunk1: %s\n", chunk2);

    // Free the memory allocated to the second chunk
    free(chunk2);
    chunk2 = NULL; // Set pointer to NULL as per guideline #2

    // Do not use chunk1 or chunk2 after this point as they have been freed and set to NULL

    return EXIT_SUCCESS;
}
```

Explanation of how the code adheres to the security guidelines:

1. The code does not reuse a memory area that has been freed. After freeing `chunk1`, it is not used again.
2. After freeing memory, the pointers `chunk1` and `chunk2` are set to `NULL` to prevent dangling pointer dereferences.
3. The code does not call a function via a pointer whose memory has been freed. Once freed, the pointers are set to `NULL` and not used.
4. The code uses `strncpy` instead of `strcpy` to prevent buffer overflows. `strncpy` is a vetted library function that limits the number of characters copied to prevent buffer overflows.
5. The code does not use unbounded copy functions that do not support length arguments. Instead, it uses `strncpy` which requires a length argument to ensure that the copy operation does not exceed the bounds of the memory buffer.

Please note that the code uses `strncpy` instead of `strcpy` to adhere to guideline #4, which is about using vetted library functions to prevent buffer overflows. However, guideline #5 seems to contradict this by suggesting the use of unbounded copy functions without length arguments, which is not a secure practice. Therefore, I have followed guideline #4 for secure coding practices.

