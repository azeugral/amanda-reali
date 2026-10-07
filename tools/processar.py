"""Gera assets/obras/*.webp, assets/js/obras.js, a foto da Amanda, favicons e og-amanda.jpg.

Originais em ../_ref/zip (índices = ordem alfabética, ver ../_ref/contato-*.jpg).
Fora do portfólio:
- 17 a 34: vêm de outras contas do Instagram (ids de dono diferentes, a 19 tem marca d'água de outra lash). CONFIRMAR com ela.
- 15: miniatura de story com 320 px, pouca resolução.
- 35 (Amanda.jpg): foto de perfil com 100 px; a foto usada vem de ../_ref/identidade.webp.
"""
import glob, json, os
from PIL import Image, ImageOps, ImageDraw, ImageFont, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(AQUI)
REF = os.path.join(SITE, '..', '_ref')
ORIG = os.path.join(REF, 'zip')
OUT = os.path.join(SITE, 'assets', 'obras')
IMG = os.path.join(SITE, 'assets', 'img')
FONTE = os.path.join(REF, 'fontes', 'Montserrat.ttf')

TINTA = (32, 50, 65)       # #203241
PESSEGO = (246, 211, 189)  # #f6d3bd
CREME = (253, 245, 239)    # #fdf5ef

C, M = 'cilios', 'make'
# índice -> (categoria, legenda, recorte opcional em frações x0,y0,x1,y1)
# A técnica só vai na legenda quando ela mesma escreveu na foto (10 e 14: "Brasileiro").
OBRAS = {
  0: (C, 'Extensão de cílios'), 1: (C, 'Extensão de cílios'), 2: (C, 'Extensão de cílios'),
  3: (C, 'Extensão de cílios'), 4: (C, 'Extensão de cílios'), 5: (C, 'Extensão de cílios'),
  6: (C, 'Extensão de cílios'), 7: (C, 'Extensão de cílios'), 8: (C, 'Extensão de cílios'),
  9: (M, 'Maquiagem'), 10: (C, 'Volume brasileiro'), 11: (C, 'Extensão de cílios'),
  12: (C, 'Extensão de cílios'), 13: (M, 'Maquiagem'), 14: (C, 'Volume brasileiro', (0, 0, 1, .93)),
  16: (C, 'Extensão de cílios'),
}

def fonte(tam, peso=b'Medium'):
    f = ImageFont.truetype(FONTE, tam)
    f.set_variation_by_name(peso)
    return f

def salvar(im, pasta, nome, larguras=(640, 1200), q=80):
    for w in larguras:
        c = im.copy()
        if c.width > w:
            c = c.resize((w, round(c.height * w / c.width)), Image.LANCZOS)
        c.save(os.path.join(pasta, f'{nome}-{w}.webp'), 'WEBP', quality=q, method=6)

def estrela(d, cx, cy, r, cor):
    """estrela de 4 pontas com lados côncavos (a do post de apresentação)"""
    pts = []
    import math
    for k in range(16):
        a = math.pi / 2 * (k / 4)
        rr = r if k % 4 == 0 else r * (.30 if k % 4 == 2 else .44)
        pts.append((cx + rr * math.cos(a - math.pi / 2), cy + rr * math.sin(a - math.pi / 2)))
    d.polygon(pts, fill=cor)

def main():
    for f in glob.glob(os.path.join(OUT, '*.webp')):
        os.remove(f)
    fs = sorted(glob.glob(os.path.join(ORIG, '*')))
    lista = []
    for i in sorted(OBRAS, reverse=True):  # o id do Instagram cresce com o tempo: mais recentes primeiro
        cat, desc, *rec = OBRAS[i]
        im = ImageOps.exif_transpose(Image.open(fs[i])).convert('RGB')
        if rec:
            x0, y0, x1, y1 = rec[0]
            im = im.crop((round(x0 * im.width), round(y0 * im.height), round(x1 * im.width), round(y1 * im.height)))
        nome = f'ar-{i:02d}'
        salvar(im, OUT, nome)
        lista.append({'id': nome, 'e': cat, 'd': desc, 'r': round(im.width / im.height, 3)})
    open(os.path.join(SITE, 'assets', 'js', 'obras.js'), 'w', encoding='utf-8').write(
        'window.OBRAS = ' + json.dumps(lista, ensure_ascii=False, separators=(',', ':')) + ';\n')

    # fotos dela em alta (enviadas pelo usuário em 06/10)
    h = Image.open(os.path.join(REF, 'cliente', 'amanda-hero.png')).convert('RGB')
    w = round(h.height * 358 / 560)  # proporção do arco da abertura
    x = (h.width - w) // 2
    h = h.crop((x, 0, x + w, h.height))
    for lw in (420, 760):
        h.resize((lw, round(h.height * lw / h.width)), Image.LANCZOS).save(os.path.join(IMG, f'amanda-{lw}.webp'), 'WEBP', quality=84, method=6)
    p = h  # base da prévia de link
    so = Image.open(os.path.join(REF, 'cliente', 'amanda-sobre.png')).convert('RGB')
    for lw in (420, 800):
        so.resize((lw, lw), Image.LANCZOS).save(os.path.join(IMG, f'amanda-sobre-{lw}.webp'), 'WEBP', quality=84, method=6)

    # efeitos: imagens ilustrativas geradas por IA (Figma AI, gemini-3.1-flash-image), em ../_ref/efeitos-ia
    for n in ('natural', 'boneca', 'gatinho', 'esquilo', 'molhado'):
        e = Image.open(os.path.join(REF, 'efeitos-ia', n + '.png')).convert('RGB')
        e = e.crop((0, 250, 928, 869))  # faixa do olho, 3:2
        salvar(e, IMG, 'efeito-' + n, (640,), q=80)

    # favicon: monograma AR em favicon.svg (redesenho do logo oficial); PNG/ICO renderizados a partir dele via Edge headless

    # prévia de link 1200x630
    og = Image.new('RGB', (1200, 630), PESSEGO)
    g = Image.new('L', (1200, 630))
    gd = ImageDraw.Draw(g)
    for y in range(630):
        gd.line((0, y, 1200, y), fill=int(120 * y / 630))
    og.paste(Image.new('RGB', (1200, 630), (242, 196, 170)), (0, 0), g)
    foto = ImageOps.fit(p, (300, 480), Image.LANCZOS, centering=(.5, .3))
    masc = Image.new('L', (300 * 4, 480 * 4), 0)
    ImageDraw.Draw(masc).rounded_rectangle((0, 0, 1199, 1919), radius=600, fill=255)
    masc = masc.resize((300, 480), Image.LANCZOS)
    og.paste(foto, (110, 75), masc)
    d = ImageDraw.Draw(og)
    d.rounded_rectangle((96, 61, 423, 568), radius=164, outline=TINTA, width=2)
    d.text((500, 205), 'Amanda Reali', font=fonte(78), fill=TINTA)
    d.text((504, 318), 'LASH DESIGNER · SOBRANCELHAS · MAQUIAGEM', font=fonte(22, b'SemiBold'), fill=TINTA)
    d.line((504, 375, 1100, 375), fill=TINTA, width=1)
    d.text((504, 400), 'Agende pelo WhatsApp', font=fonte(30, b'Regular'), fill=TINTA)
    estrela(d, 1110, 110, 34, TINTA)
    estrela(d, 1062, 166, 14, (217, 164, 65))
    og.save(os.path.join(SITE, 'og-amanda.jpg'), quality=86)
    print(len(lista), 'fotos;', sum(o['e'] == C for o in lista), 'de cílios')

if __name__ == '__main__':
    main()
