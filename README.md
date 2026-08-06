# BuduTech CAC Registration Landing Page

A lightweight, mobile-first landing page for Facebook/Instagram traffic.

## Files

- `index.html` — page structure and copy
- `styles.css` — responsive styling
- `script.js` — WhatsApp CTA, pre-filled messages and tracking hooks

## Before publishing

1. Open `script.js`.
2. Replace:
   `const WHATSAPP_NUMBER = "234XXXXXXXXXX";`
   with the real BuduTech WhatsApp number in international format, without `+` or spaces.
3. Replace the three sample testimonials in `index.html` with genuine client reviews.
4. Replace the portrait placeholder with a real professional image if desired.
5. Add your real Meta Pixel ID in `index.html`.
6. Review all service descriptions, pricing and claims before launch.

## GitHub

Create a new repository and upload these three files to the root.

## Vercel

Import the GitHub repository into Vercel.

Framework preset: Other / Static Site.

Build command: leave blank.

Output directory: `.`

Deploy.

## Custom domain

In Vercel:
Project → Settings → Domains → Add your domain.

Vercel will provide the DNS records required for your domain registrar.

## Recommended ad tracking

Use UTM parameters in your Facebook ads, for example:

`?utm_source=facebook&utm_medium=paid_social&utm_campaign=cac_business_name&utm_content=video_01`

Then later connect your analytics/CRM so you can compare:

Ad spend → landing-page visitors → WhatsApp clicks → qualified leads → payments → completed registrations.

## Important

Do not publish the sample testimonials. Replace them with genuine reviews.
Do not publish the placeholder WhatsApp number.
Do not publish pricing unless the displayed prices are current and accurate.
