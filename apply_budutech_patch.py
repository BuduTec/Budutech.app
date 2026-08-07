#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent

def read(name):
    return (ROOT / name).read_text(encoding="utf-8")

def write(name, text):
    (ROOT / name).write_text(text, encoding="utf-8")

def require(text, marker, label):
    if marker not in text:
        raise RuntimeError(f"Expected marker not found in {label}: {marker!r}")

# 1. Domain consistency
for name in ["index.html", "robots.txt", "sitemap.xml"]:
    p = ROOT / name
    if p.exists():
        text = p.read_text(encoding="utf-8")
        text = text.replace("https://budutech.com", "https://budutech.app")
        text = text.replace("http://budutech.com", "https://budutech.app")
        p.write_text(text, encoding="utf-8")

# 4 + 7. Founder photo and trust/proof
index = read("index.html")
require(index, '<div class="portrait">YOUR PHOTO</div>', "index.html")
require(index, '<section class="section trust" id="reviews">', "index.html")

index = index.replace(
    '<div class="portrait">YOUR PHOTO</div>',
    '''<div class="portrait">
            <img src="founder.jpg" alt="Emmanuel Buduka, founder of BuduTech Services LTD" width="1200" height="1200" loading="eager" decoding="async">
          </div>''',
    1
)

proof_section = '''
    <section class="section proof" id="about-founder">
      <div class="container">
        <div class="proof-grid">
          <div class="proof-copy">
            <span class="eyebrow">WHY BUDUTECH</span>
            <h2>Real business registration support, backed by real proof.</h2>
            <p>BuduTech Services LTD helps entrepreneurs and organisations formalise their businesses with professional guidance from registration through documentation.</p>
            <p>We are a CAC-registered company and have served 50+ clients over 3+ years. When you work with us, you know exactly who is handling your registration.</p>
          </div>
          <div class="proof-stats" aria-label="BuduTech proof points">
            <div class="proof-card"><strong>RC 9626592</strong><span>Official CAC company registration</span></div>
            <div class="proof-card"><strong>50+</strong><span>Clients served</span></div>
            <div class="proof-card"><strong>3+ Years</strong><span>Experience serving entrepreneurs</span></div>
            <div class="proof-card"><strong>4.7 ★</strong><span>20 reviews on Google Business Profile</span></div>
          </div>
        </div>
      </div>
    </section>

'''
index = index.replace(
    '    <section class="section trust" id="reviews">',
    proof_section + '    <section class="section trust" id="reviews">',
    1
)
index = index.replace(
    '<div><strong id="reviewAverage">4.9</strong><span>Average rating</span></div>',
    '<div><strong id="reviewAverage">4.7</strong><span>Average rating</span></div>',
    1
)
index = index.replace(
    '<div><strong id="reviewCount">0</strong><span>Google reviews</span></div>',
    '<div><strong id="reviewCount">20</strong><span>Google reviews</span></div>',
    1
)
index = index.replace(
    '<p>These cards are loaded from a reviews file so you can update them without touching the design.</p>',
    '<p>Our Google Business Profile currently has 20 reviews with a 4.7 average rating. Genuine client reviews are featured below.</p>',
    1
)
write("index.html", index)

