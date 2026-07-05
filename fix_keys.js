const fs = require('fs');
let code = fs.readFileSync('src/pages/AdminHubPage.tsx', 'utf8');

code = code.replace(/<motion\.div key="motion-box"/, '<motion.div key="feed"');
code = code.replace(/<motion\.div key="motion-box"/, '<motion.div key="filters"');
code = code.replace(/<motion\.div key="motion-box"/, '<motion.div key="client"');

fs.writeFileSync('src/pages/AdminHubPage.tsx', code);
