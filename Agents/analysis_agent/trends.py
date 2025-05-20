# agents/analysis_agent/trends.py

import os
import json
import pandas as pd

def load_financial_data(folder_path="/Users/paulasalda/Downloads/daten_json"):
    """
    Carga todos los JSON del directorio y los convierte en un DataFrame estructurado.
    """
    data = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            full_path = os.path.join(folder_path, filename)
            try:
                with open(full_path, 'r') as f:
                    json_data = json.load(f)

                    entry = {
                        "Company": json_data.get("company", "Unknown"),
                        "Year": json_data.get("year", None),
                        "Quarter": json_data.get("quarter", None),
                        **json_data.get("financials", {})  # Aquí están Revenue, Net Income, EPS, etc.
                    }

                    data.append(entry)
            except Exception as e:
                print(f"⚠️ Error al cargar {filename}: {e}")
    
    return pd.DataFrame(data)

def preprocess_data(df):
    df["date"] = pd.to_datetime(df["date"])
    df.sort_values("date", inplace=True)
    df["revenue_billion"] = df["revenue"] / 1e9
    df["net_income_billion"] = df["net_income"] / 1e9
    return df

def analyze_trend(df, company, metric):
    """
    Devuelve los valores del métrico para la empresa seleccionada ordenados por tiempo.
    """
    df_filtered = df[df["Company"] == company].copy()
    df_filtered["Quarter_Index"] = df_filtered["Year"].astype(str) + "-" + df_filtered["Quarter"]
    df_filtered = df_filtered.sort_values(by=["Year", "Quarter"])
    return df_filtered[["Quarter_Index", metric]]