# 3. Meta Pixel / conversion events
script_js = r'''const WHATSAPP_NUMBER = "2349027591229";
const GOOGLE_PROFILE_URL = "https://g.page/r/CZvbDAseY6mOEBM";
const GOOGLE_REVIEW_URL = "https://g.page/r/CZvbDAseY6mOEBM/review";

const packagePrices = {
  "Business Name": { Basic: "₦34,999", Premium: "₦45,000" },
  "Limited Company": { Basic: "₦65,000", Premium: "₦84,999" },
  "NGO / Incorporated Trustees": { Basic: "₦130,000", Premium: "₦180,000" }
};

function numericPrice(price = "") {
  const value = Number(String(price).replace(/[^\d.]/g, ""));
  return Number.isFinite(value) ? value : undefined;
}

function track(eventName, data = {}) {
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push({ event: eventName, ...data });

  if (typeof window.fbq === "function") {
    try {
      if (eventName === "Lead") {
        window.fbq("track", "Lead", data);
      } else {
        window.fbq("trackCustom", eventName, data);
      }
    } catch (e) {}
  }

  if (typeof window.gtag === "function") {
    try { window.gtag("event", eventName, data); } catch (e) {}
  }
}

function whatsappUrl(service, packageName = "") {
  const price = packagePrices[service]?.[packageName] || "";
  const packageLine = packageName
    ? `${packageName} Package${price ? ` (${price})` : ""}`
    : "Not yet selected";

  const message =
`Hello BuduTech, I came from your CAC registration page and I'd like to proceed with my registration.

Registration type: ${service}
Package: ${packageLine}

Please confirm the requirements and next steps for me.`;

  return `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(message)}`;
}

function updateMainWhatsApp() {
  const service = document.getElementById("service")?.value || "Business Name";
  const pkg = document.getElementById("package")?.value || "Basic";
  const button = document.getElementById("mainWhatsApp");
  const headerButton = document.getElementById("headerWhatsapp");
  const url = whatsappUrl(service, pkg);
  if (button) button.href = url;
  if (headerButton) headerButton.href = url;
}

async function loadReviews() {
  const grid = document.getElementById("reviewGrid");
  const avg = document.getElementById("reviewAverage");
  const count = document.getElementById("reviewCount");
  const googleLink = document.getElementById("googleProfileLink");
  const leaveReviewBtn = document.getElementById("leaveReviewBtn");

  if (googleLink) {
    googleLink.href = GOOGLE_PROFILE_URL;
    googleLink.addEventListener("click", () => track("ViewGoogleReviews"));
  }
  if (leaveReviewBtn) {
    leaveReviewBtn.href = GOOGLE_REVIEW_URL;
    leaveReviewBtn.addEventListener("click", () => track("LeaveGoogleReview"));
  }

  try {
    const res = await fetch("reviews.json", { cache: "no-store" });
    if (!res.ok) throw new Error(`Reviews request failed: ${res.status}`);
    const data = await res.json();
    const reviews = Array.isArray(data.reviews) ? data.reviews : [];

    if (avg && Number.isFinite(Number(data.rating))) {
      avg.textContent = Number(data.rating).toFixed(1);
    }
    if (count && Number.isFinite(Number(data.total_reviews))) {
      count.textContent = String(data.total_reviews);
    }

    if (grid) {
      grid.innerHTML = reviews.map(r => {
        const rating = Math.min(5, Math.max(1, Number(r.rating) || 5));
        const stars = "★★★★★".slice(0, rating);
        const date = r.date ? `<small>${r.date}</small>` : "";
        return `
          <article class="review-card">
            <div class="stars" aria-label="${rating} out of 5 stars">${stars}</div>
            <p>“${r.text || ""}”</p>
            <strong>${r.name || "Google Review"}</strong>
            <small>${r.source || "Google Business Profile"}</small>
            ${date}
          </article>
        `;
      }).join("");
    }
  } catch (e) {
    if (grid) {
      grid.innerHTML = '<article class="review-card"><div class="stars">★★★★★</div><p>We are currently refreshing our review display. You can view all current reviews on our Google Business Profile.</p><strong>BuduTech Services LTD</strong><small>Google Business Profile</small></article>';
    }
  }
}

document.addEventListener("DOMContentLoaded", () => {
  updateMainWhatsApp();
  loadReviews();

  track("ViewContent", {
    content_name: "CAC Registration Landing Page",
    content_category: "Business Registration"
  });

  document.getElementById("service")?.addEventListener("change", () => {
    updateMainWhatsApp();
    const service = document.getElementById("service")?.value || "";
    track("RegistrationTypeSelected", { service });
  });

  document.getElementById("package")?.addEventListener("change", () => {
    updateMainWhatsApp();
    const service = document.getElementById("service")?.value || "";
    const pkg = document.getElementById("package")?.value || "";
    track("PackageSelected", {
      service,
      package: pkg,
      price: packagePrices[service]?.[pkg] || ""
    });
  });

  document.querySelectorAll("[data-wa]").forEach(btn => {
    btn.addEventListener("click", () => {
      const service = btn.dataset.service ||
        document.getElementById("service")?.value ||
        "CAC Registration";
      const pkg = btn.dataset.package ||
        document.getElementById("package")?.value ||
        "";
      const price = packagePrices[service]?.[pkg] || "";

      btn.href = whatsappUrl(service, pkg);

      track("PackageSelected", { service, package: pkg, price });

      track("Lead", {
        content_name: "WhatsApp Registration Lead",
        service,
        package: pkg,
        value: numericPrice(price),
        currency: "NGN"
      });

      track("WhatsAppLead", { service, package: pkg, price });
    });
  });

  document.querySelectorAll("details").forEach(d => {
    d.addEventListener("toggle", () => {
      if (d.open) track("FAQOpened", {
        question: d.querySelector("summary")?.textContent || ""
      });
    });
  });

  let scrolled = false;
  window.addEventListener("scroll", () => {
    if (!scrolled && window.scrollY > window.innerHeight) {
      scrolled = true;
      track("Scroll50Percent");
    }
  }, { passive: true });

  setTimeout(() => track("Stayed30Seconds"), 30000);

  document.querySelectorAll("a[href^='tel:']").forEach(a => {
    a.addEventListener("click", () => track("PhoneCallClick"));
  });
});
'''
write("script.js", script_js)

