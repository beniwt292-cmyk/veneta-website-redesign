/* ===== VENETA measurement layer — MASTER_PLAN §10 ===========================
   Nine events. Three are purpose-built (hd_click, spec_table_view, guide_read);
   finder_complete is fired by the finder in interactive.js through window.vev;
   the rest are declarative, so a new page only has to add data-ev attributes:

     <form data-ev="trade_apply" data-ev-firm_type="designer">
     <a data-ev="spec_download" data-ev-file="dualdrape-spec.pdf">
     <select data-ev-param="products" multiple>      <- collected into the payload

   Custom dimensions page_type / module / category / audience travel as params.
   ========================================================================== */
(function () {
  var body = document.body;
  var PT = body.getAttribute('data-page-type') || '';
  var CAT = body.getAttribute('data-category') || '';

  function send(name, params) {
    var p = params || {};
    if (p.page_type === undefined) p.page_type = PT;
    if (window.gtag) gtag('event', name, p);
  }
  window.vev = send;

  /* ---------- hd_click: every retail handoff ----------------------------- */
  document.addEventListener('click', function (e) {
    var a = e.target.closest('[data-hd]');
    if (!a) return;
    var v = (a.getAttribute('data-hd') || '').split('|');
    send('hd_click', { page_type: v[0] || PT, module: v[1] || '', category: v[2] || '' });
  });

  /* ---------- declarative events ---------------------------------------- */
  function payload(el) {
    var p = {}, i, at = el.attributes;
    for (i = 0; i < at.length; i++) {
      if (at[i].name.indexOf('data-ev-') === 0 && at[i].name !== 'data-ev-param') {
        p[at[i].name.slice(8).replace(/-/g, '_')] = at[i].value;
      }
    }
    el.querySelectorAll('[data-ev-param]').forEach(function (f) {
      var k = f.getAttribute('data-ev-param');
      if (f.multiple) {
        p[k] = [].slice.call(f.selectedOptions).map(function (o) { return o.value || o.text; });
      } else if (f.type === 'checkbox') {
        p[k] = f.checked;
      } else {
        p[k] = f.value;
      }
    });
    return p;
  }

  document.querySelectorAll('form[data-ev]').forEach(function (f) {
    f.addEventListener('submit', function () { send(f.getAttribute('data-ev'), payload(f)); });
  });

  document.addEventListener('click', function (e) {
    var el = e.target.closest('[data-ev]');
    if (!el || el.tagName === 'FORM') return;
    send(el.getAttribute('data-ev'), payload(el));
  });

  /* ---------- swatch_select --------------------------------------------- */
  document.querySelectorAll('.sw2-grid').forEach(function (grid) {
    grid.addEventListener('click', function (e) {
      var s = e.target.closest('.sw2');
      if (!s) return;
      var n = s.querySelector('b');
      send('swatch_select', { category: grid.getAttribute('data-category') || CAT,
                              material: n ? n.textContent.trim() : '' });
    });
  });

  /* ---------- spec_table_view: 50% visible for 2s ----------------------- */
  var tables = document.querySelectorAll('.spec2');
  if (tables.length && window.IntersectionObserver) {
    var so = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        var t = e.target;
        if (e.isIntersecting) {
          t.__dwell = setTimeout(function () {
            so.unobserve(t);
            send('spec_table_view', { category: t.getAttribute('data-category') || CAT });
          }, 2000);
        } else {
          clearTimeout(t.__dwell);
        }
      });
    }, { threshold: 0.5 });
    tables.forEach(function (t) { so.observe(t); });
  }

  /* ---------- guide_read: 75% scroll depth on a guide -------------------- */
  if (PT === 'guide') {
    var slug = location.pathname.split('/').pop().replace(/\.html$/, '') || 'index';
    var fired = false;
    var check = function () {
      if (fired) return;
      var h = document.documentElement.scrollHeight - innerHeight;
      if (h > 0 && (scrollY / h) >= 0.75) {
        fired = true;
        removeEventListener('scroll', check);
        send('guide_read', { slug: slug, category: CAT });
      }
    };
    addEventListener('scroll', check, { passive: true });
  }
})();
