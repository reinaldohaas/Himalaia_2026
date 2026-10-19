!
! module_toro_wrf -- "modo super-resfriado" (Estado A da anti-varredura de Tinsley) para a microfisica NSSL
! de 2 momentos do WRF, e a liberacao por aerossol trazido por um vortice.
!
! Fica INERTE se nao existir o arquivo toro_wrf.txt no diretorio da rodada: nenhum fator e aplicado e o
! WRF reproduz bit a bit a rodada original (os trechos inseridos no NSSL so executam com toro_call = .true.).
!
! Estado A (t_ini <= t < t_rel, dentro de raio_km do centro (lat0,lon0), nos dominios marcados em dominios):
!   fcoal  autoconversao e autocoleta de goticulas (qrcnw, crcnw, cautn)          -> chuva quente
!   faccr  acrecao de goticulas pela chuva (qracw, cracw)                            -> chuva quente
!   fctfz  congelamento por contato (cwctfz, qwctfz)
!   fnuc   nucleacao primaria de gelo (ciint, qiint)
!   fhm    multiplicacao de gelo por Hallett-Mossop (csplinter, qsplinter)
!   frfrz  congelamento de gotas de chuva (qrfrz, crfrz) e por colisao com gelo (qiacrf, ciacrf)
!   fwfrz  congelamento de goticulas (Bigg) acima de t_hom_c; abaixo de t_hom_c (padrao -38 C) fica intacto
! Liberacao (t_rel <= t < t_rel + t_dur): fisica normal em todo lugar e, numa coluna de raio_aer_km em torno de
! (lat_aer,lon_aer) -- o vortice que traz o aerossol --, a nucleacao primaria multiplicada por fnuc_rel.
! Tempo t em horas desde 25/08/2026 00 UTC: t = gmt + xtime/60 (todos os dominios comecam em 25/08).
!
MODULE module_toro_wrf
  IMPLICIT NONE
  PRIVATE
  PUBLIC :: toro_wrf_prepara, toro_call, toro_f, toro_fnuc, toro_fwfrz

  LOGICAL, SAVE :: lido = .false., ativo = .false.
  LOGICAL, SAVE :: toro_call = .false.
  REAL,    SAVE :: t_ini = 17.0, t_rel = 26.25, t_dur = 0.5
  REAL,    SAVE :: lat0 = 28.271, lon0 = 85.515, raio_km = 150.0
  REAL,    SAVE :: fcoal = 0.0, faccr = 0.0, fctfz = 0.0, fnuc = 0.0, fhm = 0.0, frfrz = 0.0, fwfrz = 0.0
  REAL,    SAVE :: t_hom_c = -38.0
  REAL,    SAVE :: lat_aer = 28.271, lon_aer = 85.515, raio_aer_km = 5.0, fnuc_rel = 100.0
  INTEGER, SAVE :: dominios(3) = (/ 0, 1, 1 /)
  LOGICAL, ALLOCATABLE, SAVE :: msup(:,:), maer(:,:)

  NAMELIST /toro_wrf/ t_ini, t_rel, t_dur, lat0, lon0, raio_km, fcoal, faccr, fctfz, fnuc, fhm, frfrz, fwfrz, &
                      t_hom_c, lat_aer, lon_aer, raio_aer_km, fnuc_rel, dominios

