# 1. Import all settings from the base configuration
from .base import * # 2. OVERRIDE critical production settings
DEBUG = False

# 3. Define ROOT_URLCONF (if not already defined in base.py)
# This tells Django where your main URL routing file is located
ROOT_URLCONF = 'app.mubaku.urls' # <-- Adjust if your urls.py is in a different path

# 4. Define ALLOWED_HOSTS for security (CRITICAL for DEBUG=False)
ALLOWED_HOSTS = [
    '.onrender.com', 
    'mubaku-backend.onrender.com', # Your specific domain
    # Add any other domains your service will use
]

# 5. Define STATIC_ROOT (CRITICAL for collectstatic to work at runtime)
# This should point to a location where collected static files are stored.
# Ensure BASE_DIR is defined in base.py.
# from pathlib import Path # If you need Path, ensure it's imported in base.py
# STATIC_ROOT = BASE_DIR / "staticfiles"
# You might need a path calculation here depending on your base.py
import os
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# 6. Database Configuration (if not handled by dj_database_url in base.py)
# Since you're using Render's DATABASE_URL environment variable, 
# you likely handle this with a line like:
# DATABASES['default'] = dj_database_url.config(conn_max_age=600)
# Ensure any necessary imports (like dj_database_url) are handled in base.py