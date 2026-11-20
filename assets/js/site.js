/* First Medical — small, dependency-free behaviours. */
(function () {
  "use strict";
  var d = document, root = d.documentElement;
  var $$ = function (s, c) { return Array.prototype.slice.call((c || d).querySelectorAll(s)); };

  /* ---------- theme (the initial theme is set inline in <head> to avoid a flash) */
  var themeBtn = d.querySelector("[data-theme-toggle]");
  function syncTheme() {
    if (themeBtn) themeBtn.setAttribute("aria-pressed", String(root.getAttribute("data-theme") === "dark"));
  }
  if (themeBtn) {
    syncTheme();
    themeBtn.addEventListener("click", function () {
      var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try { localStorage.setItem("fm-theme", next); } catch (e) {}
      syncTheme();
    });
  }

  /* ---------- mobile menu */
  var menuBtn = d.querySelector("[data-menu-toggle]"), nav = d.querySelector("[data-nav]");
  function setMenu(open) {
    if (!nav || !menuBtn) return;
    nav.classList.toggle("open", open);
    menuBtn.setAttribute("aria-expanded", String(open));
    d.body.classList.toggle("menu-open", open);
  }
  if (menuBtn) menuBtn.addEventListener("click", function () { setMenu(!nav.classList.contains("open")); });

  /* ---------- services menu: click/keyboard everywhere, hover on desktop pointers */
  var desktopHover = window.matchMedia("(hover: hover) and (min-width: 1101px)");
  $$(".has-mega").forEach(function (li) {
    var btn = li.querySelector("[data-mega-trigger]"), timer, viaHover = false;
    function set(open) { li.classList.toggle("open", open); btn.setAttribute("aria-expanded", String(open)); }
    /* a click right after hover-open keeps the menu open instead of closing it */
    btn.addEventListener("click", function () {
      if (viaHover) { viaHover = false; set(true); } else { set(!li.classList.contains("open")); }
    });
    li.addEventListener("mouseenter", function () {
      if (!desktopHover.matches) return;
      clearTimeout(timer);
      if (!li.classList.contains("open")) { viaHover = true; set(true); }
    });
    li.addEventListener("mouseleave", function () {
      if (desktopHover.matches) { timer = setTimeout(function () { viaHover = false; set(false); }, 160); }
    });
    li.addEventListener("focusout", function (e) { if (desktopHover.matches && !li.contains(e.relatedTarget)) set(false); });
  });
  d.addEventListener("click", function (e) {
    $$(".has-mega.open").forEach(function (li) {
      if (!li.contains(e.target)) { li.classList.remove("open"); li.querySelector("[data-mega-trigger]").setAttribute("aria-expanded", "false"); }
    });
  });
  d.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    $$(".has-mega.open").forEach(function (li) {
      li.classList.remove("open");
      var b = li.querySelector("[data-mega-trigger]"); b.setAttribute("aria-expanded", "false"); b.focus();
    });
    if (nav && nav.classList.contains("open")) { setMenu(false); menuBtn.focus(); }
  });

  /* ---------- product variants (sizes, shapes) */
  $$("[data-variants]").forEach(function (group) {
    var scope = group.closest("[data-product]") || d;
    var img = scope.querySelector("[data-variant-img]");
    $$("[data-src]", group).forEach(function (chip) {
      chip.addEventListener("click", function () {
        $$("[data-src]", group).forEach(function (c) { c.setAttribute("aria-pressed", "false"); });
        chip.setAttribute("aria-pressed", "true");
        if (img) {
          img.src = chip.getAttribute("data-src");
          if (chip.dataset.w) { img.width = +chip.dataset.w; img.height = +chip.dataset.h; }
          if (chip.dataset.alt) img.alt = chip.dataset.alt;
        }
        $$("[data-bind]", scope).forEach(function (el) {
          var v = chip.getAttribute("data-" + el.getAttribute("data-bind"));
          if (v !== null) el.textContent = v;
        });
        var q = scope.querySelector("[data-quote-link]");
        if (q && chip.dataset.key) {
          q.setAttribute("href", q.getAttribute("href").split("?")[0] + "?product=" + encodeURIComponent(scope.getAttribute("data-product")) + "&size=" + encodeURIComponent(chip.dataset.key));
        }
      });
    });
  });

  /* ---------- quote form: composes a WhatsApp message or an email, stores nothing */
  var form = d.querySelector("[data-quote-form]");
  if (form) {
    var params = new URLSearchParams(location.search);
    var prod = params.get("product"), size = params.get("size");
    if (prod && form.elements.product) {
      var opt = form.elements.product.querySelector('option[value="' + prod + '"]');
      if (opt) form.elements.product.value = prod;
    }
    if (size && form.elements.size) form.elements.size.value = size.replace("x", " × ") + " " + (form.getAttribute("data-unit") || "cm");

    var msg = form.querySelector("[data-form-msg]");
    function compose() {
      var lines = [form.getAttribute("data-heading")];
      $$("[data-label]", form).forEach(function (el) {
        var v = el.tagName === "SELECT" ? el.options[el.selectedIndex].text : el.value.trim();
        if (el.tagName === "SELECT" && el.value === "") v = "";
        if (v) lines.push(el.getAttribute("data-label") + ": " + v);
      });
      return lines.join("\n");
    }
    function valid() {
      var name = form.elements.name, prod = form.elements.product, notes = form.elements.notes;
      [name, prod, notes].forEach(function (f) { f.removeAttribute("aria-invalid"); });
      if (!name.value.trim()) { name.setAttribute("aria-invalid", "true"); msg.textContent = form.getAttribute("data-err-name"); name.focus(); return false; }
      if (!prod.value && !notes.value.trim()) { prod.setAttribute("aria-invalid", "true"); msg.textContent = form.getAttribute("data-err-need"); prod.focus(); return false; }
      msg.textContent = ""; return true;
    }
    $$("[data-send]", form).forEach(function (btn) {
      btn.addEventListener("click", function (e) {
        e.preventDefault();
        if (!valid()) return;
        var text = compose(), url;
        if (btn.getAttribute("data-send") === "whatsapp") {
          url = "https://wa.me/" + form.getAttribute("data-wa") + "?text=" + encodeURIComponent(text);
          window.open(url, "_blank", "noopener");
        } else {
          url = "mailto:" + form.getAttribute("data-email") + "?subject=" + encodeURIComponent(form.getAttribute("data-heading")) + "&body=" + encodeURIComponent(text);
          window.location.href = url;
        }
      });
    });
  }

  /* ---------- footer year */
  $$("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
