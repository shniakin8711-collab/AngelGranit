(function () {
  function qs(sel, root) { return (root || document).querySelector(sel); }
  function qsa(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }

  var nav = qs("[data-site-nav]");
  if (!nav) return;

  var toggle = qs("[data-nav-toggle]", nav);
  var menu = qs(".site-nav__menu", nav);
  if (menu && !menu.id) menu.id = "site-nav-menu";
  if (toggle && menu && !toggle.getAttribute("aria-controls")) {
    toggle.setAttribute("aria-controls", menu.id);
  }

  function closeMenu() {
    nav.classList.remove("is-open");
    if (toggle) toggle.setAttribute("aria-expanded", "false");
    qsa("[data-dropdown]", nav).forEach(function (item) {
      item.classList.remove("is-open");
      var btn = qs("button", item);
      if (btn) btn.setAttribute("aria-expanded", "false");
    });
  }

  if (toggle) {
    toggle.addEventListener("click", function () {
      var open = !nav.classList.contains("is-open");
      nav.classList.toggle("is-open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  qsa("[data-dropdown]", nav).forEach(function (item) {
    var btn = qs("button", item);
    if (!btn) return;
    if (!btn.getAttribute("aria-expanded")) btn.setAttribute("aria-expanded", "false");
    btn.addEventListener("click", function (e) {
      e.preventDefault();
      var open = item.classList.contains("is-open");
      qsa("[data-dropdown]", nav).forEach(function (other) {
        other.classList.remove("is-open");
        var ob = qs("button", other);
        if (ob) ob.setAttribute("aria-expanded", "false");
      });
      if (!open) {
        item.classList.add("is-open");
        btn.setAttribute("aria-expanded", "true");
      }
    });
  });

  document.addEventListener("click", function (e) {
    if (!nav.contains(e.target)) closeMenu();
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeMenu();
  });

  var wa = "https://wa.me/77010567667?text=" + encodeURIComponent("Здравствуйте! AngelGranit — нужна консультация.");
  qsa("[data-wa]", document).forEach(function (el) {
    el.href = wa;
    if (!el.getAttribute("rel")) el.setAttribute("rel", "noopener noreferrer");
    if (!el.getAttribute("target")) el.setAttribute("target", "_blank");
  });

  if (!window.__agPdLoader) {
    window.__agPdLoader = true;
    var navScript = document.querySelector('script[src*="nav.js"]');
    var pd = document.createElement("script");
    pd.src = navScript && navScript.src
      ? navScript.src.replace(/nav\.js(\?.*)?$/, "pd-consent.js")
      : "assets/site/pd-consent.js";
    pd.defer = true;
    document.head.appendChild(pd);
  }
})();
