# Ordem: teste híbrido MPI 16 × OpenMP 7 no vlab

**Objetivo:** verificar se o CM1 rodando com MPI (16 ranks) × OpenMP (7 threads) no vlab dá os **mesmos campos, byte a byte**, que as rodadas em que confiamos: a referência local e a reprodução `rad_06utc_repro` no vlab, idênticas entre si. Só depois disso a resolução sobe (100 m), porque a 100 m o OpenMP sozinho não basta.

**Não mexer no que está funcionando:** nada em `execucoes/rad_06utc`, `execucoes/rad_06utc_repro`, `reproducao/` ou `cm1/run/cm1.exe` é alterado. O teste vai para `execucoes/rad_06utc_2h_hib16x7`.

## O que o kit traz

`kit_mpi_hibrido.tar.gz` (Drive: `vlab_cache/Himalaia_2026/entrada/`) contém:

* `kit_mpi/cm1.exe`: o executável híbrido, compilado com `mpif90 + OpenMP` (gfortran 13.3), a partir do mesmo código e das mesmas opções da referência;
* `kit_mpi/lib/`: o carregador `ld-linux` e todas as bibliotecas da máquina de referência (glibc 2.39, gfortran, OpenMPI 4.1.6, PMIx 5.0.1, hwloc…);
* `kit_mpi/ompi/` e `kit_mpi/pmix2/`: o OpenMPI e o PMIx relocáveis, com os plugins e os textos de ajuda;
* `mpi_kit.sh`: o lançador. Sobe o `orterun` e cada rank pelo carregador do kit, então nada do sistema do vlab entra. Vem ajustado para contêiner: root permitido, memória compartilhada em `/tmp`, sem cópia única;
* `rodar_hibrido.sh`: prepara o caso de 2 h, testa o lançador, roda e compara;
* `comparar_bits.py`: comparação variável a variável, bit a bit.

Testado no computador de referência:

* o kit não carrega nenhuma biblioteca do sistema (verificado com `LD_DEBUG`);
* 16 ranks × 1 thread dão campos idênticos byte a byte aos da referência OpenMP de 8 threads.

As únicas diferenças são `z0t` e `z0q`. São diagnósticos da camada superficial com memória não inicializada (NaN numa rodada, lixo desnormalizado na outra) e não realimentam o modelo; o comparador os lista à parte.

## Passos (no terminal do vlab)

```bash
cd /home/jovyan/privado/Himalaia_2026/toro_cm1_lhende
export RCLONE_CONFIG=/home/jovyan/privado/.config/rclone/rclone.conf
rclone copy gdrive:vlab_cache/Himalaia_2026/entrada/kit_mpi_hibrido.tar.gz . && rclone copy gdrive:vlab_cache/Himalaia_2026/entrada/kit_mpi_hibrido.tar.gz.sha256 .
sha256sum -c kit_mpi_hibrido.tar.gz.sha256 && tar xzf kit_mpi_hibrido.tar.gz
TESTE=1 bash rodar_hibrido.sh          # 120 s de modelo: so para ver se sobe (alguns minutos)
bash rodar_direto.sh estado            # esperar terminar o teste
bash rodar_hibrido.sh                  # o teste de verdade: 2 h de modelo, 16 x 7
bash rodar_direto.sh estado            # acompanhar
bash rodar_hibrido.sh comparar         # quando terminar
bash relatorio.sh --enviar             # manda o estado para o Drive
```

## Resultado esperado

* **Sucesso:** `RESULTADO: BIT A BIT IDENTICO (exceto diagnosticos z0t/z0q)` nas 5 saídas (0, 30, 60, 90 e 120 min) de `s`, `u`, `v` e `w`. O texto fica em `logs/comparacao_rad_06utc_2h_hib16x7.txt`.
* **Se diferir:** não repetir nem mudar nada. Mandar `logs/comparacao_*.txt`, `logs/hibrido_*.info` e `execucoes/rad_06utc_2h_hib16x7/execucao.info` para o Drive e parar.
* O `cm1out_stats.dat` **não** serve para essa comparação: com MPI, as médias do domínio somam por rank, em outra ordem de soma.

## Se o lançador falhar

* Se a amarração a núcleos falhar, o script tenta de novo sem amarração (`BIND=none`); isso muda só a velocidade, não o resultado.
* Se o `orterun` não subir de jeito nenhum, mandar `logs/mpi_teste_*.err` e parar. Não instalar OpenMPI nem conda para contornar.
