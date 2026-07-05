import re

with open('src/pages/IntakeFormPage.tsx', 'r') as f:
    content = f.read()

# Fix status to intake
old_submit = """      // Create new client record & update applicationStatus
      const newProfile = {
        id: `client-${Date.now()}`,
        email: user.email,
        package: selectedPackage,
        status: 'review' as const,
        progress: 100,
        actionNeeded: null,
        submittedAt: new Date().toISOString().split('T')[0],
        intakeData: intakeData,
      };

      addClient(newProfile);
      setApplicationStatus('review');"""

new_submit = """      // Create new client record & update applicationStatus
      const newProfile = {
        id: `client-${Date.now()}`,
        email: user.email,
        package: selectedPackage,
        status: 'intake' as const,
        progress: 100,
        actionNeeded: null,
        submittedAt: new Date().toISOString().split('T')[0],
        intakeData: intakeData,
      };

      addClient(newProfile);
      setApplicationStatus('intake');"""

content = content.replace(old_submit, new_submit)

with open('src/pages/IntakeFormPage.tsx', 'w') as f:
    f.write(content)
