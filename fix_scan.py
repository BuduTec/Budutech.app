import re

with open('src/pages/IntakeFormPage.tsx', 'r') as f:
    content = f.read()

# Fix handleIdUploadSimulate
old_sim = """  const handleIdUploadSimulate = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return;
    const file = e.target.files[0];
    
    if (file.size > 5 * 1024 * 1024) {
      alert("Security Block: File size exceeds 5MB limit.");
      return;
    }
    if (!file.type.match(/image\/(jpeg|png|jpg)|application\/pdf/)) {
      alert("Security Block: Invalid file type. Only standard images and PDFs are allowed.");
      return;
    }
    
    setScanStatus('scanning');
    setScanProgress(10);
    setError(null);

    const interval = setInterval(() => {
      setScanProgress(p => {
        if (p >= 100) {
          clearInterval(interval);
          return 100;
        }
        return p + 15;
      });
    }, 300);

    setTimeout(() => {
      setScanStatus('review');
      
      const ocrExtracted = {
        fileName: file.name,
        firstName: 'Emmanuel',
        surname: 'Elubuduka',
        otherName: 'Kaene',
        dob: '1995-07-04',
        gender: 'Male',
        phone: '08149204958',
        email: user.email,
        nin: '29485710294',
      };
      setOcrTempData(ocrExtracted);
    }, 2400);
  };"""

new_sim = """  const handleIdUploadSimulate = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return;
    const file = e.target.files[0];
    
    if (file.size > 5 * 1024 * 1024) {
      setError("File size exceeds 5MB limit.");
      return;
    }
    if (!file.type.match(/image\/(jpeg|png)|application\/pdf/)) {
      setError("Invalid file type. Only standard images (JPG, PNG) and PDFs are allowed.");
      return;
    }
    
    setScanStatus('scanning');
    setScanProgress(10);
    setError(null);

    const interval = setInterval(() => {
      setScanProgress(p => {
        if (p >= 100) {
          clearInterval(interval);
          return 100;
        }
        return p + 15;
      });
    }, 300);

    setTimeout(() => {
      // SMART REJECTION SIMULATION
      const isRandomImage = !file.name.toLowerCase().match(/(id|nin|passport|license|slip|doc|cert|scan|simulated)/);
      if (isRandomImage) {
        setScanStatus('error');
      } else {
        setScanStatus('review');
        const ocrExtracted = {
          fileName: file.name,
          firstName: 'Emmanuel',
          surname: 'Elubuduka',
          otherName: 'Kaene',
          dob: '1995-07-04',
          gender: 'Male',
          phone: '08149204958',
          email: user.email,
          nin: '29485710294',
        };
        setOcrTempData(ocrExtracted);
      }
    }, 2400);
  };"""

content = content.replace(old_sim, new_sim)

# Add scanStatus error to useState
content = content.replace("useState<'idle' | 'scanning' | 'review' | 'completed'>('idle')", "useState<'idle' | 'scanning' | 'review' | 'completed' | 'error'>('idle')")

# Add error rendering state to smart-scan
old_scan_render = """            {scanStatus === 'scanning' ? ("""
new_scan_render = """            {scanStatus === 'error' ? (
              <div className="bg-red-50 rounded-2xl p-8 border border-red-100 mb-6 flex flex-col items-center">
                <div className="w-12 h-12 bg-red-100 text-red-600 rounded-full flex items-center justify-center mb-3">
                  <AlertCircle className="w-6 h-6" />
                </div>
                <p className="font-bold text-red-800 text-sm">Invalid document detected.</p>
                <p className="text-xs text-red-600 mt-1 max-w-sm text-center">Please upload a clear image of a valid National ID, Driver's License, or Passport.</p>
                
                <label className="mt-6 inline-flex items-center px-6 py-2 bg-red-600 hover:bg-red-700 text-white text-xs font-semibold rounded-xl transition-colors cursor-pointer shadow-sm">
                  <Camera className="w-4 h-4 mr-1.5" /> Try Again
                  <input type="file" accept="image/jpeg,image/png,application/pdf" className="hidden" onChange={handleIdUploadSimulate} />
                </label>
              </div>
            ) : scanStatus === 'scanning' ? ("""

content = content.replace(old_scan_render, new_scan_render)

old_handle_next = """  const handleNext = () => {
    setError(null);
    const stepId = steps[currentStep].id;

    // --- Validation Logic ---
    if (stepId === 'smart-scan') {
      if (!intakeData.idScanCompleted) {
        setError('Please upload your primary ID to proceed, or use the simulated smart-fill scan.');
        return;
      }
    }"""

new_handle_next = """  const handleNext = () => {
    setError(null);
    const stepId = steps[currentStep].id;

    // --- Validation Logic ---
    if (stepId === 'smart-scan') {
      if (scanStatus === 'review' && ocrTempData) {
        handleAcceptOcr();
      } else if (!intakeData.idScanCompleted && scanStatus !== 'completed') {
        setError('Please upload your primary ID to proceed, or use the simulated smart-fill scan.');
        return;
      }
    }"""

content = content.replace(old_handle_next, new_handle_next)

content = content.replace('accept="image/*,application/pdf"', 'accept="image/jpeg,image/png,application/pdf"')

with open('src/pages/IntakeFormPage.tsx', 'w') as f:
    f.write(content)

