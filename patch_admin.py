import re

with open('src/pages/AdminHubPage.tsx', 'r') as f:
    content = f.read()

# 1. Imports
content = content.replace("import { \n  Search", "import { Download, Bell, ChevronDown, Activity, Clock, BarChart2, \n  Search")

# 2. State
state_insert = """
  const [filterJurisdiction, setFilterJurisdiction] = useState('');
  const [filterType, setFilterType] = useState('');
  const [filterAlertOnly, setFilterAlertOnly] = useState(false);
  const [showActivityFeed, setShowActivityFeed] = useState(false);
  const [showFilters, setShowFilters] = useState(false);
"""
content = re.sub(r'(const \[searchQuery, setSearchQuery\] = useState\(''\);\n)', r'\1' + state_insert, content)

# 3. Filtering Logic
new_filter_logic = """
  const filteredClients = clients.filter(client => {
    const query = searchQuery.toLowerCase();
    const primaryName = client.intakeData.enterpriseDetails?.proposedNames?.[0] || 
                        client.intakeData.companyDetails?.proposedNames?.[0] || 
                        client.intakeData.ngoDetails?.proposedNames?.[0] || 
                        client.email;
    const matchesSearch = primaryName.toLowerCase().includes(query) || client.email.toLowerCase().includes(query);
    const matchesType = filterType ? client.package.type === filterType : true;
    const matchesAlert = filterAlertOnly ? !!client.actionNeeded : true;
    const matchesJurisdiction = filterJurisdiction ? true : true; // Jurisdiction not stored in client profile currently
    return matchesSearch && matchesType && matchesAlert && matchesJurisdiction;
  });

  const activePipeline = clients.filter(c => c.status !== 'completed').length;
  const attentionRequired = clients.filter(c => !!c.actionNeeded).length;
  const completedThisMonth = clients.filter(c => c.status === 'completed').length;
  const averageTurnaround = "4.2 Days";

  const handleExportCSV = () => {
    const headers = ["ID", "Email", "Package", "Status", "Progress", "Submitted At", "Action Needed"];
    const rows = filteredClients.map(c => [
      c.id, c.email, c.package.name, c.status, c.progress.toString(), c.submittedAt || '', c.actionNeeded || 'None'
    ]);
    const csvContent = "data:text/csv;charset=utf-8," 
      + headers.join(",") + "\\n" 
      + rows.map(e => e.join(",")).join("\\n");
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "master_log.csv");
    document.body.appendChild(link);
    link.click();
    link.remove();
  };
"""
content = re.sub(r'const filteredClients = clients\.filter\(client => \{.*?\n  \}\);', new_filter_logic.strip(), content, flags=re.DOTALL)

# 4. App Status Controller
app_status_html = """
                <div className="flex items-center space-x-2">
                  <select
                    value={selectedClient.status}
                    onChange={(e) => moveClient(selectedClient.id, e.target.value as any)}
                    className="px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg text-xs font-bold text-gray-700 outline-none hover:bg-gray-100 transition-colors focus:ring-2 focus:ring-brand-500"
                  >
                    {stages.map(s => <option key={s.id} value={s.id}>{s.label}</option>)}
                  </select>
"""
content = content.replace('<div className="flex items-center space-x-2">\n                  <button onClick={() => setShowFlagModal(true)}', app_status_html + '                  <button onClick={() => setShowFlagModal(true)}')

