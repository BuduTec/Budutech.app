import re
with open('src/pages/AdminHubPage.tsx', 'r') as f:
    code = f.read()

code = code.replace('headers.join(",") + "\\\n"', 'headers.join(",") + "\\\\n"')
code = code.replace('.join("\\\n");', '.join("\\\\n");')
with open('src/pages/AdminHubPage.tsx', 'w') as f:
    f.write(code)
