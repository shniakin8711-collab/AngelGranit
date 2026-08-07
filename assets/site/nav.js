(function () {
  function qs(sel, root) { return (root || document).querySelector(sel); }
  function qsa(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }

  var nav = qs("[data-site-nav]");
  if (!nav) return;

  var toggle = qs("[data-nav-toggle]", nav);
  if (toggle) {
    toggle.addEventListener("click", function () {
      nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", nav.classList.contains("is-open") ? "true" : "false");
    });
  }

  qsa("[data-dropdown]", nav).forEach(function (item) {
    var btn = qs("button", item);
    if (!btn) return;
    btn.addEventListener("click", function (e) {
      e.preventDefault();
      var open = item.classList.contains("is-open");
      qsa("[data-dropdown]", nav).forEach(function (other) { other.classList.remove("is-open"); });
      if (!open) item.classList.add("is-open");
    });
  });

  document.addEventListener("click", function (e) {
    if (!nav.contains(e.target)) {
      qsa("[data-dropdown]", nav).forEach(function (item) { item.classList.remove("is-open"); });
    }
  });

  var wa = "https://wa.me/77010567667?text=" + encodeURIComponent("Здравствуйте! AngelGranit — нужна консультация.");
  qsa("[data-wa]", document).forEach(function (el) { el.href = wa; });
})();