# 5. Document Management & Business Details & Delete bottom status control
old_smart_badge_to_content = r'\{/\* Verified ID Smart Badge \*/\}.*?\{/\* Dynamically Loaded CAC Detail Forms \*/\}'
new_smart_badge_to_content = """
              {/* Document Management Header */}
              <div className="px-6 py-4 bg-gray-50 border-b border-gray-100 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                <div className="flex flex-col space-y-2">
                  {selectedClient.intakeData.idScanCompleted && (
                    <div className="flex items-center">
                      <CheckCircle2 className="w-4 h-4 mr-1.5 text-green-600" />
                      <span className="text-xs font-semibold text-gray-700 mr-2">National ID Verified:</span>
                      <a href={selectedClient.intakeData.scannedIdUrl || '#'} target="_blank" rel="noreferrer" className="text-[10px] bg-brand-100 hover:bg-brand-200 text-brand-900 px-2 py-0.5 rounded font-extrabold cursor-pointer transition-colors border border-brand-200">
                        {selectedClient.intakeData.scannedIdName || 'ID_NIN_CARD.pdf'}
                      </a>
                    </div>
                  )}
                  {selectedClient.intakeData.ngoDetails?.utilityBillUrl && (
                     <div className="flex items-center">
                       <CheckCircle2 className="w-4 h-4 mr-1.5 text-green-600" />
                       <span className="text-xs font-semibold text-gray-700 mr-2">Utility Bill:</span>
                       <a href="#" target="_blank" rel="noreferrer" className="text-[10px] bg-brand-100 hover:bg-brand-200 text-brand-900 px-2 py-0.5 rounded font-extrabold cursor-pointer transition-colors border border-brand-200">
                         {selectedClient.intakeData.ngoDetails.utilityBillUrl}
                       </a>
                     </div>
                  )}
                </div>
                <button className="flex shrink-0 items-center px-4 py-2 bg-white border border-gray-200 text-gray-700 text-xs font-bold rounded-xl hover:bg-gray-50 transition-colors shadow-sm">
                  <Download className="w-4 h-4 mr-1.5" /> Download Document Bundle
                </button>
              </div>

              <div className="flex-1 overflow-y-auto bg-gray-50 p-6 space-y-6">
                
                {/* Top-Level Business Data Section */}
                <div className="bg-white p-5 rounded-2xl border border-gray-200 shadow-sm">
                  <h4 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3 pb-2 border-b border-gray-100 flex items-center">
                    <Briefcase className="w-4 h-4 mr-1.5" /> Business Details
                  </h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <span className="text-xs text-gray-500 block mb-1">Proposed Names</span>
                      <ol className="list-decimal pl-4 text-sm font-bold text-gray-900">
                        {(selectedClient.intakeData.enterpriseDetails?.proposedNames || 
                          selectedClient.intakeData.companyDetails?.proposedNames || 
                          selectedClient.intakeData.ngoDetails?.proposedNames || []).map((name, i) => name ? <li key={i}>{name}</li> : null)}
                      </ol>
                    </div>
                    <div>
                      <span className="text-xs text-gray-500 block mb-1">Nature of Business / Objectives</span>
                      <p className="text-sm font-medium text-gray-800">
                        {selectedClient.intakeData.enterpriseDetails?.natureOfBusiness || 
                         selectedClient.intakeData.companyDetails?.objectsOfMemorandum?.join(', ') || 
                         selectedClient.intakeData.ngoDetails?.mission || 'N/A'}
                      </p>
                    </div>
                    <div className="md:col-span-2">
                      <span className="text-xs text-gray-500 block mb-1">Principal Business Address</span>
                      <p className="text-sm font-medium text-gray-800">
                        {(() => {
                          const addr = selectedClient.intakeData.enterpriseDetails?.businessAddress || 
                                       selectedClient.intakeData.ngoDetails?.officeAddress ||
                                       selectedClient.intakeData.companyDetails?.witness?.address; // Fallback
                          if (addr && addr.houseNumber) return `${addr.houseNumber} ${addr.streetName}, ${addr.city}, ${addr.lga}, ${addr.state} State`;
                          return 'N/A';
                        })()}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Dynamically Loaded CAC Detail Forms */}
"""
content = re.sub(old_smart_badge_to_content, new_smart_badge_to_content.strip(), content, flags=re.DOTALL)

old_status_footer = r'\{/\* Status Control Footer in Details \*/\}.*?</button>\s*</div>\s*</div>'
content = re.sub(old_status_footer, '', content, flags=re.DOTALL)

