# Advocacia Fittipaldi — site

Site estático (HTML/CSS/JS, sem build), pronto para GitHub Pages.

## Editar
- Textos: `index.html`
- Contato e OAB: `assets/config.js` (campo vazio = não aparece no site)
- Cores/tipografia: variáveis no topo de `assets/style.css`

## Publicar no GitHub Pages com domínio próprio
1. Crie um repositório no GitHub e suba estes arquivos na raiz (branch `main`).
2. Settings → Pages → Source: **Deploy from a branch** → `main` / `(root)`.
3. Crie um arquivo `CNAME` na raiz contendo apenas o domínio, ex.: `advocaciafittipaldi.com.br`
   (ou configure em Settings → Pages → Custom domain).
4. No registrador do domínio, configure o DNS:
   - Domínio raiz (apex): 4 registros **A** → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `www`: registro **CNAME** → `<seu-usuario>.github.io`
5. Quando o DNS propagar, marque **Enforce HTTPS** em Settings → Pages.

Confira os IPs na documentação atual do GitHub Pages antes de configurar.

## Endereço provisório
https://www.advocaciafittipaldi.com.br/

## SEO — o que já está feito e o que falta

**Já no código (automático a cada `python3 tools/build_blog.py`):** título e descrição por página, canonical, Open Graph/Twitter (miniatura 1200×630), dados estruturados (LegalService, Person, WebSite, BlogPosting, breadcrumbs), sitemap.xml, robots.txt, HTML estático rápido, imagens com dimensões e lazy-load.

**Quando o domínio definitivo estiver no ar:**
1. Trocar `SITE_URL` em `tools/build_blog.py`, rodar o script, commitar e dar push.
2. Cadastrar o site no Google Search Console e enviar o `sitemap.xml`; fazer o mesmo no Bing Webmaster Tools.
3. Criar/reivindicar o Perfil da Empresa no Google (precisa do endereço do escritório) — é o que mais pesa em buscas locais como "advogado em São Paulo".
4. Preencher `address` e telefone fixo em `assets/config.js` e no JSON-LD.
5. Link do site no canal do YouTube, no Instagram, na página da OAB-SP e em diretórios jurídicos sérios.
6. Continuar publicando 1 artigo por vídeo (já é a principal fonte de tráfego orgânico).

**Limite ético:** o Código de Ética da OAB e o Provimento 205/2021 proíbem promessas, "melhor advogado", comparações e captação agressiva. O SEO aqui é de conteúdo informativo.
