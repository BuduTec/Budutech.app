import re

with open('src/store.ts', 'r') as f:
    content = f.read()

# Change clients: mockClients to clients: []
content = content.replace("clients: mockClients,", "clients: [],")

with open('src/store.ts', 'w') as f:
    f.write(content)
