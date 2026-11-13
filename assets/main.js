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
  fill('whatsapp', waDigits && ('+' + waDigits), waLink);
  if (waLink) {
    var wa = doc.getElementById('wa-float');
    wa.href = waLink; wa.hidden = false;
  }
  fill('address', S.address);
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
