# -*- coding: utf-8 -*-
"""
Aplica o patch do "toro" (toro_mod: anti-coalescencia de Tinsley + vortice imposto) a uma COPIA do
codigo do CM1 r21.1 (ja com o patch initsfc=5). Cada insercao confere que o trecho-ancora existe uma
unica vez; se algo nao bater, para sem gravar nada. Os fontes do CM1 vem com CRLF: o texto e
normalizado para LF durante a troca e gravado de volta com o fim de linha original.

Uso: python3 aplicar_patch_toro.py <dir_src_do_cm1> <caminho/toro_mod.F>
"""
import os
import shutil
import sys

SRC, TORO = sys.argv[1], sys.argv[2]
CR = chr(13)
LF = chr(10)


def troca(texto, ancora, novo, nome, depois=True):
    n = texto.count(ancora)
    if n != 1:
        sys.exit("ERRO: ancora de '%s' aparece %d vezes" % (nome, n))
    return texto.replace(ancora, ancora + novo if depois else novo + ancora)


arqs, crlf = {}, {}
for f in ("module_mp_nssl_2mom.F", "solve1.F", "Makefile"):
    bruto = open(os.path.join(SRC, f), encoding="latin-1", newline="").read()
    crlf[f] = (CR + LF) in bruto
    arqs[f] = bruto.replace(CR + LF, LF)

# ---------------- NSSL ----------------
t = arqs["module_mp_nssl_2mom.F"]
t = troca(t, "\nMODULE module_mp_nssl_2mom\n",
          "  use toro_mod, only: toro_ativo, toro_fc, toro_fa, toro_ft   ! toro: anti-coalescencia (Tinsley)\n",
          "nssl use")
t = troca(t, "      ENDIF  !  ( ipconc .ge. 2 )\n",
          """
! toro (toro_mod): Estado A da anti-varredura -- autoconversao/autocoleta (fcoal) e acrecao (faccr)
      IF ( toro_ativo ) THEN
        DO mgs = 1,ngscnt
          qrcnw(mgs) = toro_fc(real(qx(mgs,lh)))*qrcnw(mgs)
          crcnw(mgs) = toro_fc(real(qx(mgs,lh)))*crcnw(mgs)
          zrcnw(mgs) = toro_fc(real(qx(mgs,lh)))*zrcnw(mgs)
          cautn(mgs) = toro_fc(real(qx(mgs,lh)))*cautn(mgs)
          qracw(mgs) = toro_fa(real(qx(mgs,lh)))*qracw(mgs)
          cracw(mgs) = toro_fa(real(qx(mgs,lh)))*cracw(mgs)
        ENDDO
      ENDIF
""", "nssl coalescencia")
anc_ct = """         qwctfz(mgs) = min(qwctfz(mgs),qcmxd(mgs))
        ENDIF
"""
t = troca(t, anc_ct, """! toro (toro_mod): congelamento por contato (fctfz)
        IF ( toro_ativo .and. ipconc .ge. 2 ) THEN
         cwctfz(mgs) = Min( toro_ft(real(qx(mgs,lh)))*cwctfz(mgs), ccmxd(mgs) )
         qwctfz(mgs) = xmas(mgs,lc)*cwctfz(mgs)/rho0(mgs)
        ENDIF
""", "nssl contato")
arqs["module_mp_nssl_2mom.F"] = t

# ---------------- solve1: vortice ----------------
t = arqs["solve1.F"]
t = troca(t, "      use lsnudge_module\n", "      use toro_mod   ! toro: vortice imposto\n", "solve1 use")
t = troca(t, "      real :: umod,uref,zref,oldval,newval\n", "      real :: tvx,tvy,tvr,tvs,tvh   ! toro\n", "solve1 decl")
t = troca(t, "      timenudge = mtime+dt\n", "      call toro_atualiza(mtime,myid)   ! toro: le toro_params.txt na 1a chamada\n\n",
          "solve1 atualiza", depois=False)
bloco_u = """      ! toro (toro_mod): vortice imposto -- componente x da forca tangencial
      IF( toro_ativo .and. ivortex.eq.1 .and. gamm_v.gt.0.0 )THEN
        !$omp parallel do default(shared)  &
        !$omp private(i,j,k,tvx,tvy,tvr,tvs,tvh)
        do k=1,nk
        do j=1,nj
        do i=1,ni+1
          tvx = xf(i)-xc_v
          tvy = yh(j)-yc_v
          tvr = sqrt(tvx*tvx+tvy*tvy)
          if( tvr.gt.1.0 )then
            tvh = 0.5*(zh(i-1,j,k)+zh(i,j,k)) - 0.5*(zs(i-1,j)+zs(i,j))
            tvs = gamm_v*alpha_v*(tvr/rmax_v)*exp(1.0-tvr/rmax_v)*(cosh(tvh/zr_v))**(-2)
            uten1(i,j,k) = uten1(i,j,k) - tvs*tvy/tvr
          endif
        enddo
        enddo
        enddo
      ENDIF
"""
t = troca(t, "      if(timestats.ge.1) time_rdamp=time_rdamp+mytime()\n\n      if( use_pbl )then\n        if( axisymm.eq.1 )then\n          ip = 2",
          bloco_u, "solve1 vortice u", depois=False)
bloco_v = """
      ! toro (toro_mod): vortice imposto -- componente y da forca tangencial
      IF( toro_ativo .and. ivortex.eq.1 .and. gamm_v.gt.0.0 )THEN
        !$omp parallel do default(shared)  &
        !$omp private(i,j,k,tvx,tvy,tvr,tvs,tvh)
        do k=1,nk
        do j=1,nj+1
        do i=1,ni
          tvx = xh(i)-xc_v
          tvy = yf(j)-yc_v
          tvr = sqrt(tvx*tvx+tvy*tvy)
          if( tvr.gt.1.0 )then
            tvh = 0.5*(zh(i,j-1,k)+zh(i,j,k)) - 0.5*(zs(i,j-1)+zs(i,j))
            tvs = gamm_v*alpha_v*(tvr/rmax_v)*exp(1.0-tvr/rmax_v)*(cosh(tvh/zr_v))**(-2)
            vten1(i,j,k) = vten1(i,j,k) + tvs*tvx/tvr
          endif
        enddo
        enddo
        enddo
      ENDIF
"""
t = troca(t, "!--------------------------------------------------------------------\n!  V-equation\n", bloco_v, "solve1 vortice v")
arqs["solve1.F"] = t

# ---------------- Makefile ----------------
t = arqs["Makefile"]
t = troca(t, "\tmodule_mp_nssl_2mom.F \\\n", "\ttoro_mod.F \\\n", "Makefile SRC", depois=False)
t = troca(t, "solve1.o: constants.o input.o bc.o diff2.o turbtend.o misclibs.o testcase_simple_phys.o eddy_recycle.o lsnudge.o",
          " toro_mod.o", "Makefile solve1")
t = t.rstrip("\n") + "\nmodule_mp_nssl_2mom.o: toro_mod.o\n"
arqs["Makefile"] = t

for f, txt in arqs.items():
    shutil.copy2(os.path.join(SRC, f), os.path.join(SRC, f + ".antes_toro"))
    saida = txt.replace(LF, CR + LF) if crlf[f] else txt
    open(os.path.join(SRC, f), "w", encoding="latin-1", newline="").write(saida)
shutil.copy2(TORO, os.path.join(SRC, "toro_mod.F"))
print("patch do toro aplicado em", SRC)