CONTAINS

  SUBROUTINE toro_wrf_prepara(id, xtime, gmt, xlat, xlong, ims, ime, jms, jme, its, ite, jts, jte)
    INTEGER, INTENT(IN) :: id, ims, ime, jms, jme, its, ite, jts, jte
    REAL,    INTENT(IN) :: xtime, gmt
    REAL,    INTENT(IN) :: xlat(ims:ime, jms:jme), xlong(ims:ime, jms:jme)
    INTEGER :: i, j, iu, ios
    REAL :: th, d, da, cl
    LOGICAL :: existe
    IF ( .not. lido ) THEN
      lido = .true.
      INQUIRE( FILE='toro_wrf.txt', EXIST=existe )
      IF ( existe ) THEN
        iu = 77
        OPEN( iu, FILE='toro_wrf.txt', STATUS='old', ACTION='read', IOSTAT=ios )
        IF ( ios == 0 ) READ( iu, NML=toro_wrf, IOSTAT=ios )
        CLOSE( iu )
        ativo = ( ios == 0 )
        IF ( ativo ) WRITE(0,'(a)') 'toro_wrf: modo super-resfriado ATIVO (toro_wrf.txt lido)'
        IF ( .not. ativo ) WRITE(0,'(a)') 'toro_wrf: ERRO lendo toro_wrf.txt -- modulo INATIVO'
      ENDIF
    ENDIF
    toro_call = .false.
    IF ( .not. ativo ) RETURN
    IF ( id < 1 .or. id > 3 ) RETURN
    IF ( dominios(id) /= 1 ) RETURN
    th = gmt + xtime/60.0
    IF ( th < t_ini .or. th >= t_rel + t_dur ) RETURN
    IF ( allocated(msup) ) THEN
      IF ( lbound(msup,1) /= ims .or. ubound(msup,1) /= ime .or. lbound(msup,2) /= jms .or. ubound(msup,2) /= jme ) THEN
        DEALLOCATE( msup, maer )
      ENDIF
    ENDIF
    IF ( .not. allocated(msup) ) ALLOCATE( msup(ims:ime, jms:jme), maer(ims:ime, jms:jme) )
    msup = .false. ; maer = .false.
    DO j = jts, jte
      DO i = its, ite
        cl = cos( xlat(i,j)*0.0174533 )
        d  = 111.32*sqrt( (xlat(i,j)-lat0)**2 + ((xlong(i,j)-lon0)*cl)**2 )
        da = 111.32*sqrt( (xlat(i,j)-lat_aer)**2 + ((xlong(i,j)-lon_aer)*cl)**2 )
        IF ( th < t_rel ) THEN
          msup(i,j) = ( d <= raio_km )
        ELSE
          maer(i,j) = ( da <= raio_aer_km )
        ENDIF
      ENDDO
    ENDDO
    toro_call = any(msup) .or. any(maer)
  END SUBROUTINE toro_wrf_prepara

  ! fator do processo k no ponto (i,j): o fator do Estado A dentro da regiao; 1 fora dela ou fora da janela
  REAL FUNCTION toro_f(k, i, j)
    INTEGER, INTENT(IN) :: k, i, j
    toro_f = 1.0
    IF ( .not. toro_call ) RETURN
    IF ( .not. msup(i,j) ) RETURN
    SELECT CASE (k)
      CASE (1) ; toro_f = fcoal
      CASE (2) ; toro_f = faccr
      CASE (3) ; toro_f = fctfz
      CASE (5) ; toro_f = fhm
      CASE (6) ; toro_f = frfrz
    END SELECT
  END FUNCTION toro_f

  ! nucleacao primaria: fnuc no Estado A; fnuc_rel na coluna do aerossol durante a liberacao
  REAL FUNCTION toro_fnuc(i, j)
    INTEGER, INTENT(IN) :: i, j
    toro_fnuc = 1.0
    IF ( .not. toro_call ) RETURN
    IF ( msup(i,j) ) toro_fnuc = fnuc
    IF ( maer(i,j) ) toro_fnuc = fnuc_rel
  END FUNCTION toro_fnuc

  ! congelamento de goticulas (Bigg): suprimido no Estado A so acima de t_hom_c (congelamento homogeneo intacto)
  REAL FUNCTION toro_fwfrz(i, j, temk)
    INTEGER, INTENT(IN) :: i, j
    REAL,    INTENT(IN) :: temk
    toro_fwfrz = 1.0
    IF ( .not. toro_call ) RETURN
    IF ( msup(i,j) .and. temk > 273.15 + t_hom_c ) toro_fwfrz = fwfrz
  END FUNCTION toro_fwfrz

END MODULE module_toro_wrf
