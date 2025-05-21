import gdown
import zipfile
import os

# === 1. Coloca aquí el ID del archivo compartido desde Drive (de tu ZIP)
# Copia solo el ID desde tu link de Drive:
# Ejemplo: https://drive.google.com/file/d/1AbCdEfGhIjKlmNOPqrS/view?usp=sharing
# El ID es lo que va entre `/d/` y `/view`
FILE_ID = "12T65_cFrwrP8AIvCcbAxswbAublY-lmq"

# === 2. Nombres de los archivos
ZIP_PATH = "daten_json.zip"
EXTRACT_PATH = "data/daten_json"

# === 3. Descargar desde Drive
url = f"https://drive.google.com/uc?id={FILE_ID}"
print("⬇️ Descargando ZIP desde Google Drive...")
gdown.download(url, ZIP_PATH, quiet=False)

# === 4. Descomprimir
print("📦 Extrayendo archivos...")
with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
    zip_ref.extractall(EXTRACT_PATH)

print(f"✅ Datos listos en: {EXTRACT_PATH}")
