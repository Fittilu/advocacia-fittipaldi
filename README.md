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
