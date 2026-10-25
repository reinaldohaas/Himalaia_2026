!
! module_toro_wrf -- "modo super-resfriado" (Estado A da anti-varredura de Tinsley) para a microfisica NSSL
! de 2 momentos do WRF, um vortice dinamico imposto e a nucleacao secundaria iniciada no nucleo do vortice.
!
! Configuracao: grupo &toro_wrf no proprio namelist.input (o WRF ignora grupos que nao conhece) ou, na forma
! antiga, no arquivo toro_wrf.txt. Sem grupo (ou com ligado = .false.) o modulo fica INERTE: nenhum fator e
! aplicado e o WRF reproduz bit a bit a rodada original. Um so executavel faz os experimentos:
!   A = sem grupo;  B = Estado A;  C = B + vortice + nucleacao no nucleo inteiro (disparo_w = .false.,
!   nucleo_no_estado_A = .false.);  D = como C, mas o nucleo so nucleia onde w > w_crit (padroes .true.).
!   E = como D, com o vortice em niveis medios (perfil_v = 1: gaussiana em z ASL centrada em zc_v_m, meia-largura
!   zw_v_m) e o disparo restrito a faixa de temperatura t_nuc_min_c < T < t_nuc_max_c (C), p. ex. -8 a -3 (Hallett-Mossop).
!   Padroes: perfil_v = 0 (sech^2 a partir do chao) e faixa -999 a 0 C, que reproduzem A-D bit a bit.
!
! Estado A (t_ini <= t < t_rel, dentro de raio_km do centro (lat0,lon0), nos dominios marcados em dominios):
!   fcoal  autoconversao e autocoleta de goticulas (qrcnw, crcnw, cautn)          -> chuva quente
!   faccr  acrecao de goticulas pela chuva (qracw, cracw)                            -> chuva quente
!   fctfz  congelamento por contato (cwctfz, qwctfz)
!   fnuc   nucleacao primaria de gelo (ciint, qiint)
!   fhm    multiplicacao de gelo por Hallett-Mossop (csplinter, qsplinter)
!   frfrz  congelamento de gotas de chuva (qrfrz, crfrz) e por colisao com gelo (qiacrf, ciacrf)
!   fwfrz  congelamento de goticulas (Bigg) acima de t_hom_c; abaixo de t_hom_c (padrao -38 C) fica intacto
! Liberacao por tempo (t_rel <= t < t_rel + t_dur): fisica normal em todo lugar e, numa coluna de raio_aer_km em
!   torno de (lat_aer,lon_aer), a nucleacao primaria multiplicada por fnuc_rel.
! Vortice dinamico (ivortex = 1; t_v_ini <= t < t_v_fim, rampa de tr_v horas; dominios_v): forca tangencial
!   ciclonica F = gamm*alpha_v*(r/rmax)*exp(1 - r/rmax)*sech^2(h/zr_v), somada a RUBLTEN/RVBLTEN (m s-2) no driver
!   da camada limite; r = distancia a (lat_v,lon_v); h = altura acima do terreno.
! Nucleacao secundaria iniciada pelo vortice (t_vn_ini <= t < t_v_fim, a ate raio_vn_km de (lat_v,lon_v)):
!   no nucleo, ONDE A ASCENDENTE CHEGA (w > w_crit, agua liquida qc+qr > q_crit e T < 0 C), o Estado A e
!   levantado (fatores = 1), o Hallett-Mossop e multiplicado por fhm_v e a nucleacao primaria por fnuc_v (o
!   aerossol trazido pelo vortice). No resto do nucleo e fora dele o Estado A continua (versao D).
! Tempo t em horas desde 25/08/2026 00 UTC: t = gmt + xtime/60 (todos os dominios comecam em 25/08).
! Tiles: supoe OMP_NUM_THREADS = 1 (as mascaras sao do modulo, recalculadas a cada chamada de tile).
!
MODULE module_toro_wrf
  IMPLICIT NONE
  PRIVATE
  PUBLIC :: toro_wrf_prepara, toro_vortice, toro_call, toro_f, toro_fnuc, toro_fwfrz

  LOGICAL, SAVE :: lido = .false., ativo = .false.
  LOGICAL, SAVE :: toro_call = .false.
  REAL,    SAVE :: t_ini = 17.0, t_rel = 26.25, t_dur = 0.5
  REAL,    SAVE :: lat0 = 28.271, lon0 = 85.515, raio_km = 150.0
  REAL,    SAVE :: fcoal = 0.0, faccr = 0.0, fctfz = 0.0, fnuc = 0.0, fhm = 0.0, frfrz = 0.0, fwfrz = 0.0
  REAL,    SAVE :: t_hom_c = -38.0
  REAL,    SAVE :: lat_aer = 28.271, lon_aer = 85.515, raio_aer_km = 5.0, fnuc_rel = 100.0
  INTEGER, SAVE :: dominios(3) = (/ 0, 1, 1 /)
  ! vortice dinamico e nucleacao no nucleo
  INTEGER, SAVE :: ivortex = 0
  REAL,    SAVE :: t_v_ini = 25.0, t_v_fim = 27.0, tr_v = 0.5
  REAL,    SAVE :: lat_v = 28.271, lon_v = 85.515, rmax_v_km = 5.0, zr_v_m = 3000.0, alpha_v = 1.0e-2
  INTEGER, SAVE :: dominios_v(3) = (/ 0, 0, 1 /)
  REAL,    SAVE :: t_vn_ini = 25.5, raio_vn_km = 5.0, fhm_v = 10.0, fnuc_v = 100.0
  REAL,    SAVE :: w_crit = 2.0, q_crit = 1.0e-5       ! disparo no nucleo: m/s e kg/kg
  LOGICAL, SAVE :: avisou_disparo = .false.
  LOGICAL, SAVE :: ligado = .true.               ! .false. desliga o modulo mesmo com o grupo presente
  LOGICAL, SAVE :: disparo_w = .true.            ! D: nucleacao no nucleo so onde w > w_crit; .false. = C
  LOGICAL, SAVE :: nucleo_no_estado_A = .true.   ! D: o nucleo segue no Estado A fora do disparo; .false. = C
  INTEGER, SAVE :: perfil_v = 0                  ! 0: sech^2(h/zr_v_m) a partir do chao; 1: gaussiana em z ASL (E)
  REAL,    SAVE :: zc_v_m = 7500.0, zw_v_m = 1500.0   ! perfil_v = 1: altitude do maximo e meia-largura (m)
  REAL,    SAVE :: t_nuc_min_c = -999.0, t_nuc_max_c = 0.0   ! faixa de T (C) do disparo no nucleo
  LOGICAL, ALLOCATABLE, SAVE :: msup(:,:), maer(:,:), mvn(:,:)

  NAMELIST /toro_wrf/ t_ini, t_rel, t_dur, lat0, lon0, raio_km, fcoal, faccr, fctfz, fnuc, fhm, frfrz, fwfrz, &
                      t_hom_c, lat_aer, lon_aer, raio_aer_km, fnuc_rel, dominios, &
                      ivortex, t_v_ini, t_v_fim, tr_v, lat_v, lon_v, rmax_v_km, zr_v_m, alpha_v, dominios_v, &
                      t_vn_ini, raio_vn_km, fhm_v, fnuc_v, w_crit, q_crit, &
                      ligado, disparo_w, nucleo_no_estado_A, perfil_v, zc_v_m, zw_v_m, t_nuc_min_c, t_nuc_max_c

