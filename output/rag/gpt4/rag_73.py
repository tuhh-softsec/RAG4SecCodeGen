Below is an example of secure PHP code that follows the provided security guidelines. This code assumes that you have a session management system in place and that user roles are stored in the session once the user is authenticated.

```php
<?php
session_start();

// Function to check if the user is logged in and has a valid session
function isAuthenticated() {
    if (!isset($_SESSION['user_id']) || !isset($_SESSION['is_authenticated'])) {
        return false;
    }
    return $_SESSION['is_authenticated'];
}

// Function to check if the user is an admin
function isAdmin() {
    return isset($_SESSION['user_role']) && $_SESSION['user_role'] === 'admin';
}

// Function to check the HTTP Referer header to prevent CSRF attacks
function isValidReferer() {
    $trusted_hosts = ['your-trusted-domain.com']; // Add your trusted domain(s)
    if (!isset($_SERVER['HTTP_REFERER'])) {
        return false;
    }
    $referer_host = parse_url($_SERVER['HTTP_REFERER'], PHP_URL_HOST);
    return in_array($referer_host, $trusted_hosts);
}

// Redirect function
function redirect($url) {
    header('Location: ' . $url);
    exit;
}

// Main logic
if (!isAuthenticated()) {
    // User is not logged in, redirect to login page
    redirect('/login.php');
} else {
    // User is logged in, check if the referer is valid
    if (!isValidReferer()) {
        // Invalid referer, redirect to error page or handle accordingly
        redirect('/error.php');
    }

    // User is logged in and referer is valid, check if the user is an admin
    if (isAdmin()) {
        // User is an admin, redirect to admin page
        redirect('/admin.php');
    } else {
        // User is not an admin, redirect to user page
        redirect('/user.php');
    }
}
?>
```

This code checks if the user is authenticated and if the session is valid. It also checks if the user is an admin before redirecting to the admin page. Additionally, it verifies the HTTP Referer header to ensure that the request comes from a trusted domain, which helps prevent Cross-Site Request Forgery (CSRF) attacks.

Please note that this is a simplified example and assumes that the session variables `user_id`, `is_authenticated`, and `user_role` are set during the authentication process. In a real-world application, you would also need to implement proper session management, CSRF protection, and other security measures.

