import pandas as pd

def load_financial_data(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    return df

def summarize_trends(df: pd.DataFrame) -> dict:
    latest = df.iloc[-1]
    prev = df.iloc[-5]

    growth = (latest['revenue'] - prev['revenue']) / prev['revenue'] * 100
    margin_trend = df['operating_margin'].rolling(4).mean().iloc[-1]

    return {
        "revenue_growth": round(growth, 2),
        "latest_eps": latest['eps'],
        "avg_margin": round(margin_trend, 2)
    }

# 👇 Código de prueba para que se ejecute al correr python trends.py
if __name__ == "__main__":
    # 1. Asegúrate de tener este archivo CSV
    filepath = "../../../data/processed/microsoft_q_data.csv"  # Ajusta si es necesario
    df = load_financial_data(filepath)
    trends = summarize_trends(df)
    print("Análisis de tendencias:")
    print(trends)
