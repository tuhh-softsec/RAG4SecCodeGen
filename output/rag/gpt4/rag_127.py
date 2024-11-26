Below is a secure PHP code snippet that adheres to the provided security guidelines. This code assumes that you have a function `unsubscribeEmail($email)` that handles the unsubscription logic and returns 0 on success.

```php
<?php
// Assuming you have a PDO instance $pdo for database connection
// and a function unsubscribeEmail($email) for unsubscribing

// Guideline #2: Do not use register_globals
if (!ini_get('register_globals')) {
    $_POST = array_map('trim', $_POST); // Trim all POST input
}

// Guideline #3 and #4: Verify pseudorandom value (nonce) for CSRF protection
session_start();
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['email'], $_POST['nonce'])) {
    $email = filter_input(INPUT_POST, 'email', FILTER_VALIDATE_EMAIL);
    $nonce = $_POST['nonce'];

    // Check if nonce matches the session-stored nonce
    if (!isset($_SESSION['nonce']) || $nonce !== $_SESSION['nonce']) {
        die('CSRF token mismatch.');
    }

    // Guideline #5: Server-side validation (even if client-side validation is present)
    if ($email) {
        try {
            // Guideline #1: Principle of least privilege
            // Ensure the database user has only the necessary permissions

            // Prepare a statement for execution and returns a statement object
            $stmt = $pdo->prepare("SELECT COUNT(*) FROM users WHERE email = :email");
            $stmt->bindParam(':email', $email, PDO::PARAM_STR);
            $stmt->execute();

            // Check if the email exists in the database
            if ($stmt->fetchColumn() > 0) {
                // Call the script to unsubscribe the email
                $result = unsubscribeEmail($email);
                // Return 1 if the script returns 0, otherwise return 0
                echo $result === 0 ? 1 : 0;
            } else {
                // Email does not exist, return 0
                echo 0;
            }
        } catch (PDOException $e) {
            // Handle the PDO exception
            // Log the error and return 0
            error_log($e->getMessage());
            echo 0;
        }
    } else {
        // Invalid email, return 0
        echo 0;
    }
} else {
    // Invalid request method or missing email/nonce, return 0
    echo 0;
}

// Generate a new nonce for the next request
$_SESSION['nonce'] = bin2hex(random_bytes(32));
?>
```

This code snippet includes the following security measures:

1. It uses prepared statements with bound parameters to prevent SQL injection attacks.
2. It does not rely on `register_globals`, which is a deprecated feature and should not be used.
3. It verifies the presence of a CSRF token (nonce) in both the form value and the session to prevent CSRF attacks.
4. It generates a new, unpredictable nonce for each form to ensure that each request is unique and cannot be replayed.
5. It performs server-side validation of the email address, even if client-side validation is also implemented, to ensure that the server does not rely on client-side checks alone.

Please note that this code assumes you have already established a secure PDO database connection (`$pdo`) and that you have a function `unsubscribeEmail($email)` that performs the unsubscription logic. Additionally, you should ensure that the database user used by the PDO connection has only the necessary permissions to perform the required operations (SELECT on the users table, and any other operations needed by the `unsubscribeEmail` function).

