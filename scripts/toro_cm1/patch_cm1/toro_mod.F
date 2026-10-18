!-----------------------------------------------------------------------
!  toro_mod -- experimentos do "toro" (Lhende Khola, 25-26/08/2026).
!  DESLIGADO POR PADRAO: so atua se existir 'toro_params.txt' (namelist &toro)
!  no diretorio da rodada. Sem o arquivo, nenhum calculo do CM1 muda.
!
!  Microfisica NSSL -- hipotese de anti-varredura eletrica (Tinsley):
!  "Estado A" (nuvem carregada, eletrificacao fraca): coalescencia e congelamento
!  por contato suprimidos, a agua super-resfriada fica retida;
!  "Estado B" (reversao): "o aparecimento de graupel e a reversao" -- a varredura liga.
!    fcoal : fator na autoconversao e autocoleta de goticulas (qrcnw, crcnw, zrcnw, cautn)
!    faccr : fator na acrecao de goticulas pela chuva (qracw, cracw)
!    fctfz : fator no congelamento por contato de goticulas (cwctfz, qwctfz)
!    *_pos : fatores fora do Estado A (Estado B; 1 = microfisica padrao)
!    Estado A vale entre t1_mp e t2_mp (s de modelo) e:
!      modo_mp = 1 : em todo o dominio
!      modo_mp = 2 : so onde nao ha graupel (qg < qg_rev, kg/kg); onde ha, Estado B
!
!  Vortice imposto (forca tangencial; ciclonico se alpha_v > 0):
!    centro (xc_v, yc_v) [m], raio rmax_v [m], perfil radial (r/R) exp(1 - r/R),
!    perfil vertical sech^2(h/zr_v), h = altura sobre o relevo [m],
!    intensidade alpha_v [m/s2]; liga em t1_v com rampa linear de tr_v [s];
!    desliga em t2_v.
!
!  Gelo vindo de cima (semeadura; iseed = 1): fonte de massa sq_s [kg/kg/s] e de numero
!    sn_s [#/kg/s] na especie (nq_s, nn_s) do vetor qa (NSSL ptype 27: 4 = qi, 11 = cci;
!    5 = qs, 12 = csw), num cilindro de raio r_s [m] em torno de (xc_s, yc_s), entre z1_s e
!    z2_s [m ASL; zbase_s = cota da base do modelo], de t1_s a t2_s [s de modelo].
!-----------------------------------------------------------------------
module toro_mod
  implicit none
  logical, save :: toro_lido = .false., toro_ativo = .false.
  integer, save :: modo_mp = 1
  real, save :: fcoal = 1.0, faccr = 1.0, fctfz = 1.0
  real, save :: fcoal_pos = 1.0, faccr_pos = 1.0, fctfz_pos = 1.0
  real, save :: t1_mp = 0.0, t2_mp = 0.0, qg_rev = 1.0e-6
  integer, save :: ivortex = 0
  real, save :: xc_v = 0.0, yc_v = 0.0, rmax_v = 2000.0, zr_v = 2000.0
  real, save :: alpha_v = 0.0, t1_v = 0.0, t2_v = 0.0, tr_v = 1800.0
  integer, save :: iseed = 0, nq_s = 4, nn_s = 11
  real, save :: xc_s = 0.0, yc_s = 0.0, r_s = 4000.0, z1_s = 5500.0, z2_s = 7500.0, zbase_s = 3000.0
  real, save :: t1_s = 0.0, t2_s = 0.0, sq_s = 0.0, sn_s = 0.0
  ! estado no instante corrente (toro_atualiza, chamado a cada passo, fora de regiao paralela)
  logical, save :: mp_A = .false., seed_on = .false.
  real, save :: gamm_v = 0.0
  namelist /toro/ modo_mp, fcoal, faccr, fctfz, fcoal_pos, faccr_pos, fctfz_pos,  &
                  t1_mp, t2_mp, qg_rev, ivortex, xc_v, yc_v, rmax_v, zr_v,        &
                  alpha_v, t1_v, t2_v, tr_v,                                      &
                  iseed, nq_s, nn_s, xc_s, yc_s, r_s, z1_s, z2_s, zbase_s,        &
                  t1_s, t2_s, sq_s, sn_s

contains

  subroutine toro_ler(myid)
    integer, intent(in) :: myid
    logical :: existe
    integer :: un, ios
    toro_lido = .true.
    inquire(file='toro_params.txt', exist=existe)
    if (.not. existe) return
    open(newunit=un, file='toro_params.txt', status='old', action='read', iostat=ios)
    if (ios /= 0) return
    read(un, nml=toro, iostat=ios)
    close(un)
    if (ios /= 0) then
      if (myid == 0) print *, 'TORO: erro lendo toro_params.txt (iostat =', ios, '); experimento DESLIGADO'
      return
    endif
    toro_ativo = .true.
    if (myid == 0) then
      print *, 'TORO: toro_params.txt lido -- experimento LIGADO'
      write(*, nml=toro)
    endif
  end subroutine toro_ler

  subroutine toro_atualiza(mtime, myid)
    double precision, intent(in) :: mtime
    integer, intent(in) :: myid
    if (.not. toro_lido) call toro_ler(myid)
    if (.not. toro_ativo) return
    mp_A = (mtime >= dble(t1_mp) .and. mtime < dble(t2_mp))
    gamm_v = 0.0
    if (ivortex == 1 .and. mtime >= dble(t1_v) .and. mtime < dble(t2_v)) &
      gamm_v = real(min(1.0d0, (mtime - dble(t1_v)) / dble(max(tr_v, 1.0))))
    seed_on = (iseed == 1 .and. mtime >= dble(t1_s) .and. mtime < dble(t2_s))
  end subroutine toro_atualiza

  ! fatores no ponto (puras: seguras dentro de regioes paralelas)
  pure logical function toro_estadoA(qg)
    real, intent(in) :: qg
    toro_estadoA = mp_A .and. (modo_mp /= 2 .or. qg < qg_rev)
  end function toro_estadoA

  pure real function toro_fc(qg)
    real, intent(in) :: qg
    if (toro_estadoA(qg)) then
      toro_fc = fcoal
    else
      toro_fc = fcoal_pos
    endif
  end function toro_fc

  pure real function toro_fa(qg)
    real, intent(in) :: qg
    if (toro_estadoA(qg)) then
      toro_fa = faccr
    else
      toro_fa = faccr_pos
    endif
  end function toro_fa

  pure real function toro_ft(qg)
    real, intent(in) :: qg
    if (toro_estadoA(qg)) then
      toro_ft = fctfz
    else
      toro_ft = fctfz_pos
    endif
  end function toro_ft

end module toro_mod
