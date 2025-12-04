import os

# Try different ways to see what DEBUG is
os.environ['DJANGO_SETTINGS_MODULE'] = 'sams.settings'

print("1. Environment variable DEBUG:", os.environ.get('DEBUG', 'Not set'))
print("2. Environment variable ALLOWED_HOSTS:", os.environ.get('ALLOWED_HOSTS', 'Not set'))

# Now see what config() returns
from decouple import config, RepositoryEnv
import sys

# Find the .env file
env_file = '.env'
if os.path.exists(env_file):
    print(f"3. .env file exists at: {os.path.abspath(env_file)}")
    repo = RepositoryEnv(env_file)
    print(f"4. DEBUG from .env: {repo.get('DEBUG')}")
    print(f"5. ALLOWED_HOSTS from .env: {repo.get('ALLOWED_HOSTS')}")
else:
    print("3. No .env file found")

# What does config() return?
print(f"6. config('DEBUG'): {config('DEBUG', default='NOT FOUND')}")
print(f"7. config('ALLOWED_HOSTS'): {config('ALLOWED_HOSTS', default='NOT FOUND')}")
