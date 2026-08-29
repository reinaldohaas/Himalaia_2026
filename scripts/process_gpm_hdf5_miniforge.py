import h5py
import numpy as np
import pandas as pd
import os
import glob

def process_gpm_hdf5():
    repo_dir = "C:/Users/haas/github/Himalaia_2026"
    meteo_dir = os.path.join(repo_dir, "data/raw/meteorology")
    
    # Encontrar arquivos HDF5
    hdf5_files = glob.glob(os.path.join(meteo_dir, "*HDF5*")) + glob.glob(os.path.join(meteo_dir, "*3IMERG*"))
    print(f"=== PROCESSAMENTO CIENTÍFICO COM MINIFORGE / H5PY ===")
    print(f"Arquivos HDF5 do GPM encontrados: {len(hdf5_files)}")
    
    for h5_path in hdf5_files:
        if os.path.isfile(h5_path):
            size_mb = os.path.getsize(h5_path) / (1024 * 1024)
            print(f"\nLendo arquivo GPM: {os.path.basename(h5_path)} ({size_mb:.2f} MB)")
            try:
                with h5py.File(h5_path, 'r') as f:
                    print("Grupos HDF5 disponíveis:", list(f.keys()))
                    if 'Grid' in f:
                        grid = f['Grid']
                        print("Variáveis na Grid:", list(grid.keys()))
                        
                        # Extrair precipitação (Grid/precipitationCal)
                        if 'precipitationCal' in grid:
                            precip = grid['precipitationCal'][:]
                            lon = grid['lon'][:]
                            lat = grid['lat'][:]
                            
                            print(f"Dimensões do grid: Lat={lat.shape}, Lon={lon.shape}, Precip={precip.shape}")
                            
                            # Recorte espacial na bacia do Himalaia / Langtang (Lat: 28.1 a 28.4 N, Lon: 85.2 a 85.6 E)
                            lat_idx = np.where((lat >= 27.5) & (lat <= 29.0))[0]
                            lon_idx = np.where((lon >= 84.5) & (lon <= 86.5))[0]
                            
                            if len(lat_idx) > 0 and len(lon_idx) > 0:
                                sub_precip = precip[0, lon_idx[0]:lon_idx[-1]+1, lat_idx[0]:lat_idx[-1]+1]
                                max_p = np.nanmax(sub_precip)
                                mean_p = np.nanmean(sub_precip[sub_precip >= 0])
                                print(f"-> Região do Himalaia/Langtang: Precipitação Média = {mean_p:.2f} mm/h, Máxima = {max_p:.2f} mm/h")
            except Exception as e:
                print(f"Erro ao ler HDF5 com h5py: {e}")

if __name__ == "__main__":
    process_gpm_hdf5()
