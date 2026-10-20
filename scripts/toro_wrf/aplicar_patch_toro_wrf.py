# -*- coding: utf-8 -*-
"""
Aplica o "modo super-resfriado" e o vortice dinamico (module_toro_wrf) a uma COPIA do WRF v4.7.1 (commit f52c197):
so acrescenta linhas, em phys/module_mp_nssl_2mom.F, phys/module_microphysics_driver.F, phys/module_pbl_driver.F e
main/depend.common (o PBL passa a depender do arquivo do NSSL). O module_toro_wrf entra no proprio arquivo do
NSSL, antes do modulo original, para nao mexer em Makefiles.
Cada insercao confere que a ancora aparece uma unica vez; se algo nao bater, para sem gravar nada.
Os trechos inseridos so executam com toro_call = .true. (arquivo toro_wrf.txt presente e lido).

Uso: python3 aplicar_patch_toro_wrf.py <dir_WRF> <caminho/module_toro_wrf.F>
"""
import os
import shutil
import sys

WRF, MOD = sys.argv[1], sys.argv[2]
SHA_ESPERADO = {"phys/module_mp_nssl_2mom.F": "29f42e76fbeca027a3ffb2ac805b148aaa1425c7f99ed1d8f19a90ebc1d015f8",
                "phys/module_microphysics_driver.F": "3a840534acbb42cb723e53f60ea3e9f20f284daa4c095ab106a2c0aa5ca70f72",
                "phys/module_pbl_driver.F": "42ff53571ba1fb926fa6063108806d9a2f8ff5fdd1fa2ecfc1fdde60f2bf65fb",
                "main/depend.common": "2eb1406426469b6b4c6277ce0ecc81af85d8a60ccb65ecd5c9d3c8cedb79b26f"}


def sha(p):
    import hashlib
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def troca(texto, ancora, novo, nome, depois=True):
    n = texto.count(ancora)
    if n != 1:
        sys.exit("ERRO: ancora de '%s' aparece %d vezes" % (nome, n))
    return texto.replace(ancora, ancora + novo if depois else novo + ancora)


for f, h in SHA_ESPERADO.items():
    if sha(os.path.join(WRF, f)) != h:
        sys.exit("ERRO: %s nao e o v4.7.1 esperado (sha256 diferente); nada gravado" % f)

IJ = "igs(mgs)+its-1, jyslab"
arq = {f: open(os.path.join(WRF, f), encoding="latin-1", newline="").read() for f in SHA_ESPERADO}
modsrc = open(MOD, encoding="latin-1").read()

# ---------------- NSSL ----------------
t = arq["phys/module_mp_nssl_2mom.F"]
t = troca(t, "\nMODULE module_mp_nssl_2mom\n", "\n" + modsrc + "\n", "modulo toro_wrf antes do NSSL", depois=False)
t = troca(t, "\nMODULE module_mp_nssl_2mom\n",
          "  USE module_toro_wrf, ONLY: toro_call, toro_f, toro_fnuc, toro_fwfrz   ! toro_wrf (modo super-resfriado)\n",
          "use no NSSL")
t = troca(t, "      integer jyslab,its,ids,ide,jds,jde ! domain boundaries\n",
          "      real :: tfator   ! toro_wrf\n", "declaracao em nssl_2mom_gs")
