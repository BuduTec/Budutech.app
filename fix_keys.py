with open('src/pages/AdminHubPage.tsx', 'r') as f:
    code = f.read()

code = code.replace('<motion.div key="motion-box"', '<motion.div key="feed"', 1)
code = code.replace('<motion.div key="motion-box"', '<motion.div key="filters"', 1)
code = code.replace('<motion.div key="motion-box"', '<motion.div key="client"', 1)

with open('src/pages/AdminHubPage.tsx', 'w') as f:
    f.write(code)
