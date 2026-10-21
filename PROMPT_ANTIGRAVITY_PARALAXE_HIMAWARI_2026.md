# Prompt para o Antigravity: imagens do Himawari com paralaxe corrigida e a nuvem que some sobre o anfiteatro

**Data:** 21 de outubro de 2026
**Uso:** copiar a PARTE B inteira para o Antigravity. A PARTE A é para o pesquisador.

---

# PARTE A — Para o pesquisador (não enviar)

**O que o prompt pede:** refazer as imagens e o GIF do Himawari com a paralaxe corrigida pixel a pixel, e não só na trajetória. Depois, seguir a nuvem que você marcou em azul em `docs/anotacoes/trajetoria_anotada_pesquisador_2026-10-21.webp` e testar se ela passa sobre o anfiteatro e some ali.

**Por que:** no GIF atual (`data/processed/himawari_trajetoria/nuvem_atravessa_himalaia_colapso.gif`) a imagem está na posição aparente e a trajetória está corrigida, então as duas não batem. Além disso, ele só segue o maior objeto abaixo de 213 K, e o último trecho da trajetória é troca de objeto. Os detalhes estão em `GEOESTACIONARIO_NOITE_25_26AGO2026.md`, § 6.

**O que vou conferir quando voltar:**
* Se as figuras novas são de arquivos novos, sem sobrescrever os antigos.
* Se a paralaxe foi aplicada a cada pixel, com a regra de oclusão.
* Se a nuvem marcada foi seguida por sobreposição a cada 10 min, sem saltos.
* Se o veredito sobre "some sobre o anfiteatro" vem com números: horário, temperatura e área.

---

# PARTE B — Prompt para o Antigravity

Você vai refazer as imagens do Himawari-9 do evento de 25–26/08/2026 no Lhende Khola (Nepal) com a **paralaxe corrigida em cada pixel**. Depois vai testar uma observação do pesquisador sobre uma nuvem que parece sumir ao passar sobre o anfiteatro de erosão. Responda em português.

## B.1 Contexto que você precisa saber

* **Sítio:** anfiteatro de erosão do Lhende, centro em 28,271 N / 85,515 E (local do USGS `us7000tbwb`). Polígono em `.claude/worktrees/himalaia-enchentes-auditoria-fcfdb5/data/processed/neve_anfiteatro/anfiteatro.geojson`. O anfiteatro vai de ~4.000 a ~7.200 m.
* **Hora do evento:** sinal sísmico às 02:52:10 UTC de 26/08 (08:37 no horário do Nepal, UTC+5:45). Todos os horários do trabalho são **UTC**.
* **Geometria:** o Himawari-9 está em 140,7 E e vê o sítio com zênite de ~68°. Um topo a h km aparece deslocado para **oeste-noroeste**, longe do ponto subsatélite, por ~2,4·h km: ~20 km para 8 km de topo e ~35 km para 14 km. O próprio terreno do anfiteatro, a 4–7 km de altitude, também aparece deslocado ~10–17 km na imagem navegada no elipsoide.
* **Leitor e funções prontas:** `scripts/himawari/ahi_hsd.py`:
  * `ler_segmento(caminho)` devolve `tb` e `rad`;
  * `ll2cl(...)` converte lat/lon em coluna/linha;
  * `paralaxe(lat_ap, lon_ap, h_km, sub_lon)` vai da posição aparente para a posição real.
  * A versão mais nova está no worktree (`.claude/worktrees/himalaia-enchentes-auditoria-fcfdb5/scripts/himawari/`); use essa.
  * A inversão (de "nuvem a h km sobre um ponto" para "pixel aparente") está em `fase_topo_10min.py`, função `aparente`.
* **Altura do topo pela Tb:** `h = 16 − 0,143 (Tb − 195)` km. Para topos quentes, não ponha piso de 9 km como em `trajetoria_sistema.py`: use 4,5–17 km. Abaixo de ~4,5 km, ou com Tb > ~270 K, trate o pixel como superfície ou nuvem baixa, usando a altitude do terreno (Copernicus GLO-30; `scripts/neve_anfiteatro/anfiteatro_glo30.py` mostra como ler) para corrigir o deslocamento do próprio relevo.
* **Dados:**
  * a cada 30 min de 25/08 11:00 a 26/08 03:00: `data/raw/himawari_b13/`;
  * B07 e B13 a cada 10 min de 25/08 22:00 a 26/08 03:30: `data/raw/himawari_10min/` (não existe a varredura das 02:40);
  * para o resto da janela a 10 min, baixe do bucket público `https://noaa-himawari9.s3.amazonaws.com/AHI-L1b-FLDK/AAAA/MM/DD/HHMM/`, arquivo `HS_H09_<AAAAMMDD>_<HHMM>_B13_FLDK_R20_S0310.DAT.bz2`, ~2,5 MB cada. Pergunte ao pesquisador antes de baixar mais de 200 MB.
* **O que já foi medido** (`GEOESTACIONARIO_NOITE_25_26AGO2026.md`, § 6), para conferência:
  * o topo da nuvem sobre o sítio ficou em 218–235 K de ~17:30 a 00:30;
  * desceu para o terreno entre 00:30 e 01:30 (234 → 261 → 273 K);
  * às 02:50 não há topo mais frio que ~263 K a até 30 km.
  * O seu resultado tem de ser compatível com isso, ou explicar por que não é.

