const WHATSAPP_NUMBER = "2349027591229";
const GOOGLE_PROFILE_URL = "https://g.page/r/CZvbDAseY6mOEBM";
const GOOGLE_REVIEW_URL = "https://g.page/r/CZvbDAseY6mOEBM/review";
const ATTRIBUTION_STORAGE_KEY = "budutechAttribution";
const ATTRIBUTION_KEYS = [
  "utm_source",
  "utm_medium",
  "utm_campaign",
  "utm_content",
  "utm_term",
  "fbclid",
  "gclid"
];

const packagePrices = {
  "Business Name": { Basic: "₦34,999", Premium: "₦45,000" },
  "Limited Company": { Basic: "₦65,000", Premium: "₦84,999" },
  "NGO / Incorporated Trustees": { Basic: "₦130,000", Premium: "₦180,000" }
};

function sanitizeAttributionValue(value = "") {
  return String(value).replace(/[^\w\-./:+% ]/g, "").trim().slice(0, 150);
}

function parseStoredAttribution() {
  try {
    const parsed = JSON.parse(localStorage.getItem(ATTRIBUTION_STORAGE_KEY) || "{}");
    return parsed && typeof parsed === "object" ? parsed : {};
  } catch (e) {
    return {};
  }
}

function captureAttribution() {
  const params = new URLSearchParams(window.location.search);
  const current = {};

  ATTRIBUTION_KEYS.forEach((key) => {
    const value = sanitizeAttributionValue(params.get(key) || "");
    if (value) current[key] = value;
  });

  if (Object.keys(current).length === 0) return parseStoredAttribution();

  const stored = parseStoredAttribution();
  const merged = {
    ...stored,
    ...current,
    landing_path: window.location.pathname,
    captured_at: new Date().toISOString()
  };

  try {
    localStorage.setItem(ATTRIBUTION_STORAGE_KEY, JSON.stringify(merged));
  } catch (e) {}

  return merged;
}

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
  const attribution = parseStoredAttribution();
  const attributionDetails = ATTRIBUTION_KEYS
    .filter((key) => attribution[key])
    .map((key) => `${key}: ${attribution[key]}`)
    .join("\n");
  const attributionBlock = attributionDetails
    ? `\n\nLead attribution:\n${attributionDetails}`
    : "";

  const message =
`Hello BuduTech, I came from your CAC registration page and I'd like to proceed with my registration.

Registration type: ${service}
Package: ${packageLine}

Please confirm the requirements and next steps for me.${attributionBlock}`;

  return `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(message)}`;
}

function buildAttributionPayload() {
  const attribution = parseStoredAttribution();
  const payload = {};

  ATTRIBUTION_KEYS.forEach((key) => {
    if (attribution[key]) payload[key] = attribution[key];
  });

  return payload;
}

function populateServiceOptions() {
  const serviceSelect = document.getElementById("service");
  if (!serviceSelect) return;

  const services = Object.keys(packagePrices);
  const currentValue = serviceSelect.value;

  serviceSelect.innerHTML = '<option value="">Select registration type</option>';
  services.forEach((service) => {
    const option = document.createElement("option");
    option.value = service;
    option.textContent = service;
    serviceSelect.appendChild(option);
  });

  if (services.includes(currentValue)) {
    serviceSelect.value = currentValue;
  }
}

function populatePackageOptions(service) {
  const packageSelect = document.getElementById("package");
  if (!packageSelect) return;

  const packages = packagePrices[service] || {};
  const packageNames = Object.keys(packages);
  const currentValue = packageSelect.value;

  packageSelect.innerHTML = '<option value="">Select package</option>';
  packageSelect.disabled = packageNames.length === 0;

  packageNames.forEach((pkg) => {
    const option = document.createElement("option");
    option.value = pkg;
    option.textContent = `${pkg} (${packages[pkg]})`;
    packageSelect.appendChild(option);
  });

  if (packageNames.includes(currentValue)) {
    packageSelect.value = currentValue;
  } else {
    packageSelect.value = "";
  }
}