# coalescencia e acrecao (chuva quente)
t = troca(t, "      ENDIF  !  ( ipconc .ge. 2 )\n", """
! toro_wrf: Estado A -- autoconversao/autocoleta (fcoal) e acrecao de goticulas pela chuva (faccr)
      IF ( toro_call ) THEN
        DO mgs = 1,ngscnt
          tfator = toro_f(1, %s)
          qrcnw(mgs) = tfator*qrcnw(mgs)
          crcnw(mgs) = tfator*crcnw(mgs)
          zrcnw(mgs) = tfator*zrcnw(mgs)
          cautn(mgs) = tfator*cautn(mgs)
          tfator = toro_f(2, %s)
          qracw(mgs) = tfator*qracw(mgs)
          cracw(mgs) = tfator*cracw(mgs)
        ENDDO
      ENDIF
""" % (IJ, IJ), "coalescencia")
# congelamento por contato
t = troca(t, "         qwctfz(mgs) = min(qwctfz(mgs),qcmxd(mgs))\n        ENDIF\n", """! toro_wrf: Estado A -- congelamento por contato (fctfz)
        IF ( toro_call ) THEN
          tfator = toro_f(3, %s)
          cwctfz(mgs) = tfator*cwctfz(mgs)
          qwctfz(mgs) = tfator*qwctfz(mgs)
        ENDIF
""" % IJ, "contato")
# congelamento de goticulas (Bigg) acima de t_hom_c
t = troca(t, "        if ( xplate(mgs) .eq. 1 ) then\n          qwfrzp(mgs) = qwfrz(mgs)\n", """! toro_wrf: Estado A -- congelamento de goticulas (Bigg) acima de t_hom_c (fwfrz); o homogeneo fica intacto
        IF ( toro_call ) THEN
          tfator = toro_fwfrz(%s, temg(mgs))
          qwfrz(mgs) = tfator*qwfrz(mgs)
          cwfrz(mgs) = tfator*cwfrz(mgs)
        ENDIF
""" % IJ, "Bigg", depois=False)
# Hallett-Mossop
t = troca(t, "        qsplinter(mgs) = Min(0.1*qiacr(mgs), csplinter(mgs)*splintermass/rho0(mgs) ) ! makes splinters smaller if too much mass is taken from graupel\n",
          """! toro_wrf: Estado A -- Hallett-Mossop (fhm)
        IF ( toro_call ) THEN
          tfator = toro_f(5, %s)
          csplinter(mgs) = tfator*csplinter(mgs)
          qsplinter(mgs) = tfator*qsplinter(mgs)
        ENDIF
""" % IJ, "Hallett-Mossop")
# congelamento da chuva (Bigg e por colisao com gelo/neve), depois da correcao qrzfac
t = troca(t, "       viacrf(mgs)  = qrzfac(mgs)*viacrf(mgs)\n      end if\n      end do\n!\n!\n!\n      end if\n", """
! toro_wrf: Estado A -- congelamento da chuva e coleta de chuva por gelo e neve (frfrz)
      IF ( toro_call ) THEN
        DO mgs = 1,ngscnt
          tfator = toro_f(6, %s)
          qrfrz(mgs)  = tfator*qrfrz(mgs)
          qrfrzs(mgs) = tfator*qrfrzs(mgs)
          qrfrzf(mgs) = tfator*qrfrzf(mgs)
          crfrz(mgs)  = tfator*crfrz(mgs)
          crfrzf(mgs) = tfator*crfrzf(mgs)
          crfrzs(mgs) = tfator*crfrzs(mgs)
          qiacr(mgs)  = tfator*qiacr(mgs)
          qiacrf(mgs) = tfator*qiacrf(mgs)
          qiacrs(mgs) = tfator*qiacrs(mgs)
          ciacr(mgs)  = tfator*ciacr(mgs)
          ciacrf(mgs) = tfator*ciacrf(mgs)
          ciacrs(mgs) = tfator*ciacrs(mgs)
          qsacr(mgs)  = tfator*qsacr(mgs)
          vrfrzf(mgs) = tfator*vrfrzf(mgs)
          viacrf(mgs) = tfator*viacrf(mgs)
        ENDDO
      ENDIF
""" % IJ, "congelamento da chuva")
# nucleacao primaria (Estado A: fnuc; liberacao: fnuc_rel na coluna do aerossol)
t = troca(t, "      if ( xplate(mgs) .eq. 1 ) then\n      qipipnt(mgs) = qiint(mgs)\n", """! toro_wrf: nucleacao primaria -- fnuc no Estado A; fnuc_rel na coluna do aerossol (liberacao)
      IF ( toro_call ) THEN
        tfator = toro_fnuc(%s)
        qiint(mgs) = tfator*qiint(mgs)
        ciint(mgs) = tfator*ciint(mgs)
      ENDIF
""" % IJ, "nucleacao primaria", depois=False)
arq["phys/module_mp_nssl_2mom.F"] = t

# ---------------- driver ----------------
t = arq["phys/module_microphysics_driver.F"]
t = troca(t, "   USE module_mp_nssl_2mom\n", "   USE module_toro_wrf, ONLY: toro_wrf_prepara   ! toro_wrf\n", "use no driver")
t = troca(t, "\n         CALL nssl_2mom_driver(                          &\n", """
! toro_wrf: hora e mascaras do modo super-resfriado neste dominio e bloco (inerte sem toro_wrf.txt)
         IF ( PRESENT(id) .AND. PRESENT(xtime) .AND. PRESENT(gmt) .AND. PRESENT(xlat) .AND. PRESENT(xlong) ) THEN
           CALL toro_wrf_prepara(id, xtime, gmt, xlat, xlong, ims, ime, jms, jme, its, ite, jts, jte)
         ENDIF
""", "chamada no driver", depois=False)
arq["phys/module_microphysics_driver.F"] = t

# ---------------- driver da camada limite: vortice dinamico ----------------
t = arq["phys/module_pbl_driver.F"]
t = troca(t, "   USE module_bl_ysu\n", "   USE module_toro_wrf, ONLY: toro_vortice   ! toro_wrf: vortice dinamico\n", "use no PBL")
t = troca(t, "     IF (distributed_ahe_opt == 1) THEN\n", """! toro_wrf: vortice dinamico (forca tangencial ciclonica em RUBLTEN/RVBLTEN) -- inerte sem toro_wrf.txt
     IF ( PRESENT(id) .AND. PRESENT(xlat_u) .AND. PRESENT(xlong_u) ) THEN
       CALL toro_vortice(id, gmt, xtime, xlat_u, xlong_u, z, ht, rublten, rvblten, &
                         ims, ime, jms, jme, kms, kme, its, ite, jts, jte, kts, kte)
     ENDIF
""", "chamada do vortice no PBL", depois=False)
arq["phys/module_pbl_driver.F"] = t

# ---------------- dependencia: o PBL usa o module_toro_wrf, que esta no arquivo do NSSL ----------------
t = arq["main/depend.common"]
t = troca(t, "module_pbl_driver.o: \\\n", "\tmodule_mp_nssl_2mom.o \\\n", "depend.common")
arq["main/depend.common"] = t

for f, txt in arq.items():
    p = os.path.join(WRF, f)
    shutil.copy2(p, p + ".antes_toro")
    open(p, "w", encoding="latin-1", newline="").write(txt)
print("patch toro_wrf aplicado em", WRF)
