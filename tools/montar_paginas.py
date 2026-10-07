"""Monta as páginas da raiz a partir de tools/paginas/*.html (logo centralizado, barra de menu e rodapé comuns).
Troque V para furar o cache de CSS/JS.
Marcadores nas páginas: <!--seta-->, <!--estrela--> e <!--zap-->."""
import os, re, glob
V = '6'
AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(AQUI)
BASE = 'https://azeugral.github.io/amanda-reali/'  # CONFIRMAR: trocar quando houver domínio
ZAP = 'https://wa.me/5515997615548'

SETA = '<svg class="i-seta" viewBox="0 0 18 18" aria-hidden="true"><path d="M2 9h13M10 4l5 5-5 5"/></svg>'
# estrela de 4 pontas do post de apresentação dela
ESTRELA = '<svg class="i-estrela" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 0c.9 6.4 5.1 10.6 12 12-6.9 1.4-11.1 5.6-12 12-.9-6.4-5.1-10.6-12-12C6.9 10.6 11.1 6.4 12 0z"/></svg>'

LOGO = ('<picture class="marca"><source media="(min-width:1180px)" srcset="assets/img/logo-nav.webp">'
        '<img src="assets/img/logo-nav-curto.webp" alt="Amanda Reali · Lash designer, sobrancelhas e maquiagem" width="1000" height="172"></picture>')
LOGO_RODAPE = '<img class="logo-completo" src="assets/img/logo-completo-640.webp" srcset="assets/img/logo-completo-640.webp 640w, assets/img/logo-completo-1200.webp 1200w" sizes="(min-width:720px) 420px, 80vw" alt="Amanda Reali · Lash designer, sobrancelhas e maquiagem" width="1200" height="659" loading="lazy">'

HEAD = '''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{titulo}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex">
<meta name="theme-color" content="#f6d3bd">
<meta property="og:type" content="website">
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{base}og-amanda.jpg">
<meta property="og:locale" content="pt_BR">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" href="favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="assets/img/icone-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600&display=swap">
<link rel="stylesheet" href="assets/css/site.css?v={v}">
</head>
<body class="{corpo}">
<a class="sr" href="#conteudo">Pular para o conteúdo</a>
<div class="progresso" data-prog aria-hidden="true"><i></i></div>
<header class="nav">
  <a class="nav-logo" href="./" aria-label="Amanda Reali, início">{logo}</a>
  <button class="nav-abrir" type="button" aria-expanded="false" aria-controls="menu"><span>Menu</span><i aria-hidden="true"></i></button>
  <nav class="nav-menu" id="menu" aria-label="Principal"><ul class="menu">{menu}</ul><a class="btn peq" href="agendar.html"><span>Agendar</span><i>{estrela}</i></a></nav>
</header>
<main id="conteudo">
'''

FOOT = '''</main>
<footer class="rodape">
  <div class="wrap">
    <a class="rodape-logo" href="./" aria-label="Amanda Reali, início">{logo_rodape}</a>
    <div class="colunas">
      <div><h4>Páginas</h4><ul><li><a href="./">Início</a></li><li><a href="./#servicos">Serviços</a></li><li><a href="trabalhos.html">Trabalhos</a></li><li><a href="agendar.html">Agendar</a></li></ul></div>
      <div><h4>Contato</h4><ul><li><a href="{zap}" target="_blank" rel="noopener">WhatsApp (15) 99761-5548</a></li><li><a href="https://www.instagram.com/estudioamandareali/" target="_blank" rel="noopener">Instagram @estudioamandareali</a></li></ul></div>
      <div><h4>Estúdio</h4><ul><li>Cidade: <em class="a-preencher">a preencher</em></li><li>Endereço: <em class="a-preencher">a preencher</em></li><li>Horários: <em class="a-preencher">a preencher</em></li></ul></div>
    </div>
    <div class="base"><span>© <span data-ano>2026</span> Estúdio Amanda Reali. Todos os direitos reservados.</span><span>Site por <a href="https://lrgz.com.br" target="_blank" rel="noopener">L R G Z</a></span></div>
  </div>
</footer>
<a class="zap-fixo" href="agendar.html" aria-label="Agendar horário">{estrela}<span>Agendar</span></a>
{extra}<script src="assets/js/obras.js?v={v}"></script>
<script src="assets/js/site.js?v={v}"></script>
</body>
</html>
'''

LB = '''<div class="lb" role="dialog" aria-modal="true" aria-label="Foto ampliada" aria-hidden="true">
  <div class="lb-topo"><span class="rot" data-cont></span><button type="button" data-fechar>Fechar</button></div>
  <div class="lb-palco"><img alt=""></div>
  <div class="lb-base"><button type="button" data-ant aria-label="Anterior">&larr;</button><span class="rot" data-leg></span><button type="button" data-prox aria-label="Próxima">&rarr;</button></div>
</div>
'''

MENU = [('./', 'Início'), ('./#servicos', 'Serviços'), ('./#efeitos', 'Efeitos'), ('trabalhos.html', 'Trabalhos'), ('./#sobre', 'Sobre')]
ATUAL = ' aria-current="page"'

for f in glob.glob(os.path.join(AQUI, 'paginas', '*.html')):
    nome = os.path.basename(f)
    txt = open(f, encoding='utf-8').read()
    meta = dict(re.findall(r'<!--\s*(\w+):\s*(.*?)\s*-->', txt.split('\n---\n')[0]))
    corpo = txt.split('\n---\n', 1)[1].replace('<!--seta-->', SETA).replace('<!--estrela-->', ESTRELA).replace('<!--zap-->', ZAP)
    atual = {'index.html': './', '404.html': None}.get(nome, nome)
    menu = ''.join(f'<li><a href="{h}"' + (ATUAL if h == atual else '') + f'>{t}</a></li>' for h, t in MENU)
    html = HEAD.format(titulo=meta['titulo'], desc=meta['desc'], base=BASE, v=V, menu=menu, logo=LOGO, estrela=ESTRELA,
                       corpo='inicio' if nome == 'index.html' else 'interna') + corpo + \
        FOOT.format(v=V, logo=LOGO, logo_rodape=LOGO_RODAPE, zap=ZAP, estrela=ESTRELA, extra=LB if meta.get('lightbox') == 'sim' else '')
    if nome == '404.html':
        html = html.replace('<head>', '<head>\n<base href="/amanda-reali/">', 1)
    if nome == 'agendar.html':
        html = html.replace('<a class="zap-fixo"', '<a hidden class="zap-fixo"', 1)
    open(os.path.join(SITE, nome), 'w', encoding='utf-8', newline='\n').write(html)
    print('ok', nome)
