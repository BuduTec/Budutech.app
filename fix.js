const fs = require('fs');
let code = fs.readFileSync('src/pages/AdminHubPage.tsx', 'utf8');
code = code.replace(/headers\.join\(\",\"\)\s*\+\s*\"\n\"/g, 'headers.join(",") + "\\n"');
code = code.replace(/\.join\(\"\n\"\);/g, '.join("\\n");');
fs.writeFileSync('src/pages/AdminHubPage.tsx', code);