## B.2 A observação do pesquisador que você vai testar

Em `docs/anotacoes/trajetoria_anotada_pesquisador_2026-10-21.webp` (painéis de `trajetoria.png`), o pesquisador circulou em azul uma nuvem e sua posição aparente em cada horário:

| UTC | Posição aproximada marcada (aparente) |
| :--- | :--- |
| 25/08 09:00 | ~88 E, ~28,3 N |
| 25/08 12:00 | ~88 E, ~29,2 N |
| 25/08 15:00 | ~88,5 E, ~28,8 N |
| 25/08 18:00 | ~87,5 E, ~28,5 N (maior) |
| 25/08 21:00 | ~87 E, ~28,3 N |
| 26/08 00:00 | ~82,5–83,5 E, ~27,5–29 N (já a **oeste** do sítio) |
| 26/08 02:50 | "X" em ~82,8 E, ~28,7 N: desapareceu |

A leitura dele é que "existe realmente uma nuvem que desaparece quando passa sobre o anfiteatro". Teste isso sem pressupor o resultado:
1. **Essa nuvem é um objeto contínuo?** De 21:00 a 00:00 o salto é de ~87 E para ~83 E, ~400 km em 3 h. Siga-a **a cada 10 min**, por sobreposição de área entre horários consecutivos, com limite de velocidade de 80 km/h. Não use o "maior objeto": isso é o que gerou a troca de objeto no GIF atual.
   * Use limiares mais quentes que 213 K, porque a nuvem perto do sítio tinha 218–235 K. Faça o acompanhamento a 235 K e a 250 K e diga qual dá um objeto contínuo.
   * Se for um objeto só, dê a trajetória já corrigida. Se forem objetos diferentes, diga quando e onde um some e o outro aparece.
2. **Ela passa sobre o anfiteatro?** Com a paralaxe corrigida, dê a menor distância entre a borda do objeto e o polígono do anfiteatro, o horário e a Tb mínima do objeto nesse momento.
3. **Ela some ali?** Dê a série de área e Tb mínima do objeto a cada 10 min. "Sumir" quer dizer cair abaixo do limiar. Diga se isso aconteceu sobre o anfiteatro (a até ~30 km, corrigido), antes ou depois dele, e quanto tempo antes de 02:52.
4. **Compare com a § 6 do GEOESTACIONARIO.** O colapso medido lá (00:30–01:30, sobre o sítio) é a mesma nuvem? Se não for, qual era a nuvem sobre o sítio?

## B.3 Como corrigir a paralaxe nas imagens

Para cada horário:
1. Leia a Tb na grade do satélite, não reamostrada.
2. Para cada pixel com Tb < 270 K, calcule h(Tb) e a posição real com `paralaxe`. Para os outros pixels, use a altitude do terreno.
3. Projete cada pixel na grade corrigida, de 0,02°, a partir da posição real ("splat"). Quando vários pixels caírem na mesma célula, **fique com o mais frio**, porque o topo mais alto oculta o que está embaixo. Preencha buracos de uma célula com o vizinho mais frio. Marque como "sem dado" o que ficar vazio, em vez de interpolar.
4. Desenhe o polígono e a estrela do anfiteatro na **posição real**, que agora é a mesma da imagem.

Gere, em arquivos **novos** e sem sobrescrever os antigos, em `data/processed/himawari_paralaxe/`:
* `paineis_paralaxe_corrigida.png`: os mesmos 8 horários de `trajetoria.png`, lado a lado com a versão aparente, com a nuvem seguida em B.2 contornada.
* `nuvem_paralaxe_corrigida_10min.gif`: zoom de ±250 km em torno do sítio, de 25/08 17:00 a 26/08 03:30, a cada 10 min. Inclua o contorno da nuvem seguida, a trajetória corrigida (sem trechos de troca de objeto) e, embaixo, a série de área e Tb mínima dela e a Tb sobre o sítio (paralaxe invertida, como em `fase_topo_10min.py`).
* `nuvem_seguida.json` e `.txt`: a série a cada 10 min, com UTC, área (km²), Tb mínima, centroide aparente e corrigido, distância ao anfiteatro e limiar usado.
* `LEIA-ME_paralaxe.md`: método, resultados de B.2 (itens 1–4) com números, e limites.

## B.4 Regras

* **Nada inventado.** Se um horário não tiver dado, diga. Se o acompanhamento falhar, diga onde.
* **Nada de afirmar "colapsa sobre a arena"** sem os números de B.2 itens 2–3.
* **Não mude os arquivos que já existem:** `trajetoria.*`, o GIF atual, os scripts do worktree, `GEOESTACIONARIO_NOITE_25_26AGO2026.md` e o artigo. Escreva scripts novos em `scripts/himawari/`, com nome que diga o que fazem.
* **Teste antes de concluir:** um pixel de topo a 10 km sobre o sítio tem de cair, depois da correção, a menos de 3 km do sítio.
* Ao terminar, mostre ao pesquisador a tabela de B.2 e a figura `paineis_paralaxe_corrigida.png`.
