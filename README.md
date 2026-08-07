# BuduTech.app — Plan B Precision Patch

This bundle applies the agreed fixes to `BuduTec/Budutech.app`.

Changes:
1. `budutech.app` becomes the single canonical domain.
2. Meta Pixel `1915513149012218` is preserved. WhatsApp intent now fires Meta's standard `Lead` event plus a custom `WhatsAppLead` event.
3. The supplied founder photo replaces `YOUR PHOTO`.
4. Review summary uses the official GBP figures: 4.7 rating / 20 reviews.
5. Stale relative review dates such as “5 days ago” are removed rather than converted into invented dates. Existing absolute dates remain.
6. A trust/proof section adds RC 9626592, 50+ clients, 3+ years, and the 4.7/20 Google proof point.

Apply from the repository root:

    python apply_budutech_patch.py

The script validates important markers and stops if the repository structure differs materially.

Important: the repo currently contains 17 genuine review records, while the official GBP total is 20. The patch does not invent the missing three reviews. It displays the official 20-review total and keeps the 17 genuine reviews as featured reviews.

No Google Analytics or Clarity ID is invented because those IDs were not supplied.
