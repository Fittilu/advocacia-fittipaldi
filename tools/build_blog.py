#!/usr/bin/env python3
"""Gera as páginas do blog, a seção "Artigos" da home e o sitemap.

Uso:  python3 tools/build_blog.py
Artigos: conteudo/blog/*.md (cabeçalho com titulo, descricao, data, autor).
Quando o domínio definitivo estiver no ar, altere SITE_URL abaixo e rode de novo.
"""
import html, re, pathlib, datetime

SITE_URL = "https://fittilu.github.io/advocacia-fittipaldi"   # sem barra no final
ROOT = pathlib.Path(__file__).resolve().parent.parent
MESES = ["janeiro","fevereiro","março","abril","maio","junho","julho","agosto","setembro","outubro","novembro","dezembro"]

def data_pt(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{d.day} de {MESES[d.month-1]} de {d.year}"

def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"\*(.+?)\*", r"<em>\1</em>", t)
    t = re.sub(r"\[(.+?)\]\((https?://[^)\s]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', t)
    t = re.sub(r"\[(.+?)\]\((\.\./[^)\s]+)\)", r'<a href="\2">\1</a>', t)  # link interno
    return t

def md(body):
    out = []
    for blk in re.split(r"\n\s*\n", body.strip()):
        lines = blk.strip().splitlines()
        if blk.startswith("## "):
            out.append(f"<h2>{inline(blk[3:].strip())}</h2>")
        elif all(l.startswith("- ") for l in lines):
            out.append("<ul>" + "".join(f"<li>{inline(l[2:])}</li>" for l in lines) + "</ul>")
        else:
            out.append(f"<p>{inline(' '.join(lines))}</p>")
    return "\n        ".join(out)

def load():
    posts = []
    for f in sorted((ROOT / "conteudo/blog").glob("*.md")):
        txt = f.read_text(encoding="utf-8")
        m = re.match(r"---\n(.*?)\n---\n(.*)", txt, re.S)
        meta = dict(l.split(": ", 1) for l in m.group(1).splitlines() if ": " in l)
        meta["slug"] = f.stem; meta["html"] = md(m.group(2))
        posts.append(meta)
    return sorted(posts, key=lambda p: p["data"], reverse=True)

def head(title, desc, canon, root, extra=""):
    t, d = html.escape(title), html.escape(desc, quote=True)
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{t}</title>
  <meta name="description" content="{d}">
  <meta name="theme-color" content="#13244a">
  <link rel="canonical" href="{canon}">
  <meta property="og:type" content="{'article' if extra else 'website'}">
  <meta property="og:locale" content="pt_BR">
  <meta property="og:title" content="{t}">
  <meta property="og:description" content="{d}">
  <meta property="og:url" content="{canon}">
  <meta property="og:image" content="{SITE_URL}/assets/og.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="{root}favicon.ico" sizes="48x48">
  <link rel="icon" type="image/png" href="{root}assets/favicon-512.png">
  <link rel="apple-touch-icon" href="{root}assets/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Source+Sans+3:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{root}assets/style.css?v=__VERSION__">
{extra}</head>'''

def chrome_top(root):
    return f'''<body>
  <a class="skip" href="#conteudo">Ir para o conteúdo</a>
  <header class="site-header" id="topo">
    <div class="wrap header-in">
      <a class="brand" href="{root}" aria-label="Advocacia Fittipaldi — início">
        <img src="{root}assets/logo.png" alt="Advocacia Fittipaldi — Assessoria Jurídica Estratégica" width="890" height="215">
      </a>
      <button class="nav-toggle" aria-expanded="false" aria-controls="menu" aria-label="Abrir menu"><span></span><span></span><span></span></button>
      <nav id="menu" class="nav" aria-label="Principal">
        <a href="{root}#sobre">O escritório</a>
        <a href="{root}#areas">Áreas de atuação</a>
        <a href="{root}#fundador">Fundador</a>
        <a href="{root}#canal">Canal</a>
        <a href="{root}blog/">Blog</a>
        <a href="{root}#contato" class="btn btn-sm">Contato</a>
      </nav>
    </div>
  </header>
'''

def chrome_bottom(root):
    return f'''
  <footer class="site-footer">
    <div class="wrap footer-in">
      <img src="{root}assets/logo-claro.png" alt="Advocacia Fittipaldi" width="890" height="215" class="footer-logo">
      <div class="footer-meta">
        <p>© <span id="ano">2026</span> Advocacia Fittipaldi. Todos os direitos reservados.</p>
        <p id="oab" hidden></p>
        <p><a class="foot-link" href="https://www.youtube.com/@direitodescomplicadofittipaldi" target="_blank" rel="noopener">YouTube: Direito Descomplicado</a></p>
        <p class="disclaimer">Este site tem caráter exclusivamente informativo, nos termos do Código de Ética e Disciplina da OAB, e não constitui oferta de serviços nem aconselhamento jurídico.</p>
      </div>
    </div>
  </footer>
  <a class="wa-float" id="wa-float" href="#" target="_blank" rel="noopener" hidden aria-label="Conversar pelo WhatsApp">
    <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
    <span>WhatsApp</span>
  </a>
  <script src="{root}assets/config.js?v=__VERSION__"></script>
  <script src="{root}assets/main.js?v=__VERSION__"></script>
</body>
</html>
'''

def write(path, content):
    p = ROOT / path; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(content, encoding="utf-8")

def cards(posts, root):
    return "\n".join(f'''          <li class="reveal"><time datetime="{p['data']}">{data_pt(p['data'])}</time>
            <h3><a href="{root}blog/{p['slug']}/">{html.escape(p['titulo'])}</a></h3>
            <p>{html.escape(p['descricao'])}</p>
            <a class="more" href="{root}blog/{p['slug']}/">Ler artigo →</a></li>''' for p in posts)

def build():
    posts = load()
    # artigos
    for p in posts:
        url = f"{SITE_URL}/blog/{p['slug']}/"
        ld = f'''  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"BlogPosting","headline":{__import__('json').dumps(p['titulo'], ensure_ascii=False)},"description":{__import__('json').dumps(p['descricao'], ensure_ascii=False)},"datePublished":"{p['data']}","inLanguage":"pt-BR","mainEntityOfPage":"{url}","image":"{SITE_URL}/assets/og.jpg","author":{{"@type":"Person","name":{__import__('json').dumps(p.get('autor','Luiz Fittipaldi'), ensure_ascii=False)}}},"publisher":{{"@type":"Organization","name":"Advocacia Fittipaldi","logo":{{"@type":"ImageObject","url":"{SITE_URL}/assets/apple-touch-icon.png"}}}}}}
  </script>
