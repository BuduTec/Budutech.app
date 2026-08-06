const WHATSAPP_NUMBER = "2349027591229";
const GOOGLE_PROFILE_URL = "https://g.page/r/CZvbDAseY6mOEBM";

const packagePrices = {
  "Business Name": { Basic: "₦34,999", Premium: "₦45,000" },
  "Limited Company": { Basic: "₦65,000", Premium: "₦84,999" },
  "NGO / Incorporated Trustees": { Basic: "₦130,000", Premium: "₦180,000" }
};

function whatsappUrl(service, packageName = "") {
  const price = packagePrices[service]?.[packageName] || "";
  const packageLine = packageName ? `${packageName} Package${price ? ` (${price})` : ""}` : "Not yet selected";
  const message = `Hello BuduTech, I came from your CAC registration page and I'd like to proceed with my registration.\n\nRegistration type: ${service}\nPackage: ${packageLine}\n\nPlease confirm the requirements and next steps for me.`;
  return `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(message)}`;
}

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

function updateMainWhatsApp() {
  const service = document.getElementById("service")?.value || "Business Name";
  const pkg = document.getElementById("package")?.value || "Basic";
  const button = document.getElementById("mainWhatsApp");
  if (button) button.href = whatsappUrl(service, pkg);
}

async function loadReviews() {
  const grid = document.getElementById("reviewGrid");
  const avg = document.getElementById("reviewAverage");
  const count = document.getElementById("reviewCount");
  const googleLink = document.getElementById("googleProfileLink");

  try {
    const res = await fetch("reviews.json", { cache: "no-store" });
    const data = await res.json();
    const reviews = data.reviews || data || [];
    if (googleLink) googleLink.href = https://g.page/r/CZvbDAseY6mOEBM;

    const total = reviews.reduce((sum, r) => sum + (Number(r.rating) || 5), 0);
    if (avg && reviews.length) avg.textContent = (total / reviews.length).toFixed(1);
    if (count) count.textContent = String(reviews.length);

    grid.innerHTML = reviews.map(r => `
      <article class="review-card">
        <div class="stars">${"★★★★★".slice(0, Math.max(0, Number(r.rating) || 5))}</div>
        <p>“${r.text || ""}”</p>
        <strong>${r.name || "Google Review"}</strong>
        <small>${r.source || "Google Business Profile"}</small>
        ${r.date ? `<small>${r.date}</small>` : ""}
      </article>
    `).join("");
  } catch (e) {
    if (grid) grid.innerHTML = `<article class="review-card"><div class="stars">★★★★★</div><p>Paste your real Google Business Profile reviews in <code>reviews.json</code>.</p><strong>BuduTech</strong><small>Google Business Profile</small></article>`;
  }
}

document.addEventListener("DOMContentLoaded", () => {
  updateMainWhatsApp();
  loadReviews();

  document.getElementById("service")?.addEventListener("change", updateMainWhatsApp);
  document.getElementById("package")?.addEventListener("change", updateMainWhatsApp);

  document.querySelectorAll("[data-wa]").forEach(el => {
    el.addEventListener("click", () => {
      const service = el.dataset.service || document.getElementById("service")?.value || "CAC Registration";
      const pkg = el.dataset.package || document.getElementById("package")?.value || "";
      el.href = whatsappUrl(service, pkg);
      track("Lead", { service, package: pkg, source: "landing_page" });
    });
  });

  document.querySelectorAll(".package-card .btn").forEach(el => {
    el.addEventListener("click", () => {
      const service = el.dataset.service || "";
      const pkg = el.dataset.package || "";
      track("PackageSelected", { service, package: pkg });
    });
  });

  track("PageView");
});
  
