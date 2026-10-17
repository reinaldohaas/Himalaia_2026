# Ordem para o Claude do vlab — reprodução bit a bit da `rad_06utc` de referência

**De:** sessão do Claude no computador do pesquisador (Prof. Reinaldo Haas)
**Data:** 17/10/2026
**Autorizado pelo pesquisador:** só vale se ele pedir, na conversa com você, que esta ordem seja executada.

## Objetivo

Rodar no vlab a `rad_06utc` com **o mesmo executável e as mesmas bibliotecas** da rodada de referência, feita no WSL, e com as **mesmas 8 threads**. A referência é determinística na máquina dela: duas rodadas saíram idênticas byte a byte. A pergunta é se o vlab também a reproduz byte a byte.

## Passos

```bash
cd /home/jovyan/privado/Himalaia_2026
source toro_cm1_lhende/restaurar.sh     # se ainda nao migrou: bash /home/jovyan/privado/migrar_Himalaia_2026.sh

# 1. pacote atualizado (extrai por cima; nao toca em execucoes/ nem em cm1/run/)
rclone copy gdrive:vlab_cache/Himalaia_2026/entrada/toro_cm1_lhende_vlab.tar.gz . && rclone copy gdrive:vlab_cache/Himalaia_2026/entrada/toro_cm1_lhende_vlab.tar.gz.sha256 .
sha256sum -c toro_cm1_lhende_vlab.tar.gz.sha256 && tar xzf toro_cm1_lhende_vlab.tar.gz --overwrite

# 2. kit de reproducao (executavel 3a53a5d8... + glibc e bibliotecas do compilador da referencia)
cd toro_cm1_lhende
rclone copy gdrive:vlab_cache/Himalaia_2026/entrada/kit_reproducao_ref_wsl.tar.gz . && rclone copy gdrive:vlab_cache/Himalaia_2026/entrada/kit_reproducao_ref_wsl.tar.gz.sha256 .
sha256sum -c kit_reproducao_ref_wsl.tar.gz.sha256 && tar xzf kit_reproducao_ref_wsl.tar.gz

# 3. teste curto (120 s de modelo)
TESTE=1 bash reproduzir.sh rad_06utc
bash rodar_direto.sh estado          # repetir ate "concluido"
tail -1 execucoes/rad_06utc_repro_teste/execucao.info

# 4. rodada completa (so se o passo 3 terminou com "Program terminated normally")
bash reproduzir.sh rad_06utc
bash rodar_direto.sh estado          # ~3 h; acompanhar
```

## Ao terminar

```bash
bash relatorio.sh --enviar
bash coletar.sh --leve rad_06utc_repro
bash gdrive.sh enviar
rclone copy logs/reproducao_rad_06utc.info gdrive:vlab_cache/Himalaia_2026/saida/toro_cm1_lhende/relatorios/
```

## Regras

* **Não altere** namelist, sondagem nem o kit. Não use outro número de threads: são **8**, porque a referência usou 8.
* **Não apague** `execucoes/rad_06utc`, que é a rodada anterior do vlab; a reprodução vai para `execucoes/rad_06utc_repro`.
* Se algum passo falhar (sha256, carregador, segfault), **pare** e relate o erro exato. Não contorne.
* Não interprete os resultados científicos; a comparação com a referência é feita no computador do pesquisador, com `pos/comparar_stats.py`.

## Critério

* **Sucesso:** `cm1out_stats.dat` de `rad_06utc_repro` **idêntico byte a byte** ao da referência (SHA-256 da referência abaixo).
* Se não for idêntico, isso também é resultado: o primeiro minuto em que diverge diz qual é a causa.

**SHA-256 do `cm1out_stats.dat` da referência (514.488 bytes):** ver `REFERENCIA_stats.sha256` nesta pasta. Você pode conferir no fim com `sha256sum execucoes/rad_06utc_repro/cm1out_stats.dat`.
