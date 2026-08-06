const WHATSAPP_NUMBER = "2349027591229";

const packagePrices = {
  "Business Name": { Basic: "₦34,999", Premium: "₦45,000" },
  "Limited Company": { Basic: "₦65,000", Premium: "₦84,999" },
  "NGO / Incorporated Trustees": { Basic: "₦130,000", Premium: "₦180,000" }
};

function whatsappUrl(service, packageName = "") {
  const price = packagePrices[service]?.[packageName] || "";
  const packageLine = packageName
    ? `${packageName} Package${price ? ` (${price})` : ""}`
    : "Not yet selected";

  const message = `Hello BuduTech, I came from your CAC registration page and I'd like to proceed with my registration.

Registration type: ${service}
Package: ${packageLine}

Please confirm the requirements and next steps for me.`;

  return `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(message)}`;
}

function track(eventName, data = {}) {
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push({ event: eventName, ...data });
  if (typeof window.fbq === "function") {
    window.fbq("trackCustom", eventName, data);
  }
}

function updateMainWhatsApp() {
  const service = document.getElementById("service")?.value || "Business Name";
  const pkg = document.getElementById("package")?.value || "Basic";
  const button = document.getElementById("mainWhatsApp");
  if (button) button.href = whatsappUrl(service, pkg);
}

document.addEventListener("DOMContentLoaded", () => {
  updateMainWhatsApp();

  document.getElementById("service")?.addEventListener("change", updateMainWhatsApp);
  document.getElementById("package")?.addEventListener("change", updateMainWhatsApp);

  document.querySelectorAll("[data-service][data-package]").forEach(el => {
    el.addEventListener("click", () => {
      const service = el.dataset.service;
      const pkg = el.dataset.package;
      const serviceSelect = document.getElementById("service");
      const packageSelect = document.getElementById("package");
      if (serviceSelect && packagePrices[service]) serviceSelect.value = service;
      if (packageSelect && (pkg === "Basic" || pkg === "Premium")) packageSelect.value = pkg;
      updateMainWhatsApp();
      track("PackageSelected", { service, package: pkg });
    });
  });

  document.querySelectorAll("[data-wa]").forEach(el => {
    el.addEventListener("click", () => {
      const service = el.dataset.service || document.getElementById("service")?.value || "CAC Registration";
      const pkg = el.dataset.package || document.getElementById("package")?.value || "";
      el.href = whatsappUrl(service, pkg);
      track("Lead", { service, package: pkg, source: "landing_page" });
    });
  });

  document.getElementById("mainWhatsApp")?.addEventListener("click", () => {
    const service = document.getElementById("service")?.value || "CAC Registration";
    const pkg = document.getElementById("package")?.value || "";
    track("Lead", { service, package: pkg, source: "main_cta" });
  });

  track("PageView");
});
                          
