"""
Script de Download Automatizado dos Grânulos GPM IMERG V07 (Late Run) para Agosto de 2026.
Utiliza a API aberta do NASA CMR para catalogação e download autenticado via NASA Earthdata.

Uso:
  $env:EARTHDATA_TOKEN = "seu_token_aqui"
  python scripts/download_gpm_imerg_2026.py

Requisito Prévio na Conta Earthdata:
  O usuário deve aprovar o aplicativo "NASA GESDISC DATA ARCHIVE" em:
  https://urs.earthdata.nasa.gov/profile -> Applications -> Authorized Apps -> Approve More Applications
"""

import os
import sys
import json
import urllib.request
import urllib.error
import ssl

HDF5_MAGIC = b'\x89HDF\r\n\x1a\n'

def get_cmr_granules(temporal=("2026-08-25T00:00:00Z", "2026-08-26T23:59:59Z")):
    """Busca a lista oficial de grânulos GPM IMERG Late Run no NASA CMR."""
    cmr_url = (
        f"https://cmr.earthdata.nasa.gov/search/granules.json?"
        f"short_name=GPM_3IMERGHHL&version=07&"
        f"temporal={temporal[0]},{temporal[1]}&page_size=100"
    )
    print(f">> Consultando NASA CMR: {cmr_url}")
    ctx = ssl.create_default_context()
    req = urllib.request.Request(cmr_url, headers={"User-Agent": "Himalaya2026-Audit/1.0"})
    
    with urllib.request.urlopen(req, context=ctx) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        
    entries = data.get("feed", {}).get("entry", [])
    granules = []
    for entry in entries:
        title = entry.get("title", "")
        # Encontrar link direto de download de dados
        download_url = None
        for link in entry.get("links", []):
            if link.get("rel", "").endswith("/data#") and link.get("href", "").endswith(".HDF5"):
                download_url = link.get("href")
                break
        if download_url:
            granules.append({
                "title": title,
                "url": download_url,
                "start": entry.get("time_start"),
                "end": entry.get("time_end")
            })
    return granules

def download_granule(url, output_path, token):
    """Baixa um grânulo individual preservando o cabeçalho de autenticação."""
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "Himalaya2026-Audit/1.0"
    }
    
    # Criar handler customizado para manter Authorization em redirecionamentos HTTPS
    class AuthRedirectHandler(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            new_req = super().redirect_request(req, fp, code, msg, headers, newurl)
            if new_req:
                new_req.add_header("Authorization", f"Bearer {token}")
            return new_req

    ctx = ssl.create_default_context()
    opener = urllib.request.build_opener(AuthRedirectHandler())
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with opener.open(req, context=ctx, timeout=60) as resp:
            content = resp.read()
            
            # Verificação de integridade: checar magic bytes HDF5
            if not content.startswith(HDF5_MAGIC):
                # Provavelmente página de login HTML ou erro
                if b"html" in content[:200].lower() or b"access denied" in content[:200].lower():
                    raise ValueError(
                        "O servidor retornou HTML em vez de HDF5. "
                        "Certifique-se de que o app 'NASA GESDISC DATA ARCHIVE' está autorizado em sua conta Earthdata."
                    )
            
            with open(output_path, "wb") as f:
                f.write(content)
            return True, len(content)
    except Exception as e:
        return False, str(e)

def main():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_dir = os.path.join(repo_dir, "data", "raw", "meteorology")
    os.makedirs(target_dir, exist_ok=True)
    
    token = os.environ.get("EARTHDATA_TOKEN")
    if not token:
        print("[ERRO] Variável de ambiente EARTHDATA_TOKEN não configurada.")
        print("Defina a variável no terminal antes de executar:")
        print("  Windows PowerShell: $env:EARTHDATA_TOKEN = '<seu_token>'")
        sys.exit(1)
        
    print(f"=== DOWNLOAD AUTOMATIZADO GPM IMERG V07 — AGOSTO/2026 ===")
    granules = get_cmr_granules()
    print(f"Total de grânulos localizados no NASA CMR: {len(granules)}")
    
    # Salvar catálogo oficial atualizado de 2026
    catalog_path = os.path.join(target_dir, "gpm_imerg_granules_catalog_2026_official.json")
    with open(catalog_path, "w", encoding="utf-8") as f:
        json.dump(granules, f, indent=2)
    print(f"Catálogo salvo em: {catalog_path}")
    
    success_count = 0
    fail_count = 0
    for idx, g in enumerate(granules, 1):
        filename = g["url"].split("/")[-1]
        out_file = os.path.join(target_dir, filename)
        
        if os.path.exists(out_file) and os.path.getsize(out_file) > 1000000:
            # Já baixado e válido
            print(f"[{idx}/{len(granules)}] Já existe: {filename} ({os.path.getsize(out_file)/1024/1024:.2f} MB)")
            success_count += 1
            continue
            
        print(f"[{idx}/{len(granules)}] Baixando: {filename} ...", end=" ", flush=True)
        ok, res = download_granule(g["url"], out_file, token)
        if ok:
            print(f"OK ({res / (1024*1024):.2f} MB)")
            success_count += 1
        else:
            print(f"FALHA: {res}")
            fail_count += 1
            # Limpar arquivo com erro se existir
            if os.path.exists(out_file):
                os.remove(out_file)
                
    print(f"\nResumo: {success_count} sucessos, {fail_count} falhas.")

if __name__ == "__main__":
    main()
