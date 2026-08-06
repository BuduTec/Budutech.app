const WHATSAPP_NUMBER = "2349027591229";
const GOOGLE_PROFILE_URL = "https://g.page/r/CZvbDAseY6mOEBM";
const GOOGLE_REVIEW_URL = "https://g.page/r/CZvbDAseY6mOEBM/review";

const packagePrices = {
  "Business Name": { Basic: "₦34,999", Premium: "₦45,000" },
  "Limited Company": { Basic: "₦65,000", Premium: "₦84,999" },
  "NGO / Incorporated Trustees": { Basic: "₦130,000", Premium: "₦180,000" }
};

function track(eventName, data = {}) {
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push({ event: eventName, ...data });

  if (typeof window.fbq === "function") {
    try { window.fbq("trackCustom", eventName, data); } catch (e) {}
  }
  if (typeof window.gtag === "function") {
    try { window.gtag("event", eventName, data); } catch (e) {}
  }
}

function whatsappUrl(service, packageName = "") {
  const price = packagePrices[service]?.[packageName] || "";
  const packageLine = packageName ? `${packageName} Package${price ? ` (${price})` : ""}` : "Not yet selected";
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
    const data = await res.json();
    const reviews = data.reviews || data || [];
    const total = reviews.reduce((sum, r) => sum + (Number(r.rating) || 5), 0);

    if (avg && reviews.length) avg.textContent = (total / reviews.length).toFixed(1);
    if (count) count.textContent = String(reviews.length);

    if (grid) {
      grid.innerHTML = reviews.map(r => {
        const stars = "★★★★★".slice(0, Math.max(0, Number(r.rating) || 5));
        return `
          <article class="review-card">
            <div class="stars">${stars}</div>
            <p>“${r.text || ""}”</p>
            <strong>${r.name || "Google Review"}</strong>
            <small>${r.source || "Google Business Profile"}</small>
          </article>
        `;
      }).join("");
    }
  } catch (e) {
    if (grid) {
      grid.innerHTML = '<article class="review-card"><div class="stars">★★★★★</div><p>Paste your real Google Business Profile reviews in reviews.json.</p><strong>BuduTech</strong><small>Google Business Profile</small></article>';
    }
  }
}

document.addEventListener("DOMContentLoaded", () => {
  updateMainWhatsApp();
  loadReviews();
  track("LandingPageViewed");

  document.getElementById("service")?.addEventListener("change", updateMainWhatsApp);
  document.getElementById("package")?.addEventListener("change", updateMainWhatsApp);

  document.querySelectorAll("[data-wa]").forEach(btn => {
    btn.addEventListener("click", () => {
      const s = btn.dataset.service || document.getElementById("service")?.value || "CAC Registration";
      const p = btn.dataset.package || document.getElementById("package")?.value || "";
      btn.href = whatsappUrl(s, p);
      track("Lead", { service: s, package: p, price: packagePrices[s]?.[p] || "" });
    });
  });

  document.querySelectorAll(".package-card .btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const s = btn.dataset.service || "";
      const p = btn.dataset.package || "";
      track("PackageSelected", { service: s, package: p, price: packagePrices[s]?.[p] || "" });
    });
  });

  document.querySelectorAll("details").forEach(d => {
    d.addEventListener("toggle", () => {
      if (d.open) track("FAQOpened", { question: d.querySelector("summary")?.textContent || "" });
    });
  });

  let scrolled = false;
  window.addEventListener("scroll", () => {
    if (!scrolled && window.scrollY > window.innerHeight) {
      scrolled = true;
      track("Scroll50Percent");
    }
  });

  setTimeout(() => track("Stayed30Seconds"), 30000);

  document.querySelectorAll("a[href^='tel:']").forEach(a => {
    a.addEventListener("click", () => track("PhoneCallClick"));
  });
});
