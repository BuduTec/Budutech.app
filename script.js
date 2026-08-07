const WHATSAPP_NUMBER = "2349027591229";
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
