# CLAUDE.md — toro-CM1 no vlab (Lhende Khola, 25–26/08/2026)

Você está no contêiner do **vlab/UFSC** (JupyterHub), rodando o pacote `toro_cm1_lhende`, preparado por outra sessão do Claude no computador do pesquisador (Prof. Reinaldo Haas, Física/UFSC). O objetivo é **rodar e analisar** as simulações do CM1 descritas em `docs/TORO_CM1_SONDAGEM_REAL_ERA5.md` (cópia local; original no repositório `github.com/reinaldohaas/Himalaia_2026`, branch `claude/himalaia-enchentes-auditoria-fcfdb5`). Leia o `README.md` desta pasta antes de agir.

## O ambiente

* **Contêiner rodando como `root`, com `HOME=/root`. `/root` pode ser apagado** quando o servidor reinicia. Tudo o que precisa sobreviver fica em **`/home/jovyan/privado`**. O `ambiente.sh` define `PERSIST`, `ENVDIR` (`conda_envs/`), `RCLONE_CONFIG` e `GH_CONFIG_DIR`, e todos os scripts o carregam. Não crie ambientes conda com `-n`, nem guarde nada em `/root`.
* **Não há Slurm** (`sbatch` não existe). Use **`rodar_direto.sh`**:
  * `recursos`, para ver núcleos e memória reais;
  * `-t <caso>`, para um teste de 120 s;
  * `<caso|grupo>`, para rodar em segundo plano;
  * `estado` e `parar`.
* O CM1 roda em segundo plano dentro do servidor do Jupyter. Se o servidor for desligado, a rodada morre. Encerrar a sua sessão do Claude **não** a interrompe.
* **Drive:** o login do Google é feito pelo pesquisador **no Windows**; ele sobe o `rclone.conf` para `privado/` e você roda `bash gdrive.sh importar` (que move o arquivo sem lê-lo). Não tente autenticar daqui.
* Transferência com o computador do pesquisador:
  * **Google Drive** via `gdrive.sh`: remoto `gdrive:`, pasta `vlab_cache/{entrada,saida}`;
  * **GitHub** para baixar o pacote (o repositório é **público**).
  * Não há scp nem rsync.

## Fluxo

Ao começar uma sessão (sobretudo depois de um reinício): `source restaurar.sh`. Isso exporta o `RCLONE_CONFIG` persistente; sem ele, o `rclone` lê um arquivo antigo em `/root` e pede senha. Para o pesquisador verificar o seu trabalho: `bash relatorio.sh --enviar`.

```bash
cd /home/jovyan/privado/mesoescala-montanhas/toro_cm1_lhende
bash compilar.sh                 # se cm1/run/cm1.exe nao existir ou o ambiente mudou
bash rodar_direto.sh recursos
bash rodar_direto.sh -t rad_12utc && bash rodar_direto.sh estado
bash rodar_direto.sh rad         # rad_06utc (principal, 21 h de modelo) e rad_12utc
bash pos/analisar.sh && bash coletar.sh --leve && bash gdrive.sh enviar
```

## Regras deste trabalho (não negociáveis)

1. **Nenhum número sem arquivo.** Todo valor que você relatar vem de uma saída do CM1, de um log ou de um script rodado aqui. Se algo não rodou ou não terminou com `Program terminated normally`, diga isso e mostre o erro. Nunca descreva resultado de rodada que não terminou.
2. **Não altere `casos/*/namelist.input`, `input_sounding`, `perts.dat` nem `sfc_init.dat`** sem pedido explícito do pesquisador. Se precisar mudar algo por estabilidade ou custo (por exemplo `tapfrq`), proponha antes. Toda mudança aceita vai para `MUDANCAS.md`, com data, motivo e efeito.
3. **Não desligue `output_dbz`, `output_vort` nem `output_uh`.** Nas rodadas NSSL com terreno e radiação, isso derrubou o modelo com falha de segmentação após ~2 min.
4. **Credenciais:** nunca leia, imprima nem copie tokens (`rclone.conf`, `gh`, `.claude.json`). O login é sempre feito pelo pesquisador.
5. **Não publique nada** (git push, Release, Drive) sem pedido explícito.
6. Classifique críticas como *aritmética*, *método* ou *dado*. Não trate hipóteses heterodoxas do pesquisador com desdém: teste-as com os dados.

## O que já se sabe (não refaça, não contradiga sem dado novo)

* **Sondagem:** o `era5_to_sounding.py` do autor põe a pressão de superfície da célula ERA5 (4.322 m) na altitude pedida, sem correção. Pedir uma altitude diferente esfria a coluna em ~3 K. As rodadas planas usam base = 4.322 m, que é correto; as de terreno usam `sondagem_consistente.py`, com base em 3.000 m. A "nuvem super-resfriada persistente" da v1 era artefato desse viés e foi retirada.
* **Coluna ERA5:** livre e estável, com CAPE zero; isoterma de 0 °C a ~5.890 m; vento de 0,4 a 2,8 m/s entre 4 e 8 km. Há ~1.000 J/kg só numa camada de ~80 m junto à superfície, às 12 e 18 UTC.
* **Terreno sem radiação:** sem água super-resfriada; às 12 UTC, só nuvem de encosta quente.
* **Com radiação e fluxos:**
  * `rad_12utc` (completa): nuvem baixa noturna de 0 a −3 °C, sem gelo, sobre o anfiteatro no colapso (10–37 t).
  * `rad_06utc` (analisada só até 19 UTC; foi interrompida às 20:08 UTC): convecção profunda à tarde, chuva 2,5× maior que o IMERG e adiantada 4–6 h. Ascendências espúrias de 50–67 m/s a menos de 1 km do solo sobre encostas íngremes são artefato numérico a descontar. Hallett-Mossop dá 100–165 cristais/L.
* **A pergunta aberta,** e a razão desta rodada: o que acontece entre 20 UTC de 25/08 e o colapso (**02:52 UTC de 26/08**) na `rad_06utc`. Há água super-resfriada sobre o anfiteatro (janela de 3 × 3 km centrada em x = y = 0) nesse intervalo? Quanto? Com que gelo? O `pos/analisar_rad.py` calcula isso; a figura sai em `pos/toro_cm1_radiacao.png`.
* **Referências:**
  * colapso: USGS `us7000tbwb`, Ms 5,2, tipo landslide, 02:52:10 UTC;
  * IMERG até o colapso: 5,09 mm;
  * Himawari: 8.413 km² abaixo de 213 K às 18 UTC → 0 km² às 02:50; 272,7 K sobre o sítio às 02:50.
