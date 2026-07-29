(function () {
  "use strict";

  var PHONE = "+77010567667";
  var WA = "https://wa.me/77010567667";
  var PAGE_TITLE = document.title || "AngelGranit";

  function waLink(text) {
    return WA + "?text=" + encodeURIComponent(text);
  }

  document.querySelectorAll("[data-wa-default]").forEach(function (el) {
    if (!el.getAttribute("href") || el.getAttribute("href") === "#") {
      el.setAttribute("href", waLink("Здравствуйте! AngelGranit — нужна консультация по теме: " + PAGE_TITLE));
    }
  });

  var form = document.getElementById("seo-lead-form");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var name = (form.querySelector('[name="name"]') || {}).value || "";
      var phone = (form.querySelector('[name="phone"]') || {}).value || "";
      var service = (form.querySelector('[name="service"]') || {}).value || "";
      var message = (form.querySelector('[name="message"]') || {}).value || "";
      var text = [
        "Заявка с сайта AngelGranit",
        "Страница: " + PAGE_TITLE,
        "Имя: " + name.trim(),
        "Телефон: " + phone.trim(),
        "Услуга: " + service.trim(),
        "Сообщение: " + message.trim()
      ].join("\n");
      window.open(waLink(text), "_blank", "noopener,noreferrer");
    });
  }

  function loadMap(container) {
    if (!container || container.dataset.loaded === "1") return;
    var lat = container.dataset.lat || "43.289921";
    var lng = container.dataset.lng || "76.961065";
    var q = encodeURIComponent("ул. Осетинская, 5а, Алматы");
    var iframe = document.createElement("iframe");
    iframe.title = "Карта Google — офис AngelGranit, ул. Осетинская, 5а, Алматы";
    iframe.loading = "lazy";
    iframe.referrerPolicy = "no-referrer-when-downgrade";
    iframe.allowFullscreen = true;
    iframe.src =
      "https://maps.google.com/maps?q=" +
      lat +
      "," +
      lng +
      "(" +
      q +
      ")&z=16&output=embed";
    container.innerHTML = "";
    container.appendChild(iframe);
    container.dataset.loaded = "1";
  }

  var mapBox = document.getElementById("seo-map");
  var mapBtn = document.getElementById("seo-map-load");
  if (mapBtn && mapBox) {
    mapBtn.addEventListener("click", function () {
      loadMap(mapBox);
      mapBtn.hidden = true;
    });
  }
  if (mapBox && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            loadMap(mapBox);
            if (mapBtn) mapBtn.hidden = true;
            io.disconnect();
          }
        });
      },
      { rootMargin: "200px" }
    );
    io.observe(mapBox);
  }
})();