function updateSelectedPriceDisplay(service, pkg) {
  const selectedPrice = document.getElementById("selectedPrice");
  if (!selectedPrice) return;

  if (!service) {
    selectedPrice.textContent = "Select your registration type to view package pricing.";
    return;
  }
  if (!pkg) {
    selectedPrice.textContent = "Select a package to continue to WhatsApp.";
    return;
  }

  const price = packagePrices[service]?.[pkg] || "";
  selectedPrice.textContent = price
    ? `${service} • ${pkg} package: ${price}`
    : `${service} • ${pkg} package selected`;
}

function updateMainWhatsApp() {
  const service = document.getElementById("service")?.value || "";
  const pkg = document.getElementById("package")?.value || "";
  const button = document.getElementById("mainWhatsApp");
  const headerButton = document.getElementById("headerWhatsapp");
  const stickyButton = document.querySelector(".sticky-wa");
  const url = whatsappUrl(service, pkg);
  const canProceed = Boolean(service && pkg);
  const fallbackUrl = "#packages";

  if (button) button.href = canProceed ? url : fallbackUrl;
  if (headerButton) headerButton.href = canProceed ? url : fallbackUrl;
  if (stickyButton) stickyButton.href = canProceed ? url : fallbackUrl;
  if (button) button.setAttribute("aria-disabled", String(!canProceed));

  updateSelectedPriceDisplay(service, pkg);
}

function trackLead(service, pkg) {
  const price = packagePrices[service]?.[pkg] || "";
  const attributionPayload = buildAttributionPayload();

  track("PackageSelected", { service, package: pkg, price });

  track("Lead", {
    content_name: "WhatsApp Registration Lead",
    service,
    package: pkg,
    value: numericPrice(price),
    currency: "NGN",
    ...attributionPayload
  });

  track("WhatsAppLead", { service, package: pkg, price, ...attributionPayload });
}

function applyDynamicPricesToCards() {
  document.querySelectorAll("[data-price-service][data-price-package]").forEach((node) => {
    const service = node.getAttribute("data-price-service") || "";
    const pkg = node.getAttribute("data-price-package") || "";
    const price = packagePrices[service]?.[pkg];
    if (price) node.textContent = price;
  });
}

function setupBackToTop() {
  const backToTop = document.getElementById("backToTop");
  if (!backToTop) return;

  const toggleBackToTop = () => {
    backToTop.classList.toggle("visible", window.scrollY > 400);
  };

  window.addEventListener("scroll", toggleBackToTop, { passive: true });
  toggleBackToTop();

  backToTop.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
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
  captureAttribution();
  populateServiceOptions();
  populatePackageOptions("");
  applyDynamicPricesToCards();
  updateMainWhatsApp();
  loadReviews();
  setupBackToTop();

  track("ViewContent", {
    content_name: "CAC Registration Landing Page",
    content_category: "Business Registration"
  });

  document.getElementById("service")?.addEventListener("change", () => {
    const service = document.getElementById("service")?.value || "";
    populatePackageOptions(service);
    updateMainWhatsApp();
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

  document.getElementById("mainWhatsApp")?.addEventListener("click", (event) => {
    const service = document.getElementById("service")?.value || "";
    const pkg = document.getElementById("package")?.value || "";
    if (!service || !pkg) {
      event.preventDefault();
      return;
    }
    trackLead(service, pkg);
  });

  document.getElementById("headerWhatsapp")?.addEventListener("click", () => {
    const service = document.getElementById("service")?.value || "";
    const pkg = document.getElementById("package")?.value || "";
    if (service && pkg) trackLead(service, pkg);
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
      if (service && pkg) trackLead(service, pkg);
      else track("WhatsAppLead", { service, package: pkg, price });
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
