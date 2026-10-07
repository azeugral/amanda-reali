"""Gera as peças do logo a partir do logo oficial (../_ref/cliente/logo-oficial.png, fundo transparente).

- assets/img/logo-completo-{640,1200}.webp  logo inteiro, para o rodapé
- assets/img/logo-nav.webp / logo-nav-curto.webp  AR + "AMANDA REALI" (+ subtítulo no desktop), em linha, para o nav
- favicon-32.png, favicon.ico, assets/img/icone-180/512.png  AR sobre pêssego, cantos arredondados
A tinta do logo (#151b1f) é trocada pela tinta do site (#203241), mantendo o alfa original.
"""
import os
from PIL import Image, ImageDraw

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(AQUI)
IMG = os.path.join(SITE, 'assets', 'img')
ORIG = os.path.join(SITE, '..', '_ref', 'cliente', 'logo-oficial.png')
TINTA = (32, 50, 65)
PESSEGO = (246, 211, 189)

def limpar(im):
    a = im.getchannel('A').point(lambda v: 0 if v < 40 else v)
    out = Image.new('RGBA', im.size, TINTA + (0,))
    out.putalpha(a)
    return out

def blocos(im, x0=0, x1=None):
    """faixas horizontais com tinta (separadas por linhas vazias)"""
    a = im.getchannel('A')
    x1 = x1 or im.width
    rows = [y for y in range(im.height) if a.crop((x0, y, x1, y + 1)).getbbox()]
    bl, s, p = [], rows[0], rows[0]
    for y in rows[1:]:
        if y > p + 4:
            bl.append((s, p + 1)); s = y
        p = y
    bl.append((s, p + 1))
    return bl

def recorte(im, y0, y1):
    c = im.crop((0, y0, im.width, y1))
    return c.crop(c.getbbox())

def salvar(im, nome, larguras):
    for w in larguras:
        c = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS) if im.width > w else im
        c.save(os.path.join(IMG, f'{nome}-{w}.webp'), 'WEBP', quality=90, method=6)

def main():
    im = limpar(Image.open(ORIG).convert('RGBA'))
    im = im.crop(im.getbbox())
    bl = [b for b in blocos(im) if b[1] - b[0] > 12]
    ar, nome = (recorte(im, *b) for b in bl[:2])
    # subtítulo e linha com estrela encostam no meio: mede o subtítulo só pela metade esquerda
    y0, y1 = bl[2]
    ys = blocos(im.crop((0, y0, im.width // 3, y1)))[0]
    sub = recorte(im, y0 + ys[0], y0 + ys[1])
    print('peças', [p.size for p in (ar, nome, sub)])

    salvar(im, 'logo-completo', (640, 1200))

    # nav: AR à esquerda; à direita o nome e, na versão longa, o subtítulo
    def lockup(com_sub):
        h = 300
        a = ar.resize((round(ar.width * h / ar.height), h), Image.LANCZOS)
        n = nome.resize((round(nome.width * h * .36 / nome.height), round(h * .36)), Image.LANCZOS)
        col = [n]
        if com_sub:
            s = sub.resize((n.width, round(sub.height * n.width / sub.width)), Image.LANCZOS)
            col.append(s)
        gap = round(h * .1)
        ch = sum(c.height for c in col) + gap * (len(col) - 1)
        W = a.width + round(h * .16) + n.width
        out = Image.new('RGBA', (W, h), TINTA + (0,))
        out.alpha_composite(a, (0, 0))
        y = round((h - ch) / 2) + round(h * .06)
        for c in col:
            out.alpha_composite(c, (a.width + round(h * .16), y)); y += c.height + gap
        return out.crop(out.getbbox())
    for com, n in ((True, 'logo-nav'), (False, 'logo-nav-curto')):
        l = lockup(com)
        alvo = 1000
        l = l.resize((alvo, round(l.height * alvo / l.width)), Image.LANCZOS)
        l.save(os.path.join(IMG, n + '.webp'), 'WEBP', quality=92, method=6)
        print(n, l.size)

    # favicon: AR sobre pêssego, quadrado de cantos arredondados
    def icone(t, raio=.22, margem=.05):
        s = 4
        T = t * s
        base = Image.new('RGBA', (T, T), (0, 0, 0, 0))
        ImageDraw.Draw(base).rounded_rectangle((0, 0, T - 1, T - 1), radius=round(T * raio), fill=PESSEGO + (255,))
        m = ar.copy()
        larg = round(T * (1 - 2 * margem))
        m = m.resize((larg, round(m.height * larg / m.width)), Image.LANCZOS)
        if m.height > T * (1 - 2 * margem):
            alt = round(T * (1 - 2 * margem)); m = ar.resize((round(ar.width * alt / ar.height), alt), Image.LANCZOS)
        base.alpha_composite(m, ((T - m.width) // 2, (T - m.height) // 2))
        return base.resize((t, t), Image.LANCZOS)
    f32 = icone(32, margem=.03)
    f32.save(os.path.join(SITE, 'favicon-32.png'))
    icone(48, margem=.03).save(os.path.join(SITE, 'favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48)])
    icone(512).save(os.path.join(IMG, 'icone-512.png'))
    a180 = icone(180, raio=0)  # o iOS arredonda sozinho
    a180.convert('RGB').save(os.path.join(IMG, 'icone-180.png'))

if __name__ == '__main__':
    main()
