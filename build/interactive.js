/* ===== VENETA interactive layer =============================================
   Product finder, live grid filtering, product mega menu and site search.
   Data below is injected at build time.
   ========================================================================== */
(function () {
  var D = /*__DATA__*/{};
  var P = D.products || {}, ROOM = D.room || {}, NEED = D.need || {}, LOOK = D.look || {}, LIFT = D.lift || {};

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  function cardHTML(slug, reason) {
    var p = P[slug]; if (!p) return '';
    return '<a class="card rev in" href="' + slug + '.html">' +
      '<div class="ph"><img src="assets/img/' + p.img + '" alt="' + esc(p.name) + ' shown in a styled room" loading="lazy"></div>' +
      '<h3>' + p.name + '</h3>' +
      '<p class="desc">' + (reason || p.desc) + '</p>' +
      '<p class="price">' + p.price + '</p>' +
      '<div class="badges">' + p.badges.slice(0, 2).map(function (b, i, a) {
        return '<span class="badge">' + b + '</span>';
      }).join('') + '</div></a>';
  }

  /* ---------- scoring ---------------------------------------------------- */
  function rank(maps) {
    var score = {};
    maps.forEach(function (list) {
      (list || []).forEach(function (slug, i) {
        score[slug] = (score[slug] || 0) + (3 - i > 0 ? 3 - i : 0.5);
      });
    });
    return Object.keys(score).sort(function (a, b) { return score[b] - score[a]; });
  }

  function val(id) { var e = document.getElementById(id); return e ? e.value : ''; }

  /* ---------- homepage / finder page ------------------------------------ */
  function runFinder(outId, withLift) {
    var out = document.getElementById(outId); if (!out) return;
    var room = val('f-room'), need = val('f-need');
    var maps = [ROOM[room], NEED[need]];
    if (withLift) { maps.push(LIFT[val('f-lift')]); } else { maps.push(LOOK[val('f-look')]); }
    var order = rank(maps).slice(0, 3);
    var w = parseFloat(val('f-w')) || 0;
    var wide = w >= 96;
    if (wide) { order = order.filter(function (s) { return P[s] && P[s].wide; }).concat(order.filter(function (s) { return !(P[s] && P[s].wide); })).slice(0, 3); }

    var head = '<p class="eyebrow">Your shortlist</p><h2 class="fout-h">' +
      esc(room) + ' &middot; ' + esc(need).toLowerCase() + '</h2>' +
      '<p class="tnote" style="margin:0 0 26px">Ranked for this combination. Order swatches before you commit to a colour.</p>';
    var reasons = { 0: 'Best match for what you described.', 1: 'Close second, different look.', 2: 'Worth a look if the first two miss.' };
    out.innerHTML = head + '<div class="cards">' + order.map(function (s, i) {
      return cardHTML(s, reasons[i]);
    }).join('') + '</div>' +
      (wide ? '<div class="callout" style="margin-top:28px"><p><strong>At 96&quot; and wider</strong> a single blind gets heavy. We have kept the shortlist to lines built for wide openings.</p></div>' : '');
    out.hidden = false;
    out.setAttribute('aria-live', 'polite');
    if (window.vev) {
      window.vev('finder_complete', {
        room: room, priority: need,
        look: withLift ? val('f-lift') : val('f-look')
      });
    }
    if (window.__finderScroll) { out.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
  }

  var homeBtn = document.querySelector('[data-analytics="finder-submit"]');
  if (homeBtn) {
    homeBtn.addEventListener('click', function () { window.__finderScroll = true; runFinder('fout', false); });
  }
  var pf = document.getElementById('pf-form');
  if (pf) {
    pf.addEventListener('submit', function (e) { e.preventDefault(); window.__finderScroll = true; runFinder('pf-out', true); });
    ['f-room', 'f-need', 'f-lift'].forEach(function (id) {
      var el = document.getElementById(id);
      if (el) el.addEventListener('change', function () { window.__finderScroll = false; runFinder('pf-out', true); });
    });
    window.__finderScroll = false;
    runFinder('pf-out', true);
  }

  /* ---------- live grid filtering --------------------------------------- */
  var chipRow = document.querySelector('.chips[data-filter]');
  if (chipRow) {
    var grid = document.getElementById('filter-grid');
    var count = document.getElementById('filter-count');
    var reset = document.getElementById('filter-reset');
    var apply = function () {
      var on = [].slice.call(chipRow.querySelectorAll('.chip[aria-pressed="true"]')).map(function (c) { return c.dataset.tag; });
      var shown = 0;
      [].slice.call(grid.querySelectorAll('.card')).forEach(function (card) {
        var tags = (card.dataset.tags || '').split(' ');
        var ok = on.every(function (t) { return tags.indexOf(t) > -1; });
        card.hidden = !ok;
        if (ok) shown++;
      });
      count.textContent = shown === 8 ? 'All 8 products' : shown + (shown === 1 ? ' product' : ' products');
      reset.hidden = on.length === 0;
      grid.classList.toggle('empty', shown === 0);
    };
    chipRow.addEventListener('click', function (e) {
      var c = e.target.closest('.chip'); if (!c) return;
      c.setAttribute('aria-pressed', c.getAttribute('aria-pressed') === 'true' ? 'false' : 'true');
      apply();
    });
    reset.addEventListener('click', function () {
      chipRow.querySelectorAll('.chip').forEach(function (c) { c.setAttribute('aria-pressed', 'false'); });
      apply();
    });
    apply();
  }

  /* ---------- product mega menu ----------------------------------------- */
  var mm = document.querySelector('.hasmenu');
  if (mm) {
    var t;
    var open = function (v) { mm.classList.toggle('open', v); mm.querySelector('a').setAttribute('aria-expanded', v ? 'true' : 'false'); };
    mm.addEventListener('mouseenter', function () { clearTimeout(t); open(true); });
    mm.addEventListener('mouseleave', function () { t = setTimeout(function () { open(false); }, 160); });
    mm.addEventListener('focusin', function () { open(true); });
    mm.addEventListener('focusout', function (e) { if (!mm.contains(e.relatedTarget)) open(false); });
    addEventListener('keydown', function (e) { if (e.key === 'Escape') open(false); });
  }

  /* ---------- site search ----------------------------------------------- */
  var sBtn = document.querySelectorAll('[data-search-open]');
  var sPanel = document.getElementById('search');
  if (sPanel && sBtn.length) {
    var input = document.getElementById('search-q');
    var res = document.getElementById('search-res');
    var openS = function () {
      sPanel.classList.add('on'); document.body.style.overflow = 'hidden';
      input.value = ''; render(''); setTimeout(function () { input.focus(); }, 60);
    };
    var closeS = function () { sPanel.classList.remove('on'); document.body.style.overflow = ''; };
    var render = function (q) {
      var idx = window.VENETA_INDEX || [];
      q = q.trim().toLowerCase();
      var hits = q.length < 2 ? idx.slice(0, 8) : idx.map(function (p) {
        var hay = (p.t + ' ' + p.d).toLowerCase();
        var s = 0;
        if (p.t.toLowerCase().indexOf(q) > -1) s += 10;
        q.split(/\s+/).forEach(function (w) { if (hay.indexOf(w) > -1) s += 2; });
        return { p: p, s: s };
      }).filter(function (h) { return h.s > 0; }).sort(function (a, b) { return b.s - a.s; }).slice(0, 8).map(function (h) { return h.p; });

      res.innerHTML = hits.length
        ? '<p class="search-lbl">' + (q.length < 2 ? 'Popular pages' : hits.length + ' result' + (hits.length === 1 ? '' : 's')) + '</p>' +
          hits.map(function (p) {
            return '<a href="' + p.u + '"><strong>' + esc(p.t) + '</strong><span>' + esc(p.d) + '</span></a>';
          }).join('')
        : '<p class="search-lbl">Nothing matched. Try “measure”, “blackout”, “patio” or “warranty”.</p>';
    };
    sBtn.forEach(function (b) { b.addEventListener('click', openS); });
    sPanel.addEventListener('click', function (e) { if (e.target === sPanel || e.target.closest('[data-search-close]')) closeS(); });
    input.addEventListener('input', function () { render(input.value); });
    addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeS();
      if ((e.key === '/' || (e.key === 'k' && (e.metaKey || e.ctrlKey))) && !/^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName)) {
        e.preventDefault(); openS();
      }
    });
  }
})();

