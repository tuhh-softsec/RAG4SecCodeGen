DATABASES = {
    'default': {
        # ... other settings ...
        'OPTIONS': {
            'sslmode': 'require',
            'sslrootcert': '/path/to/ca-certificate',
            # ... other SSL options ...
        },
    }
}