CONTAINS

  ! o arquivo tem uma linha que comeca com &toro_wrf (sem distinguir maiusculas)?
  LOGICAL FUNCTION tem_grupo(arq)
    CHARACTER(len=*), INTENT(IN) :: arq
    CHARACTER(len=512) :: linha
    INTEGER :: iu, ios, k, c
    LOGICAL :: existe
    tem_grupo = .false.
    INQUIRE( FILE=arq, EXIST=existe )
    IF ( .not. existe ) RETURN
    OPEN( NEWUNIT=iu, FILE=arq, STATUS='old', ACTION='read', IOSTAT=ios )
    DO WHILE ( ios == 0 .and. .not. tem_grupo )
      READ( iu, '(a)', IOSTAT=ios ) linha
      IF ( ios /= 0 ) EXIT
      linha = adjustl(linha)
      DO k = 1, 9
        c = ichar(linha(k:k)); IF ( c >= 65 .and. c <= 90 ) linha(k:k) = char(c + 32)
      ENDDO
      tem_grupo = ( linha(1:9) == '&toro_wrf' )
    ENDDO
    CLOSE( iu )
  END FUNCTION tem_grupo

  SUBROUTINE le_config()
    INTEGER :: iu, ios
    CHARACTER(len=32) :: fonte
    IF ( lido ) RETURN
    lido = .true.
    IF ( tem_grupo('namelist.input') ) THEN
      fonte = 'namelist.input'
    ELSEIF ( tem_grupo('toro_wrf.txt') ) THEN
      fonte = 'toro_wrf.txt'
    ELSE
      RETURN                                     ! experimento A: modulo inerte
    ENDIF
    OPEN( NEWUNIT=iu, FILE=trim(fonte), STATUS='old', ACTION='read', IOSTAT=ios )
    IF ( ios == 0 ) READ( iu, NML=toro_wrf, IOSTAT=ios )
    CLOSE( iu )
    IF ( ios /= 0 ) THEN
      WRITE(0,'(a)') 'toro_wrf: ERRO lendo &toro_wrf em ' // trim(fonte) // ' -- modulo INATIVO'
      RETURN
    ENDIF
    ativo = ligado
    IF ( .not. ativo ) WRITE(0,'(a)') 'toro_wrf: grupo &toro_wrf com ligado = .false. em ' // trim(fonte) // ' -- modulo INATIVO'
    IF ( ativo ) WRITE(0,'(a)') 'toro_wrf: modo super-resfriado ATIVO (' // trim(fonte) // ' lido)'
    IF ( ativo .and. ivortex == 1 ) WRITE(0,'(a)') 'toro_wrf: vortice dinamico LIGADO'
    IF ( ativo .and. ivortex == 1 ) WRITE(0,'(a,l1,a,l1)') 'toro_wrf: disparo_w = ', disparo_w, &
                                                          ', nucleo_no_estado_A = ', nucleo_no_estado_A
    IF ( ativo .and. ivortex == 1 .and. perfil_v == 1 ) WRITE(0,'(a,f7.0,a,f6.0,a)') &
      'toro_wrf: perfil do vortice em niveis medios: maximo a ', zc_v_m, ' m ASL, meia-largura ', zw_v_m, ' m'
    IF ( ativo .and. ivortex == 1 .and. t_nuc_min_c > -900.0 ) WRITE(0,'(a,f6.1,a,f6.1,a)') &
      'toro_wrf: disparo so com ', t_nuc_min_c, ' < T < ', t_nuc_max_c, ' C'
  END SUBROUTINE le_config

  REAL FUNCTION dist_km(la, lo, la0, lo0)
    REAL, INTENT(IN) :: la, lo, la0, lo0
    dist_km = 111.32*sqrt( (la-la0)**2 + ((lo-lo0)*cos(la*0.0174533))**2 )
  END FUNCTION dist_km

  SUBROUTINE toro_wrf_prepara(id, xtime, gmt, xlat, xlong, ims, ime, jms, jme, its, ite, jts, jte)
    INTEGER, INTENT(IN) :: id, ims, ime, jms, jme, its, ite, jts, jte
    REAL,    INTENT(IN) :: xtime, gmt
    REAL,    INTENT(IN) :: xlat(ims:ime, jms:jme), xlong(ims:ime, jms:jme)
    INTEGER :: i, j
    REAL :: th
    LOGICAL :: em_vn
    CALL le_config()
    toro_call = .false.
    IF ( .not. ativo ) RETURN
    IF ( id < 1 .or. id > 3 ) RETURN
    IF ( dominios(id) /= 1 ) RETURN
    th = gmt + xtime/60.0
    em_vn = ( ivortex == 1 .and. dominios_v(id) == 1 .and. th >= t_vn_ini .and. th < t_v_fim )
    IF ( ( th < t_ini .or. th >= t_rel + t_dur ) .and. .not. em_vn ) RETURN
    IF ( allocated(msup) ) THEN
      IF ( lbound(msup,1) /= ims .or. ubound(msup,1) /= ime .or. lbound(msup,2) /= jms .or. ubound(msup,2) /= jme ) THEN
        DEALLOCATE( msup, maer, mvn )
      ENDIF
    ENDIF
    IF ( .not. allocated(msup) ) ALLOCATE( msup(ims:ime, jms:jme), maer(ims:ime, jms:jme), mvn(ims:ime, jms:jme) )
    msup = .false. ; maer = .false. ; mvn = .false.
    DO j = jts, jte
      DO i = its, ite
        IF ( em_vn ) mvn(i,j) = ( dist_km(xlat(i,j), xlong(i,j), lat_v, lon_v) <= raio_vn_km )
        IF ( th >= t_ini .and. th < t_rel ) THEN
          msup(i,j) = ( dist_km(xlat(i,j), xlong(i,j), lat0, lon0) <= raio_km ) .and. &
                      ( nucleo_no_estado_A .or. .not. mvn(i,j) )
        ELSEIF ( th >= t_rel .and. th < t_rel + t_dur ) THEN
          maer(i,j) = ( dist_km(xlat(i,j), xlong(i,j), lat_aer, lon_aer) <= raio_aer_km )
        ENDIF
      ENDDO
    ENDDO
    toro_call = any(msup) .or. any(maer) .or. any(mvn)
  END SUBROUTINE toro_wrf_prepara

  ! vortice dinamico: forca tangencial ciclonica somada a rublten/rvblten (m s-2, pontos de massa)
  SUBROUTINE toro_vortice(id, gmt, xtime, xlat_u, xlong_u, z, ht, rublten, rvblten, &
                          ims, ime, jms, jme, kms, kme, its, ite, jts, jte, kts, kte)
    INTEGER, INTENT(IN) :: id, ims, ime, jms, jme, kms, kme, its, ite, jts, jte, kts, kte
    REAL,    INTENT(IN) :: gmt, xtime
    REAL,    INTENT(IN) :: xlat_u(ims:ime, jms:jme), xlong_u(ims:ime, jms:jme)
    REAL,    INTENT(IN) :: z(ims:ime, kms:kme, jms:jme), ht(ims:ime, jms:jme)
    REAL,    INTENT(INOUT) :: rublten(ims:ime, kms:kme, jms:jme), rvblten(ims:ime, kms:kme, jms:jme)
    INTEGER :: i, j, k
    REAL :: th, gamm, la, lo, x, y, r, s, prof, h, fv, rmax
    CALL le_config()
    IF ( .not. ativo .or. ivortex /= 1 ) RETURN
    IF ( id < 1 .or. id > 3 ) RETURN
    IF ( dominios_v(id) /= 1 ) RETURN
    th = gmt + xtime/60.0
    IF ( th < t_v_ini .or. th >= t_v_fim ) RETURN
    gamm = min( 1.0, (th - t_v_ini)/max(tr_v, 1.0e-3) )
    rmax = rmax_v_km*1000.0
    DO j = jts, jte
      DO i = its, ite
        la = 0.5*( xlat_u(i,j) + xlat_u(i+1,j) )
        lo = 0.5*( xlong_u(i,j) + xlong_u(i+1,j) )
        x = (lo - lon_v)*111320.0*cos(la*0.0174533)
        y = (la - lat_v)*111320.0
        r = sqrt( x*x + y*y )
        IF ( r < 1.0 .or. r > 10.0*rmax ) CYCLE
        s = r/rmax
        prof = gamm*alpha_v*s*exp(1.0 - s)
        ! dois lacos separados: com o IF dentro do laco o gfortran deixa de vetorizar o cosh (libmvec) e o
        ! perfil sech^2 muda no ultimo bit; assim o caminho padrao e o mesmo codigo de A-D (v4.1)
        IF ( perfil_v == 1 ) THEN
          DO k = kts, kte-1
            fv = prof*exp( -( (z(i,k,j) - zc_v_m)/zw_v_m )**2 )
            rublten(i,k,j) = rublten(i,k,j) - fv*y/r
            rvblten(i,k,j) = rvblten(i,k,j) + fv*x/r
          ENDDO
        ELSE
          DO k = kts, kte-1
            h = z(i,k,j) - ht(i,j)
            fv = prof/cosh( min(h/zr_v_m, 20.0) )**2
            rublten(i,k,j) = rublten(i,k,j) - fv*y/r
            rvblten(i,k,j) = rvblten(i,k,j) + fv*x/r
          ENDDO
        ENDIF
      ENDDO
    ENDDO
  END SUBROUTINE toro_vortice

  ! disparo no nucleo do vortice: a ascendente chegou e ha agua liquida super-resfriada no ponto
  LOGICAL FUNCTION disparo(i, j, wl, ql, tk)
    INTEGER, INTENT(IN) :: i, j
    REAL,    INTENT(IN) :: wl, ql, tk
    disparo = .false.
    IF ( .not. mvn(i,j) ) RETURN
    IF ( .not. disparo_w ) THEN                  ! experimento C: o nucleo inteiro, sem condicao de ascendente
      disparo = .true.
      RETURN
    ENDIF
    disparo = ( wl > w_crit .and. ql > q_crit .and. tk < 273.15 + t_nuc_max_c .and. tk > 273.15 + t_nuc_min_c )
    IF ( disparo .and. .not. avisou_disparo ) THEN
      avisou_disparo = .true.
      WRITE(0,'(a,f6.2,a,es9.2,a,f7.2)') 'toro_wrf: nucleacao no nucleo disparada (w = ', wl, ' m/s, ql = ', ql, ' kg/kg, T = ', tk
    ENDIF
  END FUNCTION disparo

  ! fator do processo k no ponto (i,j): disparo no nucleo > Estado A > 1
  REAL FUNCTION toro_f(k, i, j, wl, ql, tk)
    INTEGER, INTENT(IN) :: k, i, j
    REAL,    INTENT(IN) :: wl, ql, tk
    toro_f = 1.0
    IF ( .not. toro_call ) RETURN
    IF ( disparo(i, j, wl, ql, tk) ) THEN
      IF ( k == 5 ) toro_f = fhm_v
      RETURN
    ENDIF
    IF ( .not. msup(i,j) ) RETURN
    SELECT CASE (k)
      CASE (1) ; toro_f = fcoal
      CASE (2) ; toro_f = faccr
      CASE (3) ; toro_f = fctfz
      CASE (5) ; toro_f = fhm
      CASE (6) ; toro_f = frfrz
    END SELECT
  END FUNCTION toro_f

  ! nucleacao primaria: fnuc_v no disparo; fnuc no Estado A; fnuc_rel na coluna da liberacao por tempo
  REAL FUNCTION toro_fnuc(i, j, wl, ql, tk)
    INTEGER, INTENT(IN) :: i, j
    REAL,    INTENT(IN) :: wl, ql, tk
    toro_fnuc = 1.0
    IF ( .not. toro_call ) RETURN
    IF ( disparo(i, j, wl, ql, tk) ) THEN
      toro_fnuc = fnuc_v
    ELSEIF ( msup(i,j) ) THEN
      toro_fnuc = fnuc
    ELSEIF ( maer(i,j) ) THEN
      toro_fnuc = fnuc_rel
    ENDIF
  END FUNCTION toro_fnuc

  ! congelamento de goticulas (Bigg): suprimido no Estado A so acima de t_hom_c; livre no disparo
  REAL FUNCTION toro_fwfrz(i, j, wl, ql, tk)
    INTEGER, INTENT(IN) :: i, j
    REAL,    INTENT(IN) :: wl, ql, tk
    toro_fwfrz = 1.0
    IF ( .not. toro_call ) RETURN
    IF ( disparo(i, j, wl, ql, tk) ) RETURN
    IF ( msup(i,j) .and. tk > 273.15 + t_hom_c ) toro_fwfrz = fwfrz
  END FUNCTION toro_fwfrz

END MODULE module_toro_wrf