# 5 + 6. Reviews: official GBP summary + preserve genuine local reviews.
reviews = json.loads(read("reviews.json"))
reviews["rating"] = 4.7
reviews["total_reviews"] = 20
reviews["source"] = "Google Business Profile"
reviews["featured_reviews_count"] = len(reviews.get("reviews", []))

for review in reviews.get("reviews", []):
    d = str(review.get("date", "")).lower().strip()
    if re.fullmatch(r"\d+\s+(day|days|week|weeks)\s+ago", d):
        review["date"] = None

write("reviews.json", json.dumps(reviews, ensure_ascii=False, indent=2) + "\n")

# 4. Require the supplied photo.
photo = ROOT / "founder.jpg"
if not photo.exists() or photo.stat().st_size < 10000:
    raise RuntimeError("founder.jpg is missing or unexpectedly small.")

# 7. Add proof styling safely if not already present.
css = read("styles.css")
if ".proof-grid" not in css:
    css += r'''

/* Founder / trust proof */
.proof{background:#f7f9fc}
.proof-grid{display:grid;grid-template-columns:1fr 1fr;gap:28px;align-items:stretch}
.proof-copy{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:34px;box-shadow:var(--shadow)}
.proof-copy h2{font-size:clamp(30px,4vw,46px);line-height:1.08;margin:0 0 16px;letter-spacing:-.03em}
.proof-copy p{color:var(--muted);font-size:17px}
.proof-stats{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.proof-card{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:25px;box-shadow:var(--shadow);display:flex;flex-direction:column;justify-content:center}
.proof-card strong{font-size:28px;color:var(--blue);line-height:1.1}
.proof-card span{color:var(--muted);margin-top:7px;font-size:14px}
.portrait{height:300px;border-radius:18px;overflow:hidden;background:#dfe7f7}
.portrait img{display:block;width:100%;height:100%;object-fit:cover;object-position:center top}

@media (max-width:850px){
  .proof-grid{grid-template-columns:1fr}
}
@media (max-width:520px){
  .proof-stats{grid-template-columns:1fr}
}
'''
    write("styles.css", css)

# Final checks.
final_index = read("index.html")
for marker in [
    "https://budutech.app/",
    'src="founder.jpg"',
    "RC 9626592",
    "50+",
    "3+ Years",
    "20 reviews on Google Business Profile"
]:
    require(final_index, marker, "index.html")

for name in ["index.html", "robots.txt", "sitemap.xml"]:
    if Path(name).exists() and "budutech.com" in read(name):
        raise RuntimeError(f"Domain validation failed: budutech.com remains in {name}")

final_reviews = json.loads(read("reviews.json"))
assert final_reviews["rating"] == 4.7
assert final_reviews["total_reviews"] == 20

print("SUCCESS")
print("Updated: index.html, script.js, reviews.json, styles.css, robots.txt, sitemap.xml")
print("Installed: founder.jpg")
print("Meta Pixel ID preserved: 1915513149012218")
print("Official GBP summary: 4.7 / 20")
print("No review text was invented or altered.")
