(function () {
  "use strict";

  function pdHref() {
    var path = (location.pathname || "").replace(/index\.html$/i, "");
    var parts = path.split("/").filter(Boolean);
    var i = parts.indexOf("AngelGranit");
    var depth = i >= 0 ? parts.length - i - 1 : parts.length;
    if (depth <= 0) return "personalnye-dannye/";
    return "../".repeat(depth) + "personalnye-dannye/";
  }

  function ensureCheckbox(form) {
    if (!form || form.querySelector("[name='pd_consent']")) return;
    var href = pdHref();
    var label = document.createElement("label");
    label.className = "pd-consent";
    label.style.cssText = "display:flex;gap:.5rem;align-items:flex-start;margin:0.75rem 0;font-size:0.82rem;line-height:1.4;color:#9a907e;";
    label.innerHTML =
      '<input type="checkbox" name="pd_consent" value="1" required style="width:auto;margin-top:.2rem;flex-shrink:0" />' +
      '<span>Согласен на обработку персональных данных (имя, телефон) и на связь через WhatsApp (серверы вне РК). ' +
      '<a href="' + href + '">Политика конфиденциальности</a></span>';
    var actions = form.querySelector(".form-actions, .pcat-modal__submit");
    if (actions && actions.parentNode === form) form.insertBefore(label, actions);
    else if (actions && actions.classList.contains("pcat-modal__submit")) form.insertBefore(label, actions);
    else form.appendChild(label);
  }

  function bindForm(form) {
    if (!form || form.dataset.pdBound === "1") return;
    form.dataset.pdBound = "1";
    ensureCheckbox(form);
    form.addEventListener(
      "submit",
      function (e) {
        var box = form.querySelector("[name='pd_consent']");
        if (box && !box.checked) {
          e.preventDefault();
          e.stopImmediatePropagation();
          box.focus();
          alert("Отметьте согласие на обработку персональных данных.");
        }
      },
      true
    );
  }

  function injectFooter() {
    var href = pdHref();
    document.querySelectorAll("footer").forEach(function (footer) {
      if (footer.querySelector("[data-pd-link]")) return;
      var p = document.createElement("p");
      p.style.cssText = "margin:.7rem 0 0;font-size:.82rem;";
      p.innerHTML =
        '<a data-pd-link href="' + href + '">Политика конфиденциальности</a>';
      footer.appendChild(p);
    });
  }

  function init() {
    injectFooter();
    ["form", "pcat-form", "seo-lead-form"].forEach(function (id) {
      var f = document.getElementById(id);
      if (f) bindForm(f);
    });
    document.querySelectorAll("form").forEach(function (form) {
      if (form.querySelector('input[name="phone"], input[type="tel"]')) bindForm(form);
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
