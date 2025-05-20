# agents/analysis_agent/visualizations.py

import plotly.graph_objects as go
from Agents.analysis_agent.trends import analyze_trend

def plot_metric(df, company, metric):
    trend = analyze_trend(df, company, metric)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=trend["Quarter_Index"],
        y=trend[metric],
        mode='lines+markers',
        name=metric
    ))

    fig.update_layout(
        title=f"{metric} de {company} por trimestre",
        xaxis_title="Trimestre",
        yaxis_title=metric,
        template="plotly_white"
    )

    return fig