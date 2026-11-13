(function () {
  var doc = document;
  doc.documentElement.classList.add('js');

  // Contato a partir de config.js
  var S = window.SITE || {};
  var any = false;
  function fill(field, text, href) {
    var li = doc.querySelector('[data-field="' + field + '"]');
    if (!li || !text) return;
    var a = li.querySelector('a');
    if (a) { a.textContent = text; a.href = href; } else { li.querySelector('address').textContent = text; }
    li.hidden = false; any = true;
  }
  fill('email', S.email, 'mailto:' + S.email);
  fill('phone', S.phone, 'tel:+' + String(S.phone || '').replace(/\D/g, '').replace(/^(?!55)/, '55'));
  var waDigits = String(S.whatsapp || '').replace(/\D/g, '');
  var waLink = waDigits ? 'https://wa.me/' + waDigits + (S.whatsappMessage ? '?text=' + encodeURIComponent(S.whatsappMessage) : '') : '';
  var waShown = /^55\d{2}9\d{8}$/.test(waDigits) ? waDigits.replace(/^(55)(\d{2})(\d{5})(\d{4})$/, '+$1 $2 $3-$4') : '+' + waDigits;
  fill('whatsapp', waDigits && waShown, waLink);
  if (waLink) {
    var wa = doc.getElementById('wa-float');
    wa.href = waLink; wa.hidden = false;
    doc.querySelectorAll('[data-wa]').forEach(function (a) { a.href = waLink; a.hidden = false; });
  }
  fill('address', S.address);
  var ig = doc.querySelector('[data-ig]');
  if (ig && /^https?:\/\//.test(S.instagram || '')) { ig.href = S.instagram; ig.hidden = false; }
  var ml = doc.querySelector('[data-mail]');
  if (ml && S.email) { ml.href = 'mailto:' + S.email; ml.hidden = false; }
  var cm = doc.querySelector('[data-mail-btn]');
  if (cm && S.email) { cm.href = 'mailto:' + S.email; cm.hidden = false; }
  if (any) doc.getElementById('contact-empty').hidden = true;
  if (S.oab) { var o = doc.getElementById('oab'); o.textContent = S.oab; o.hidden = false; }
  doc.getElementById('ano').textContent = new Date().getFullYear();

  // Menu mobile
  var btn = doc.querySelector('.nav-toggle'), nav = doc.getElementById('menu');
  function setOpen(open) {
    btn.setAttribute('aria-expanded', open);
    btn.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
    nav.classList.toggle('open', open);
  }
  btn.addEventListener('click', function () { setOpen(btn.getAttribute('aria-expanded') !== 'true'); });
  nav.addEventListener('click', function (e) { if (e.target.tagName === 'A') setOpen(false); });
  doc.addEventListener('keydown', function (e) { if (e.key === 'Escape') setOpen(false); });

  // Sombra no header ao rolar
  var header = doc.querySelector('.site-header');
  function onScroll() { header.classList.toggle('scrolled', window.scrollY > 8); }
  onScroll(); window.addEventListener('scroll', onScroll, { passive: true });

  // Player do YouTube (só carrega ao clicar)
  var pl = doc.getElementById('player');
  if (pl) pl.querySelector('.player-btn').addEventListener('click', function () {
    var f = doc.createElement('iframe');
    f.src = pl.getAttribute('data-src');
    f.title = 'Vídeos do canal Direito Descomplicado';
    f.allow = 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture; fullscreen';
    f.allowFullscreen = true; f.loading = 'lazy';
    pl.innerHTML = ''; pl.appendChild(f);
  });

  // Animação de entrada
  var items = doc.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.12 });
    items.forEach(function (el, i) { el.style.transitionDelay = (i % 4) * 70 + 'ms'; io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('in'); });
  }
})();
