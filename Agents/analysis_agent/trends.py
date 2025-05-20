# trends.py

import os
import sys
import json
import pandas as pd

# Agrega la raíz del proyecto al path — versión robusta y segura
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Ahora sí, importa config
from utils.config import JSON_DATA_DIR

def load_financial_data(data_dir: str = JSON_DATA_DIR) -> pd.DataFrame:
    """
    Carga y unifica los archivos JSON en un solo DataFrame.
    Realiza limpieza básica de tipos de datos.
    """
    data = []

    # 📁 Recorrer todos los archivos .json en la carpeta
    for file in os.listdir(data_dir):
        if file.endswith(".json"):
            file_path = os.path.join(data_dir, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = json.load(f)
                    data.append(content)
            except json.JSONDecodeError as e:
                print(f"❌ Error al leer {file}: {e}")

    # 📊 Convertir lista de dicts en DataFrame
    df = pd.DataFrame(data)

    # 🧹 Conversión y limpieza de columnas
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    if 'revenue' in df.columns:
        df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce')
    if 'net_income' in df.columns:
        df['net_income'] = pd.to_numeric(df['net_income'], errors='coerce')
    if 'stock_price' in df.columns:
        df['stock_price'] = pd.to_numeric(df['stock_price'], errors='coerce')

    return df

# 🧪 Modo de prueba directa: ejecutar este archivo solo
if __name__ == "__main__":
    df = load_financial_data()
    
    print("\n📄 Primeras filas del DataFrame:")
    print(df.head())

    print("\n🏢 Empresas encontradas:")
    print(df['company'].value_counts())

    print("\n📆 Rango de fechas:")
    print(df['date'].min(), "→", df['date'].max())

    print("🧭 sys.path contiene:\n", "\n".join(sys.path))
