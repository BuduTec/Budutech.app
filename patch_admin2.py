import re

with open('src/pages/AdminHubPage.tsx', 'r') as f:
    content = f.read()

# 1. Imports
content = content.replace("import { Download, Bell, ChevronDown, Activity, Clock, BarChart2, \n  Search", "import { Download, Bell, ChevronDown, Activity, Clock, BarChart2, UploadCloud, ToggleLeft, ToggleRight, \n  Search")

# 2. State
state_insert = """
  const [notifyClient, setNotifyClient] = useState(true);
"""
content = re.sub(r'(const \[showFilters, setShowFilters\] = useState\(false\);\n)', r'\1' + state_insert, content)

# 3. Status/Payment/Notify controllers
old_controls = r'<div className="flex items-center space-x-2">\s*<select\s*value=\{selectedClient.status\}\s*onChange=\{.*?\}\s*className="px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg text-xs font-bold text-gray-700 outline-none hover:bg-gray-100 transition-colors focus:ring-2 focus:ring-brand-500"\s*>\s*\{stages\.map\(s => <option key=\{s\.id\} value=\{s\.id\}>\{s\.label\}</option>\)\}\s*</select>\s*<button onClick=\{.*?\} className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors border border-transparent hover:border-red-100" title="Flag Issue">\s*<MessageSquareWarning className="w-5 h-5" />\s*</button>\s*<button onClick=\{handleCopyData\} className="flex items-center px-4 py-2 bg-gray-900 text-white text-xs font-bold rounded-xl hover:bg-gray-800 transition-colors shadow-sm uppercase tracking-wide">\s*<Copy className="w-4 h-4 mr-1\.5" /> Smart Copy\s*</button>\s*</div>'

new_controls = """
                <div className="flex flex-wrap items-center justify-end gap-2 mt-2 sm:mt-0">
                  <button 
                    onClick={() => {
                      const current = selectedClient.paymentStatus || 'pending';
                      const next = current === 'pending' ? 'partially_paid' : current === 'partially_paid' ? 'fully_paid' : 'pending';
                      updateClient(selectedClient.id, { paymentStatus: next });
                      setSelectedClient({ ...selectedClient, paymentStatus: next });
                    }}
                    className={`px-3 py-1.5 rounded-full text-[10px] font-bold uppercase tracking-wider transition-colors border ${
                      selectedClient.paymentStatus === 'fully_paid' 
                        ? 'bg-green-100 text-green-800 border-green-200'
                        : selectedClient.paymentStatus === 'partially_paid'
                        ? 'bg-orange-100 text-orange-800 border-orange-200'
                        : 'bg-yellow-100 text-yellow-800 border-yellow-200'
                    }`}
                  >
                    {selectedClient.paymentStatus === 'fully_paid' ? 'Fully Paid' : selectedClient.paymentStatus === 'partially_paid' ? 'Partially Paid' : 'Pending Payment'}
                  </button>

                  <div className="flex items-center space-x-2 bg-gray-50 border border-gray-200 rounded-lg px-2 py-1.5 relative group cursor-pointer" onClick={() => setNotifyClient(!notifyClient)}>
                    <span className="text-[10px] font-bold text-gray-500 uppercase tracking-wider">Notify</span>
                    {notifyClient ? <ToggleRight className="w-5 h-5 text-brand-500" /> : <ToggleLeft className="w-5 h-5 text-gray-400" />}
                  </div>

                  <select
                    value={selectedClient.status}
                    onChange={(e) => {
                       moveClient(selectedClient.id, e.target.value as any);
                       if (notifyClient) {
                         alert(`Simulated alert: Status update sent to ${selectedClient.email}`);
                       }
                    }}
                    className="px-3 py-1.5 bg-gray-50 border border-gray-200 rounded-lg text-xs font-bold text-gray-700 outline-none hover:bg-gray-100 transition-colors focus:ring-2 focus:ring-brand-500"
                  >
                    {stages.map(s => <option key={s.id} value={s.id}>{s.label}</option>)}
                  </select>

                  <button onClick={() => setShowFlagModal(true)} className="p-1.5 text-red-600 hover:bg-red-50 rounded-lg transition-colors border border-transparent hover:border-red-100" title="Flag Issue">
                    <MessageSquareWarning className="w-5 h-5" />
                  </button>
                  <button onClick={handleCopyData} className="flex items-center px-3 py-1.5 bg-gray-900 text-white text-xs font-bold rounded-xl hover:bg-gray-800 transition-colors shadow-sm uppercase tracking-wide">
                    <Copy className="w-4 h-4 mr-1.5" /> Smart Copy
                  </button>
                </div>
"""
content = re.sub(old_controls, new_controls.strip(), content, flags=re.DOTALL)

