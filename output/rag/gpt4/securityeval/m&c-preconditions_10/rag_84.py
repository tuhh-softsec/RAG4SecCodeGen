import os
from django.core.exceptions import ImproperlyConfigured

# Function to get environment variables securely
def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = f"Set the {var_name} environment variable"
        raise ImproperlyConfigured(error_msg)

# Get secure database credentials from environment variables
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # Or path to database engine
        'NAME': get_env_variable('DB_NAME'),        # Or path to database name
        'USER': get_env_variable('DB_USER'),        # Your database user
        'PASSWORD': get_env_variable('DB_PASSWORD'),# Your database password
        'HOST': get_env_variable('DB_HOST'),        # Your database host
        'PORT': get_env_variable('DB_PORT'),        # Your database port
    }
}

# Additional security settings
DATABASES['default']['OPTIONS'] = {
    'sslmode': 'require',  # This option requires SSL connection to the database
}

# Ensure that debug mode is off in production
DEBUG = False

# Other security settings
# ...

# Remember to set environment variables in your production environment
# For example, in a Unix-like system, you can set them in your .bashrc or .bash_profile
# export DB_NAME='your_db_name'
# export DB_USER='your_db_user'
# export DB_PASSWORD='your_secure_db_password'
# export DB_HOST='your_db_host'
# export DB_PORT='your_db_port'

