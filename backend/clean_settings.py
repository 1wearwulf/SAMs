import re

with open('sams/settings/__init__.py', 'r') as f:
    content = f.read()

# Remove duplicate accounts entries
content = re.sub(r"if 'api\.apps\.accounts' not in INSTALLED_APPS:.*?\n.*INSTALLED_APPS\.append\('api\.apps\.accounts'\).*?\n", '', content, flags=re.DOTALL)
content = re.sub(r"if 'api\.apps\.accounts' not in INSTALLED_APPS:.*?\n.*INSTALLED_APPS\.append\('api\.apps\.accounts'\).*?\n", '', content, flags=re.DOTALL)

# Make sure AUTH_USER_MODEL is correct
content = re.sub(r"AUTH_USER_MODEL = 'accounts\.User'", "AUTH_USER_MODEL = 'api.apps.accounts.User'", content)

with open('sams/settings/__init__.py', 'w') as f:
    f.write(content)

print("Cleaned settings file")
