# agents/analysis_agent/explainer.py

def generate_explanation(df, company, metric):
    df = df[df["Company"] == company].sort_values(by=["Year", "Quarter"])
    latest = df.iloc[-1][metric]
    avg = df[metric].mean()
    diff = latest - avg
    direction = "aumentó" if diff > 0 else "disminuyó"

    return (
        f"El último valor de {metric} reportado por {company} fue {latest:.2f}, "
        f"lo que representa una {direction} de {abs(diff):.2f} en comparación con el promedio."
    )