# 4. Final Deliverables
old_dynamic_forms = r'\{/\* Dynamically Loaded CAC Detail Forms \*/\}\s*\{renderClientDetailContent\(selectedClient\)\}'
new_dynamic_forms = """
                {/* Dynamically Loaded CAC Detail Forms */}
                {renderClientDetailContent(selectedClient)}

                {/* FINAL APPROVED DOCUMENTS Upload Zone */}
                <div className="bg-white p-5 rounded-2xl border border-gray-200 shadow-sm mt-6">
                  <h4 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3 pb-2 border-b border-gray-100 flex items-center">
                    <UploadCloud className="w-4 h-4 mr-1.5" /> Final Approved Documents
                  </h4>
                  <p className="text-[10px] text-gray-500 mb-4">
                    Upload finished registry documents here (CAC Certificate, Status Report, MEMART, TIN). These will be instantly pushed to the client's dashboard.
                  </p>
                  
                  {selectedClient.deliverables && selectedClient.deliverables.length > 0 && (
                    <div className="space-y-2 mb-4">
                      {selectedClient.deliverables.map((doc, idx) => (
                        <div key={idx} className="flex items-center justify-between p-2 bg-gray-50 rounded-lg border border-gray-100">
                           <div className="flex items-center space-x-2">
                             <FileText className="w-4 h-4 text-brand-500" />
                             <span className="text-xs font-bold text-gray-700">{doc.name}</span>
                           </div>
                           <span className="text-[10px] text-gray-400">{doc.date}</span>
                        </div>
                      ))}
                    </div>
                  )}

                  <div className="border-2 border-dashed border-gray-200 rounded-xl p-6 flex flex-col items-center justify-center bg-gray-50 hover:bg-brand-50 hover:border-brand-300 transition-colors cursor-pointer group" onClick={() => {
                     const newDoc = { id: Date.now().toString(), name: 'CAC_Certificate_Final.pdf', url: '#', date: new Date().toLocaleDateString() };
                     const updatedDeliverables = [...(selectedClient.deliverables || []), newDoc];
                     updateClient(selectedClient.id, { deliverables: updatedDeliverables });
                     setSelectedClient({ ...selectedClient, deliverables: updatedDeliverables });
                     alert("Document uploaded and synced to client dashboard.");
                  }}>
                    <div className="w-10 h-10 bg-white rounded-full flex items-center justify-center shadow-sm mb-3 group-hover:scale-110 transition-transform">
                      <UploadCloud className="w-5 h-5 text-gray-400 group-hover:text-brand-500 transition-colors" />
                    </div>
                    <span className="text-xs font-bold text-gray-700">Drag & drop files or click to browse</span>
                    <span className="text-[10px] text-gray-400 mt-1">PDF, JPG, PNG up to 10MB</span>
                  </div>
                </div>
"""
content = re.sub(old_dynamic_forms, new_dynamic_forms.strip(), content, flags=re.DOTALL)

with open('src/pages/AdminHubPage.tsx', 'w') as f:
    f.write(content)

