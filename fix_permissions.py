
import os

file_path = 'api.py'
with open(file_path, 'r') as f:
    content = f.read()

# Replace role_required calls to include OWNER
new_content = content.replace("@role_required('ADMIN'", "@role_required('OWNER', 'ADMIN'")

with open(file_path, 'w') as f:
    f.write(new_content)

print("Updated api.py with OWNER permissions")
