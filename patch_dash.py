import re

with open('src/pages/DashboardPage.tsx', 'r') as f:
    content = f.read()

# 1. Imports
content = content.replace("import { AlertCircle, FileText, CheckCircle2, ChevronRight, Download, Activity, Clock } from 'lucide-react';", 
"import { AlertCircle, FileText, CheckCircle2, ChevronRight, Download, Activity, Clock, CreditCard, Award, UploadCloud, MessageCircle } from 'lucide-react';")

# 2. Steps update
content = content.replace(
"""const steps = [
  { id: 'intake', name: 'Intake Forms', description: 'Provide corporate details' },
  { id: 'review', name: 'Review', description: 'Admin reviewing data' },
  { id: 'filed', name: 'Filed with Registry', description: 'Processing at CAC' },
  { id: 'completed', name: 'Completed', description: 'Certificates Ready' },
];""",
"""const steps = [
  { id: 'intake', name: 'Submitted', description: 'Application forms received' },
  { id: 'review', name: 'In Review', description: 'Admin reviewing data' },
  { id: 'filed', name: 'Filed with Registry', description: 'Processing at CAC' },
  { id: 'completed', name: 'Completed', description: 'Certificates Ready' },
];""")

# 3. Component state & mock documents -> retrieve from store
state_update = """
  const { user, selectedPackage, clients } = useAppStore();

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  const clientProfile = clients.find(c => c.email === user.email);
  const applicationStatus = clientProfile?.status || 'intake';
  const actionNeeded = clientProfile?.actionNeeded;
  const primaryName = clientProfile?.intakeData?.enterpriseDetails?.proposedNames?.[0] || 
                      clientProfile?.intakeData?.companyDetails?.proposedNames?.[0] || 
                      clientProfile?.intakeData?.ngoDetails?.proposedNames?.[0] || 
                      'your application';
"""
content = re.sub(r'const \{ user, selectedPackage, applicationStatus, actionNeeded \} = useAppStore\(\);\s*if \(\!user\) \{\s*return <Navigate to="/login" replace \/>;\s*\}\s*// Find current step index', state_update.strip() + '\n\n  // Find current step index', content)

# 4. Action Banner Update
action_banner_old = r'<Link \s*to="/intake" \s*className="whitespace-nowrap px-6 py-2.5 bg-red-600 hover:bg-red-700 text-white rounded-xl font-medium text-sm transition-colors shadow-sm"\s*>\s*Update Application\s*</Link>'
action_banner_new = """
            <label className="whitespace-nowrap px-6 py-2.5 bg-red-600 hover:bg-red-700 text-white rounded-xl font-medium text-sm transition-colors shadow-sm cursor-pointer flex items-center">
              <UploadCloud className="w-4 h-4 mr-2" /> Upload Replacement File
              <input type="file" className="hidden" onChange={() => alert('File uploaded successfully. Admin will be notified.')} />
            </label>
"""
content = re.sub(action_banner_old, action_banner_new.strip(), content)

# 5. Greeting Update
greeting_old = r'<h1 className="heading-font text-3xl font-bold text-gray-900 mb-2">Welcome back, \{user.email.split\(\'@\'\)\[0\]\}</h1>\s*<p className="text-gray-600">Track your application progress and access your corporate documents securely.</p>'
greeting_new = """
          <h1 className="heading-font text-3xl font-bold text-gray-900 mb-2">Welcome back, {user.email.split('@')[0]}.</h1>
          <p className="text-gray-600">Here is the status of <span className="font-bold">{primaryName}</span>.</p>
"""
content = re.sub(greeting_old, greeting_new.strip(), content)

# 6. Document Vault
vault_old = r'\{/\* Document Vault \*/\}.*?(?=\{/\* Quick Summary \*/\})'
vault_new = """
            {/* Document Vault */}
            <div className="bg-white rounded-3xl shadow-sm border border-gray-200 p-8">
              <div className="flex items-center justify-between mb-8">
                <h2 className="heading-font text-xl font-bold text-gray-900 flex items-center">
                  <FileText className="w-5 h-5 mr-2 text-brand-500" /> Secure Document Vault
                </h2>
              </div>
              
              <div className="space-y-8">
                {/* Official Approved Documents */}
                <div>
                  <h3 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-4 flex items-center">
                    <Award className="w-4 h-4 mr-1.5 text-brand-500" /> Official Approved Documents
                  </h3>
                  {clientProfile?.deliverables && clientProfile.deliverables.length > 0 ? (
                    <div className="grid gap-4">
                      {clientProfile.deliverables.map((doc, idx) => (
                        <div key={idx} className="flex items-center justify-between p-4 rounded-xl border border-brand-200 bg-brand-50/50 transition-colors">
                          <div className="flex items-center">
                            <div className="w-10 h-10 rounded-lg flex items-center justify-center mr-4 bg-brand-100 text-brand-600 shadow-sm border border-brand-200">
                              <FileText className="w-5 h-5" />
                            </div>
                            <div>
                              <p className="font-bold text-sm text-gray-900">{doc.name}</p>
                              <p className="text-xs text-gray-500 mt-0.5">{doc.date}</p>
                            </div>
                          </div>
                          <a href={doc.url} download className="p-2 text-brand-600 hover:bg-brand-100 rounded-lg transition-colors border border-transparent hover:border-brand-200" title="Download">
                            <Download className="w-5 h-5" />
                          </a>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="p-6 rounded-xl border border-dashed border-gray-200 bg-gray-50 text-center">
                      <Clock className="w-6 h-6 text-gray-400 mx-auto mb-2" />
                      <p className="text-sm text-gray-500 font-medium">Your official documents will appear here once approved.</p>
                    </div>
                  )}
                </div>

                {/* Your Submissions */}
                <div>
                  <h3 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-4 flex items-center">
                    <UploadCloud className="w-4 h-4 mr-1.5" /> Your Submissions
                  </h3>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    {clientProfile?.intakeData?.scannedIdName && (
                      <div className="flex items-center p-3 rounded-lg border border-gray-100 bg-gray-50">
                        <FileText className="w-4 h-4 text-gray-400 mr-2" />
                        <span className="text-xs font-medium text-gray-700 truncate" title={clientProfile.intakeData.scannedIdName}>{clientProfile.intakeData.scannedIdName}</span>
                      </div>
                    )}
                    {clientProfile?.intakeData?.ngoDetails?.utilityBillUrl && (
                      <div className="flex items-center p-3 rounded-lg border border-gray-100 bg-gray-50">
                        <FileText className="w-4 h-4 text-gray-400 mr-2" />
                        <span className="text-xs font-medium text-gray-700 truncate" title={clientProfile.intakeData.ngoDetails.utilityBillUrl}>{clientProfile.intakeData.ngoDetails.utilityBillUrl}</span>
                      </div>
                    )}
                    {(!clientProfile?.intakeData?.scannedIdName && !clientProfile?.intakeData?.ngoDetails?.utilityBillUrl) && (
                      <p className="text-xs text-gray-500">No documents uploaded.</p>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div className="space-y-8">
"""
content = re.sub(vault_old, vault_new.strip() + '\n\n', content, flags=re.DOTALL)


