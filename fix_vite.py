with open('vite.config.ts', 'r') as f:
    content = f.read()

content = content.replace("    },\n  };\n});", "    },\n    optimizeDeps: {\n      include: ['trim-canvas', 'react-signature-canvas']\n    }\n  };\n});")

with open('vite.config.ts', 'w') as f:
    f.write(content)
