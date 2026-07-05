import re

with open('src/store.ts', 'r') as f:
    content = f.read()

# Delete mockClients array
content = re.sub(r'const mockClients: ClientProfile\[\] = \[.*?\];\n', '', content, flags=re.DOTALL)

with open('src/store.ts', 'w') as f:
    f.write(content)