# 7. Invoice & Payment Status and Support Link
right_col_old = r'\{/\* Quick Summary \*/\}.*?(?=</main>)'
right_col_new = """
            {/* Invoice & Payment Status */}
            <div className="bg-gray-900 text-white rounded-3xl p-8 shadow-xl">
              <h3 className="heading-font font-bold text-lg mb-6 text-gray-100 flex items-center">
                <CreditCard className="w-5 h-5 mr-2 text-gray-400" /> Invoice & Payment
              </h3>
              <div className="space-y-6">
                <div className="flex justify-between items-center border-b border-gray-800 pb-4">
                  <div>
                    <p className="text-gray-400 text-sm mb-1">Service Package</p>
                    <p className="font-medium">{clientProfile?.package?.name || selectedPackage?.name || 'Not selected'}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-gray-400 text-sm mb-1">Total</p>
                    <p className="font-medium text-lg">₦{((clientProfile?.package?.price || selectedPackage?.price) || 0).toLocaleString()}</p>
                  </div>
                </div>
                <div>
                  <p className="text-gray-400 text-sm mb-2">Payment Status</p>
                  {clientProfile?.paymentStatus === 'fully_paid' ? (
                     <div className="flex items-center text-green-400 bg-green-400/10 w-fit px-3 py-1.5 rounded-full font-bold text-xs uppercase tracking-wider">
                       <CheckCircle2 className="w-4 h-4 mr-1.5" /> Payment Complete
                     </div>
                  ) : clientProfile?.paymentStatus === 'partially_paid' ? (
                     <div className="flex items-center text-orange-400 bg-orange-400/10 w-fit px-3 py-1.5 rounded-full font-bold text-xs uppercase tracking-wider">
                       <Clock className="w-4 h-4 mr-1.5" /> Partially Paid
                     </div>
                  ) : (
                     <div className="flex items-center text-yellow-400 bg-yellow-400/10 w-fit px-3 py-1.5 rounded-full font-bold text-xs uppercase tracking-wider">
                       <AlertCircle className="w-4 h-4 mr-1.5" /> Pending Payment
                     </div>
                  )}
                </div>
                {clientProfile?.paymentStatus !== 'fully_paid' ? (
                  <button className="w-full py-3 bg-brand-500 hover:bg-brand-600 text-white rounded-xl font-bold text-sm transition-colors shadow-lg shadow-brand-500/25 mt-2">
                    Pay Outstanding Balance
                  </button>
                ) : (
                  <button className="w-full py-3 bg-gray-800 hover:bg-gray-700 text-white rounded-xl font-bold text-sm transition-colors mt-2 flex items-center justify-center">
                    <Download className="w-4 h-4 mr-2" /> Download Receipt
                  </button>
                )}
              </div>
            </div>

            {/* Support Card */}
            <div className="bg-brand-50 rounded-3xl p-8 border border-brand-100 text-center">
              <div className="w-12 h-12 bg-white rounded-full flex items-center justify-center mx-auto mb-4 shadow-sm text-brand-600">
                <MessageCircle className="w-6 h-6" />
              </div>
              <h3 className="heading-font font-bold text-gray-900 mb-2">Need Help?</h3>
              <p className="text-sm text-gray-600 mb-6">Our corporate consultants are available to assist you with your application via WhatsApp.</p>
              <a href="https://wa.me/2348000000000" target="_blank" rel="noreferrer" className="flex items-center justify-center w-full py-3 bg-[#25D366] text-white rounded-xl font-bold text-sm hover:bg-[#20bd5a] transition-colors shadow-sm">
                <MessageCircle className="w-4 h-4 mr-2" /> Chat on WhatsApp
              </a>
            </div>
          </div>
        </div>
"""
content = re.sub(right_col_old, right_col_new.strip() + '\n      ', content, flags=re.DOTALL)

with open('src/pages/DashboardPage.tsx', 'w') as f:
    f.write(content)

