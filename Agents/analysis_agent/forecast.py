# agents/analysis_agent/forecast.py

from prophet import Prophet
import pandas as pd
from Agents.analysis_agent.trends import analyze_trend

def forecast_metric(df, company, metric):
    trend = analyze_trend(df, company, metric).rename(columns={
        "Quarter_Index": "ds",
        metric: "y"
    })

    # Convertir "2023-Q1" a fecha real
    trend["ds"] = pd.to_datetime(trend["ds"].str.replace(
        "Q1", "-02-01"
    ).str.replace("Q2", "-05-01").str.replace("Q3", "-08-01").str.replace("Q4", "-11-01"))

    model = Prophet()
    model.fit(trend)

    future = model.make_future_dataframe(periods=1, freq="Q")
    forecast = model.predict(future)

    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]