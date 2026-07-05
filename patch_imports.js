const fs = require('fs');
let code = fs.readFileSync('src/pages/AdminHubPage.tsx', 'utf8');
code = code.replace(/import \{ Download, Bell, ChevronDown, Activity, Clock, BarChart2,  /g, 'import { ');
code = code.replace(/import \{  Search, Filter/, 'import { Download, Bell, ChevronDown, Activity, Clock, BarChart2, Search, Filter');
fs.writeFileSync('src/pages/AdminHubPage.tsx', code);
