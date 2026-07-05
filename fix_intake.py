with open('src/pages/IntakeFormPage.tsx', 'r') as f:
    content = f.read()

# Replace import
content = content.replace("import SignatureCanvas from 'react-signature-canvas';", "import SignatureCanvas, { SignatureCanvasRef } from '../components/SignatureCanvas';")

# Replace ref type
content = content.replace("useRef<SignatureCanvas>(null)", "useRef<SignatureCanvasRef>(null)")
content = content.replace("canvasRef: React.RefObject<SignatureCanvas | null>", "canvasRef: React.RefObject<SignatureCanvasRef | null>")

with open('src/pages/IntakeFormPage.tsx', 'w') as f:
    f.write(content)
