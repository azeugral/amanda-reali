# Estúdio Amanda Reali

Site da lash designer Amanda Reali ([@estudioamandareali](https://www.instagram.com/estudioamandareali/)): extensão de cílios, design de sobrancelhas e maquiagem.

Prévia: https://azeugral.github.io/amanda-reali/ (com `noindex` até ter domínio).

## Identidade v1

Tirada do post de apresentação dela ("Um novo conceito de beleza"), em `../_ref/identidade.webp`.

- **Cores:** pêssego `#f6d3bd`, creme `#fdf5ef`, tinta azul-ardósia `#203241` e um dourado `#d9a441`, só nos brilhos.
- **Fonte:** Montserrat, a mesma do post, em tudo.
- **Detalhes:**
  - a estrela de 4 pontas;
  - a moldura em arco com o texto curvo por cima, igual ao post;
  - os feixes de linhas finas nos cantos da abertura.
- **Logo:** por enquanto é uma marca em texto, "Amanda Reali" com a estrela e o subtítulo. Fica em `LOGO`, dentro de `tools/montar_paginas.py`.
- **Favicon:** a estrela em tinta com um brilho dourado sobre pêssego, gerada por `tools/processar.py`.
- **Botões:** retos, com duas células: rótulo e ícone. No hover, a estrela gira 90° e a célula fica dourada.

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
- [ ] **Foto dela:** a atual foi recortada do post (cerca de 360 px). Pedir uma foto original em alta.
- [ ] **Logo definitivo:** se ela tiver um, ele entra no lugar da marca em texto.
- [ ] **Adega Realledo:** está na bio e ficou fora do site.
- [ ] **Domínio:** trocar `BASE` em `tools/montar_paginas.py` e o `<base>` do 404, tirar o `noindex` e liberar o `robots.txt`.

---

Site por [L R G Z](https://lrgz.com.br)
