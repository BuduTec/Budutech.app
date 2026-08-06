# BuduTech CAC Landing Page V2

A mobile-first static landing page for BuduTech Services LTD (RC 9626592).

## What's improved in V2

- Clear CAC service selection
- Exact Basic/Premium package pricing and inclusions
- Stronger message-match structure for Facebook traffic
- Customized WhatsApp message based on registration type + package
- WhatsApp number set to `2349027591229`
- 20 FAQ answers designed to reduce repetitive WhatsApp questions
- Mobile sticky WhatsApp CTA
- Conversion event hooks for PageView, PackageSelected and Lead
- Placeholder for genuine client proof and your professional portrait
- No invented testimonials

## Important before launch

1. Replace the `YOUR PHOTO` placeholder in `index.html` with your real professional image.
2. Replace the client-proof placeholder with genuine reviews/screenshots.
3. Add your Meta Pixel base code and Google Tag Manager/Analytics if desired. `script.js` already exposes `dataLayer` and calls `fbq` when available.
4. Review all prices, delivery timelines and package inclusions before publishing.
5. Add Privacy Policy and Terms pages before running paid traffic at scale.

## Deploy on GitHub + Vercel

### GitHub
Create a new repository, upload:
- `index.html`
- `styles.css`
- `script.js`
- `README.md`

### Vercel
Import the GitHub repository into Vercel.
Framework preset: Other / Static.
Build command: leave empty.
Output directory: leave empty or use the repository root.
Deploy.

The site is static and needs no backend.
