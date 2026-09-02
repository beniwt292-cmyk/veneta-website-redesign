document.querySelectorAll('#yr').forEach(function(e){e.textContent=new Date().getFullYear();});
function openNav(){document.getElementById('mnav').classList.add('on');document.body.style.overflow='hidden';}
function closeNav(){document.getElementById('mnav').classList.remove('on');document.body.style.overflow='';}
document.querySelectorAll('.mnav a').forEach(function(a){a.addEventListener('click',closeNav);});
addEventListener('keydown',function(e){if(e.key==='Escape')closeNav();});
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}})},{threshold:.12});
document.querySelectorAll('.rev').forEach(function(el,i){el.style.transitionDelay=(i%4*60)+'ms';io.observe(el);});
var hdr=document.querySelector('header');
if(hdr){var setStuck=function(){hdr.classList.toggle('stuck',scrollY>8);};setStuck();addEventListener('scroll',setStuck,{passive:true});}
var bar=document.getElementById('sticky');
if(bar){addEventListener('scroll',function(){var p=scrollY/(document.body.scrollHeight-innerHeight);bar.classList.toggle('on',p>0.12&&p<0.94);},{passive:true});}
document.querySelectorAll('.chip').forEach(function(c){c.addEventListener('click',function(){c.setAttribute('aria-pressed',c.getAttribute('aria-pressed')==='true'?'false':'true');});});
document.querySelectorAll('form[data-mock]').forEach(function(f){f.addEventListener('submit',function(e){e.preventDefault();var n=f.querySelector('.mockmsg');if(n){n.hidden=false;}});});
document.querySelectorAll('.gal-thumbs button').forEach(function(b){b.addEventListener('click',function(){var m=document.getElementById('gal-main');if(!m)return;var pp=m.parentNode;if(pp&&pp.tagName==='PICTURE'){pp.querySelectorAll('source').forEach(function(s){s.remove();});}m.src=b.dataset.src;m.alt=b.dataset.alt||m.alt;});});
/* ===== VENETA interactive layer =============================================
   Product finder, live grid filtering, product mega menu and site search.
   Data below is injected at build time.
   ========================================================================== */
(function () {
  var D = {"products":{"cellular-shades":{"name":"Cellular Shades","desc":"The warmest shade in the line.","price":"Price at The Home Depot","img":"cellular-card.webp","badges":["Cordless standard","Blackout option"],"wide":false},"roller-solar-shades":{"name":"Roller &amp; Solar","desc":"Clean lines. Precise light control.","price":"Price at The Home Depot","img":"roller-card.webp","badges":["Cordless option","1% to 14% openness"],"wide":true},"roman-shades":{"name":"Roman Shades","desc":"Soft fabric. Structured folds.","price":"Price at The Home Depot","img":"roman-card.webp","badges":["Cordless option","Designer fabrics"],"wide":false},"faux-wood-blinds":{"name":"Faux Wood Blinds","desc":"Looks like wood. Handles humidity like vinyl.","price":"Price at The Home Depot","img":"fauxwood-card.webp","badges":["Moisture resistant","Cordless option"],"wide":false},"shutters":{"name":"Shutters","desc":"Architecture, not a window covering.","price":"Price at The Home Depot","img":"shutters-card.webp","badges":["Adds resale appeal","Cordless"],"wide":true},"sheer-shades":{"name":"Sheer Shades","desc":"Two layers of sheer. One layer of vane.","price":"Price at The Home Depot","img":"sheer-card.webp","badges":["Tilting vanes","UV protection"],"wide":false},"dualdrape":{"name":"DualDrape&trade;","desc":"A sheer and a drape on one track.","price":"Price at The Home Depot","img":"dualdrape-card.webp","badges":["Patio door scale","Rotate and traverse"],"wide":true},"vertical-blinds":{"name":"Vertical Blinds","desc":"The practical answer for a sliding door.","price":"Price at The Home Depot","img":"vertical-card.webp","badges":["Patio door scale","Wipe clean"],"wide":true}},"room":{"Living room":["roller-solar-shades","sheer-shades","roman-shades"],"Bedroom":["cellular-shades","roman-shades","roller-solar-shades"],"Nursery":["cellular-shades","sheer-shades","roller-solar-shades"],"Kitchen":["faux-wood-blinds","roller-solar-shades","vertical-blinds"],"Bathroom":["faux-wood-blinds","shutters","vertical-blinds"],"Home office":["roller-solar-shades","sheer-shades","cellular-shades"],"Dining room":["roman-shades","sheer-shades","shutters"],"Patio door":["vertical-blinds","dualdrape","shutters"],"Patio door or wide opening":["vertical-blinds","dualdrape","shutters"],"Skylight":["cellular-shades","roller-solar-shades","sheer-shades"],"Arched window":["cellular-shades","shutters","sheer-shades"]},"need":{"Block all light":["cellular-shades","roller-solar-shades","roman-shades"],"Block all the light":["cellular-shades","roller-solar-shades","roman-shades"],"Soften the light":["sheer-shades","cellular-shades","roman-shades"],"Keep the view":["roller-solar-shades","shutters","sheer-shades"],"Cut glare and heat":["roller-solar-shades","sheer-shades","cellular-shades"],"Save energy":["cellular-shades","shutters","faux-wood-blinds"],"Lower the energy bill":["cellular-shades","shutters","faux-wood-blinds"],"Privacy":["shutters","cellular-shades","faux-wood-blinds"],"Privacy without darkness":["sheer-shades","shutters","cellular-shades"],"Child & pet safety":["cellular-shades","sheer-shades","roller-solar-shades"],"Child and pet safety":["cellular-shades","sheer-shades","roller-solar-shades"],"Moisture resistance":["faux-wood-blinds","vertical-blinds","shutters"],"Handle humidity":["faux-wood-blinds","vertical-blinds","shutters"],"Lowest price":["roller-solar-shades","faux-wood-blinds","cellular-shades"]},"look":{"Clean and modern":["roller-solar-shades","cellular-shades"],"Soft folds":["roman-shades","sheer-shades"],"Natural wood":["faux-wood-blinds","shutters"],"Sheer and airy":["sheer-shades","dualdrape"],"Classic shutters":["shutters","faux-wood-blinds"]},"lift":{"Cordless":["cellular-shades","roller-solar-shades","roman-shades"],"Motorized":["cellular-shades","roller-solar-shades","sheer-shades"],"No preference":[]}};
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
