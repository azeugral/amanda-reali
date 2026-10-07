# Estúdio Amanda Reali

Site da lash designer Amanda Reali ([@estudioamandareali](https://www.instagram.com/estudioamandareali/)): extensão de cílios, design de sobrancelhas e maquiagem.

Prévia: https://azeugral.github.io/amanda-reali/ (com `noindex` até ter domínio).

## Identidade (v2, 06/10)

Tirada do post de apresentação dela ("Um novo conceito de beleza"), em `../_ref/identidade.webp`.

- **Cores:** pêssego `#f6d3bd`, creme `#fdf5ef`, tinta azul-ardósia `#203241` e um dourado `#d9a441`, só nos brilhos.
- **Fonte:** Montserrat, a mesma do post, em tudo.
- **Detalhes:**
  - a estrela de 4 pontas;
  - a moldura em arco com o texto curvo por cima, igual ao post;
  - os feixes de linhas finas nos cantos da abertura.
- **Nav (v2):** convencional e mobile first.
  - Logo na esquerda máxima: o monograma AR mais "Amanda Reali".
  - Menu à direita, com o botão Agendar, a partir de 1080 px.
  - Abaixo disso, botão "Menu" que abre uma gaveta de tela cheia.
- **Logo oficial:** o original fica em `../_ref/cliente/logo-oficial.png`, com fundo transparente. A tinta foi trocada pela do site (#203241).
  - O `tools/logo.py` gera as peças:
    - nav em linha: AR + "AMANDA REALI" + subtítulo a partir de 1180 px, e sem o subtítulo abaixo disso;
    - logo completo no rodapé;
    - favicon.
- **Favicon:** o AR original sobre pêssego, num quadrado de cantos arredondados (`favicon-32.png`, `favicon.ico`, `icone-512.png`). O `icone-180` (iOS) fica quadrado, porque o iOS já arredonda.
- **Botões:** retos, com duas células: rótulo e ícone. No hover, a estrela gira 90° e a célula fica dourada.

Fotos dela em alta (06/10): `../_ref/cliente/amanda-hero.png` vai no arco da abertura e `amanda-sobre.png` no Sobre.

## Estrutura

| Arquivo | O que é |
|---|---|
| `index.html` | Abertura, serviços, técnicas e valores, efeitos, trabalhos recentes, sobre, como agendar, cuidados e chamada |
| `trabalhos.html` | Portfólio com filtro Cílios/Maquiagem (`?cat=`) e lightbox |
| `agendar.html` | Monta a mensagem e abre o WhatsApp `5515997615548`. Aceita `?servico=sobrancelha` ou `?servico=make` |
| `assets/js/site.js` | `CONFIG` (Instagram e WhatsApp) e o comportamento do site |
| `assets/js/obras.js` | Gerado. Não editar à mão |

## Fluxo

```bash
python tools/processar.py      # fotos de ../_ref/zip -> assets/obras + obras.js, foto, favicons, og-amanda.jpg
python tools/montar_paginas.py # tools/paginas/*.html -> páginas da raiz (V = cache)
```

## CONFIRMAR

Os itens pendentes aparecem no site como "✦ a preencher", com sublinhado tracejado.

- [ ] **Técnicas que ela oferece:** só o volume brasileiro está confirmado, porque ela escreve "Brasileiro" nas fotos. Fio a fio, egípcio e russo estão com "Oferece? a preencher". Apagar no `index.html` e no `agendar.html` as que ela não faz.
- [ ] **Valores** de aplicação e manutenção de cada técnica, prazo de manutenção e remoção.
- [ ] **Classificação das fotos:** nas fotos sem legenda dela, a técnica não foi escrita.
  - Pela imagem, minha leitura (a confirmar com ela):
    - 0 parece brasileiro;
    - 1, 3, 5, 6 e 7 parecem volume com pontas em W (egípcio?);
    - 11 e 12 parecem leque fechado (russo?).
  - Os números são os do `_ref/contato-*.jpg`.
- [ ] **Fotos 17 a 34 do zip:** ficaram de fora. Os ids são de contas diferentes do Instagram, e a 19 tem marca d'água de outra profissional. Se forem dela (de outro perfil), é só incluir em `OBRAS`.
- [ ] **Sobrancelhas:** não há foto só de sobrancelha. Saber se ela usa henna ou tintura.
- [ ] **Maquiagem:** saber se atende noivas e se vai a domicílio.
- [ ] **Cidade, endereço e horários.** O DDD é 15 e a bio cita a @adega_realledo, a mesma do André Azevedo (Capão Bonito). Confirmar a cidade antes de escrever.
- [ ] **Sobre:** desde quando atende, formação, cursos.
- [ ] **Sinal** para reservar, e a duração média da aplicação.
- [ ] **Cuidados:** a lista atual é a padrão do mercado. Ela confere.
- [ ] **Efeitos:** as 5 imagens são **ilustrativas, geradas por IA** (Figma AI, gemini-3.1-flash-image). Ficam em `../_ref/efeitos-ia`, e o site avisa isso abaixo da seção. Trocar por fotos reais dela, se tiver.
- [ ] **Adega Realledo:** está na bio e ficou fora do site.
- [ ] **Domínio:** trocar `BASE` em `tools/montar_paginas.py` e o `<base>` do 404, tirar o `noindex` e liberar o `robots.txt`.

---

Site por [L R G Z](https://lrgz.com.br)
