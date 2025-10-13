import os
import dj_database_url
from .base import *

# OVERRIDE critical production settings
DEBUG = False

# This tells Django where your main URL routing file is located
ROOT_URLCONF = 'mubaku.urls'

# Define ALLOWED_HOSTS for security (CRITICAL for DEBUG=False)
ALLOWED_HOSTS = [
    '.onrender.com',
    'mubaku-backend.onrender.com', # Your specific domain
]

# Define STATIC_ROOT (CRITICAL for collectstatic to work at runtime)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = '/var/data/media'

# Database Configuration
DATABASES = {
    'default': dj_database_url.config(
        # Feel free to replace 'DATABASE_URL' with your own variable
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600
    )
}
