<#
.SYNOPSIS
    Download Automatizado dos Grânulos GPM IMERG V07 (Late Run) de Agosto/2026 via PowerShell.
.DESCRIPTION
    Consulta o NASA CMR para catalogar todos os 96 grânulos de 25-26/08/2026 e realiza o download.
.EXAMPLE
    .\scripts\download_gpm_imerg_2026.ps1 -Token "seu_token_aqui"
#>

param(
    [Parameter(Mandatory=$false)]
    [string]$Token = $env:EARTHDATA_TOKEN
)

if (-not $Token) {
    Write-Error "Token Earthdata não fornecido. Passe -Token '<seu_token>' ou defina `$env:EARTHDATA_TOKEN."
    exit 1
}

$repoDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$targetDir = Join-Path $repoDir "data\raw\meteorology"
if (-not (Test-Path $targetDir)) {
    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
}

$cmrUrl = "https://cmr.earthdata.nasa.gov/search/granules.json?short_name=GPM_3IMERGHHL&version=07&temporal=2026-08-25T00:00:00Z,2026-08-26T23:59:59Z&page_size=100"

Write-Host ">> [1/3] Consultando NASA CMR para catalogação de grânulos de 25-26/08/2026..." -ForegroundColor Cyan
$cmrData = Invoke-RestMethod -Uri $cmrUrl -Method Get
$entries = $cmrData.feed.entry
Write-Host "   Total de grânulos encontrados: $($entries.Count)" -ForegroundColor Green

$catalog = @()
foreach ($entry in $entries) {
    $dataLink = $entry.links | Where-Object { $_.rel -like "*data#" -and $_.href -like "*.HDF5" } | Select-Object -First 1
    if ($dataLink) {
        $catalog += [PSCustomObject]@{
            Title = $entry.title
            Url = $dataLink.href
            Start = $entry.time_start
            End = $entry.time_end
        }
    }
}

$catalogFile = Join-Path $targetDir "gpm_imerg_granules_catalog_2026_official.json"
$catalog | ConvertTo-Json -Depth 3 | Set-Content -Path $catalogFile -Encoding UTF8
Write-Host ">> [2/3] Catálogo oficial de 2026 gravado em: $catalogFile" -ForegroundColor Green

Write-Host ">> [3/3] Iniciando download com autenticação Bearer..." -ForegroundColor Cyan
$success = 0
$failed = 0

for ($i = 0; $i -lt $catalog.Count; $i++) {
    $item = $catalog[$i]
    $fileName = Split-Path -Leaf $item.Url
    $destFile = Join-Path $targetDir $fileName
    
    if ((Test-Path $destFile) -and ((Get-Item $destFile).Length -gt 1000000)) {
        Write-Host "   [$($i+1)/$($catalog.Count)] Já existe: $fileName ($([math]::Round((Get-Item $destFile).Length/1MB, 2)) MB)" -ForegroundColor Gray
        $success++
        continue
    }

    Write-Host "   [$($i+1)/$($catalog.Count)] Baixando: $fileName ..." -NoNewline
    try {
        # Usa curl.exe com cabeçalho de autenticação e suporte a redirecionamento
        curl.exe -k -s -L --location-trusted -H "Authorization: Bearer $Token" $item.Url -o $destFile
        
        if ((Test-Path $destFile) -and ((Get-Item $destFile).Length -gt 1000000)) {
            Write-Host " OK ($([math]::Round((Get-Item $destFile).Length/1MB, 2)) MB)" -ForegroundColor Green
            $success++
        } else {
            Write-Host " FALHA (Resposta inválida ou app não autorizado no Earthdata)" -ForegroundColor Red
            if (Test-Path $destFile) { Remove-Item $destFile -Force }
            $failed++
        }
    } catch {
        Write-Host " ERRO: $_" -ForegroundColor Red
        $failed++
    }
}

Write-Host "`n=== Concluído: $success sucessos, $failed falhas ===" -ForegroundColor Yellow
