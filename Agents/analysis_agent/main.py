# main.py

import os
from agents.analysis_agent.trends import load_json_data, preprocess
from agents.analysis_agent.visualizations import plot_trend_by_company, plot_quarterly_trend
from agents.analysis_agent.explainer import (
    generate_summary,
    generate_summary_table,
    export_summaries_to_txt
)
from agents.analysis_agent.forecast import predict_by_company

# 1. Definir ruta a los datos JSON
folder = os.path.join(os.path.dirname(__file__), "../../data/daten_json")

# 2. Cargar los datos originales desde los archivos JSON
df = load_json_data(folder)
print("Spalten des ursprünglichen DataFrame:", df.columns)
print(df.head(2))

# 3. Preprocesar los datos para visualizaciones
df_clean = preprocess(df)

# 4. Validación
if df_clean.empty:
    print(" Der saubere DataFrame ist leer. Überprüfen Sie die Daten.")
else:
    # 5. Visualización anual y trimestral
    plot_trend_by_company(df_clean)
    plot_quarterly_trend(df_clean)

    # 6. Generar resúmenes por empresa
    companies = ["Apple", "Microsoft", "Google", "NVIDIA", "Meta"]
    print("\n Zusammenfassung nach Unternehmen:")
    for company in companies:
        print(generate_summary(df, company))

    # 7. Generar tabla
    generate_summary_table(df_clean)

    # 8. Predicciones
    for company in companies:
        print(f"\n Vorhersage generieren für {company}...")
        predict_by_company(df_clean, company)

    # 9. Exportar resúmenes
    export_summaries_to_txt(df, companies)