'''
        root = "../../"
        page = head(f"{p['titulo']} | Advocacia Fittipaldi", p["descricao"], url, root, ld) + "\n" + chrome_top(root) + f'''
  <main id="conteudo">
    <article class="post">
      <div class="wrap post-wrap">
        <nav class="crumbs" aria-label="Você está em"><a href="{root}">Início</a> <span>/</span> <a href="{root}blog/">Blog</a></nav>
        <p class="kicker">Artigo</p>
        <h1>{html.escape(p['titulo'])}</h1>
        <p class="post-meta"><time datetime="{p['data']}">{data_pt(p['data'])}</time> · {html.escape(p.get('autor','Luiz Fittipaldi'))}</p>
        {p['html']}
        <aside class="post-cta">
          <p>Quer conversar sobre o tema?</p>
          <a class="btn" href="#" data-wa hidden target="_blank" rel="noopener">Fale pelo WhatsApp</a>
          <a class="btn btn-outline" href="{root}#contato">Contato do escritório</a>
        </aside>
        <p class="back"><a href="{root}blog/">← Todos os artigos</a></p>
      </div>
    </article>
  </main>''' + chrome_bottom(root)
        write(f"blog/{p['slug']}/index.html", page)
    # listagem
    root = "../"
    lst = head("Blog | Advocacia Fittipaldi", "Artigos de Luiz Fittipaldi sobre direito tributário, planejamento sucessório, societário e empresas.", f"{SITE_URL}/blog/", root) + "\n" + chrome_top(root) + f'''
  <main id="conteudo">
    <section class="section">
      <div class="wrap">
        <div class="section-head">
          <p class="kicker">Blog</p>
          <h1 class="h2like">Artigos <em>de Luiz Fittipaldi</em></h1>
        </div>
        <ul class="post-list">
{cards(posts, root)}
        </ul>
      </div>
    </section>
  </main>''' + chrome_bottom(root)
    write("blog/index.html", lst)
    # home: seção Artigos
    idx = (ROOT / "index.html").read_text(encoding="utf-8")
    teaser = f'''<!-- BLOG:START -->
    <section class="section" id="blog">
      <div class="wrap">
        <div class="section-head reveal">
          <p class="kicker">Blog</p>
          <h2>Artigos <em>recentes</em></h2>
        </div>
        <ul class="post-list">
{cards(posts[:3], "")}
        </ul>
        <p class="all-posts"><a class="btn btn-outline" href="blog/">Ver todos os artigos</a></p>
      </div>
    </section>
    <!-- BLOG:END -->'''
    idx = re.sub(r"<!-- BLOG:START -->.*?<!-- BLOG:END -->", lambda m: teaser, idx, flags=re.S)
    (ROOT / "index.html").write_text(idx, encoding="utf-8")
    # sitemap + robots
    hoje = datetime.date.today().isoformat()
    urls = [(f"{SITE_URL}/", hoje), (f"{SITE_URL}/blog/", posts[0]["data"])] + [(f"{SITE_URL}/blog/{p['slug']}/", p["data"]) for p in posts]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{u}</loc><lastmod>{d}</lastmod></url>\n" for u, d in urls) + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")
    print(f"{len(posts)} artigo(s) gerado(s).")

if __name__ == "__main__":
    build()
