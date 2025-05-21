from prophet import Prophet
import pandas as pd
import matplotlib.pyplot as plt

def predict_by_company(df, company, column="document_count"):
    # Filtrar por empresa
    df_company = df[df["company"] == company].copy()

    # Asegurar que la columna 'date' exista
    if "date" not in df_company.columns:
        df_company["date"] = pd.to_datetime(df_company["year"].astype(str) + "-01-01")

    # Agrupar por fecha
    df_grouped = df_company.groupby("date")[column].sum().reset_index()
    df_grouped = df_grouped.rename(columns={"date": "ds", column: "y"})

    if df_grouped.shape[0] < 2:
        print(f"⚠️ Nicht genügend Daten für {company}, um eine Prognose durchzuführen.")
        return None, None

    # Entrenar modelo Prophet
    model = Prophet()
    model.fit(df_grouped)

    # Predecir 6 meses en el futuro
    future = model.make_future_dataframe(periods=6, freq="M")
    forecast = model.predict(future)

    # Graficar
    fig = model.plot(forecast)
    plt.title(f"Prognose des Investor Relations für {company}")
    plt.xlabel("Datum")
    plt.ylabel("Anzahl der Dokumente")
    plt.tight_layout()
    plt.savefig(f"forecast_{company.lower()}.png", dpi=300)
    plt.show()

    return forecast, model