/* --- hero background video -------------------------------------------------
   The <source> URLs ship in data-src so nothing downloads until we have decided
   the visitor wants it. We skip the fetch only for Save-Data and slow
   connections, and pause offscreen to stop burning battery on a video nobody
   can see. The clip always autoplays on load, same as every other hero video
   out there. It plays once and rests on its final frame: it is never told to
   loop, and reaching the end never re-triggers playback, including when it
   scrolls back into view. There is no user-facing pause control; the clip is
   short, silent, decorative and non-interactive. */
(function () {
  var vids = [].slice.call(document.querySelectorAll('[data-bg-video]'));
  if (!vids.length) return;

  var conn = navigator.connection || {};
  var cheap = conn.saveData === true || /^(slow-)?2g$/.test(conn.effectiveType || '');

  var attach = function (v) {
    if (v.dataset.attached) return;
    v.dataset.attached = '1';
    v.querySelectorAll('source[data-src]').forEach(function (s) { s.src = s.dataset.src; });
    v.addEventListener('canplay', function () { v.classList.add('ready'); });
    v.load();
    v.play().catch(function () { /* autoplay refused: the still stands in */ });
  };

  vids.forEach(function (v) {
    if (!cheap) attach(v);

    // Only run while the hero is actually on screen, and never past the end.
    if (window.IntersectionObserver) {
      new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          if (!v.dataset.attached || v.ended) return;
          if (e.isIntersecting) { v.play().catch(function () {}); } else { v.pause(); }
        });
      }, { threshold: 0 }).observe(v);
    }
  });
})();