# 6. Global Top Sections (Metrics, Filter, Export, Notification)
top_layout_old = r'<main className="flex-1 flex overflow-hidden">\s*\{/\* Kanban Board \*/\}\s*<div className={`flex-1 overflow-x-auto p-6 \$\{selectedClient \? \'hidden lg:block\' : \'block\'\}`\}>'
top_layout_new = """
      <main className="flex-1 flex flex-col overflow-hidden">
        {/* High-Level Metrics Strip */}
        <div className="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between z-10 relative">
          <div className="flex items-center space-x-6">
            <div className="flex flex-col">
              <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1 flex items-center"><Activity className="w-3.5 h-3.5 mr-1" /> Active Pipeline</span>
              <span className="text-xl font-bold text-gray-900">{activePipeline}</span>
            </div>
            <div className="h-8 w-px bg-gray-200"></div>
            <div className="flex flex-col">
              <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1 flex items-center"><AlertCircle className="w-3.5 h-3.5 mr-1 text-red-500" /> Attention Required</span>
              <span className="text-xl font-bold text-red-600">{attentionRequired}</span>
            </div>
            <div className="h-8 w-px bg-gray-200"></div>
            <div className="flex flex-col">
              <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1 flex items-center"><CheckCircle2 className="w-3.5 h-3.5 mr-1 text-green-500" /> Completed This Month</span>
              <span className="text-xl font-bold text-gray-900">{completedThisMonth}</span>
            </div>
            <div className="h-8 w-px bg-gray-200"></div>
            <div className="flex flex-col">
              <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1 flex items-center"><Clock className="w-3.5 h-3.5 mr-1 text-blue-500" /> Average Turnaround</span>
              <span className="text-xl font-bold text-gray-900">{averageTurnaround}</span>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <button onClick={handleExportCSV} className="flex items-center px-4 py-2 bg-white border border-gray-200 text-gray-700 text-sm font-bold rounded-xl hover:bg-gray-50 transition-colors shadow-sm">
              <Download className="w-4 h-4 mr-2" /> Export Master Log
            </button>
            <div className="relative">
              <button onClick={() => setShowActivityFeed(!showActivityFeed)} className="p-2 border border-gray-200 rounded-xl bg-white text-gray-600 hover:bg-gray-50 relative">
                <Bell className="w-5 h-5" />
                <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-brand-500 rounded-full border border-white"></span>
              </button>
              <AnimatePresence>
                {showActivityFeed && (
                  <motion.div 
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: 10 }}
                    className="absolute right-0 mt-2 w-80 bg-white rounded-xl shadow-2xl border border-gray-100 z-50 overflow-hidden"
                  >
                    <div className="px-4 py-3 border-b border-gray-100 bg-gray-50">
                      <h3 className="text-sm font-bold text-gray-900">Recent Activity</h3>
                    </div>
                    <div className="max-h-64 overflow-y-auto">
                      <div className="px-4 py-3 border-b border-gray-50 text-sm text-gray-700 flex items-start">
                        <div className="w-2 h-2 bg-brand-500 rounded-full mt-1.5 mr-2 shrink-0"></div>
                        <p>Client <span className="font-bold">John Doe</span> has completed their initial ID Scan.</p>
                      </div>
                      <div className="px-4 py-3 border-b border-gray-50 text-sm text-gray-700 flex items-start">
                        <div className="w-2 h-2 bg-brand-500 rounded-full mt-1.5 mr-2 shrink-0"></div>
                        <p>Client <span className="font-bold">Acme Ltd</span> has updated their blurry passport photo in response to your flag.</p>
                      </div>
                      <div className="px-4 py-3 border-b border-gray-50 text-sm text-gray-700 flex items-start">
                        <div className="w-2 h-2 bg-green-500 rounded-full mt-1.5 mr-2 shrink-0"></div>
                        <p>New submission received for <span className="font-bold">Global Ventures</span>.</p>
                      </div>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </div>
        </div>

        {/* Kanban Board Container */}
        <div className="flex-1 flex overflow-hidden">
          <div className={`flex-1 overflow-x-auto p-6 ${selectedClient ? 'hidden lg:block' : 'block'}`}>
"""
content = re.sub(top_layout_old, top_layout_new.strip(), content, flags=re.DOTALL)

old_filter_row = r'<button className="p-2 border border-gray-200 rounded-lg bg-white text-gray-600 hover:bg-gray-50">\s*<Filter className="w-4 h-4" />\s*</button>'
new_filter_row = """
              <div className="relative">
                <button onClick={() => setShowFilters(!showFilters)} className={`p-2 border rounded-lg transition-colors flex items-center space-x-1 ${showFilters || filterType || filterJurisdiction || filterAlertOnly ? 'bg-brand-50 border-brand-200 text-brand-700' : 'bg-white border-gray-200 text-gray-600 hover:bg-gray-50'}`}>
                  <Filter className="w-4 h-4" />
                  <ChevronDown className="w-3 h-3" />
                </button>
                <AnimatePresence>
                  {showFilters && (
                    <motion.div 
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: 10 }}
                      className="absolute right-0 mt-2 w-64 bg-white rounded-xl shadow-2xl border border-gray-100 z-50 p-4 space-y-4"
                    >
                      <div>
                        <label className="block text-xs font-bold text-gray-700 mb-1.5 uppercase tracking-wider">Jurisdiction</label>
                        <select value={filterJurisdiction} onChange={e => setFilterJurisdiction(e.target.value)} className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm outline-none focus:border-brand-500">
                          <option value="">All Regions</option>
                          <option value="NG">Nigeria (CAC)</option>
                          <option value="US">United States</option>
                          <option value="UK">United Kingdom</option>
                        </select>
                      </div>
                      <div>
                        <label className="block text-xs font-bold text-gray-700 mb-1.5 uppercase tracking-wider">Entity Type</label>
                        <select value={filterType} onChange={e => setFilterType(e.target.value)} className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm outline-none focus:border-brand-500">
                          <option value="">All Types</option>
                          <option value="corporate">Corporate / LTD</option>
                          <option value="enterprise">Business Name</option>
                          <option value="ngo">NGO / Association</option>
                        </select>
                      </div>
                      <div className="flex items-center justify-between pt-2 border-t border-gray-100">
                        <label className="text-xs font-bold text-gray-700">Show Alerts Only</label>
                        <button 
                          onClick={() => setFilterAlertOnly(!filterAlertOnly)}
                          className={`w-10 h-5 rounded-full relative transition-colors ${filterAlertOnly ? 'bg-red-500' : 'bg-gray-300'}`}
                        >
                          <div className={`w-3.5 h-3.5 bg-white rounded-full absolute top-0.5 transition-transform ${filterAlertOnly ? 'left-6' : 'left-1'}`}></div>
                        </button>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
"""
content = re.sub(old_filter_row, new_filter_row.strip(), content)

with open('src/pages/AdminHubPage.tsx', 'w') as f:
    f.write(content)

