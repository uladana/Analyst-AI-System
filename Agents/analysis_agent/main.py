from trends import load_financial_data, preprocess_data
from visualizations import plot_revenue, plot_profit_margin
from forecast import forecast_revenue
from explainer import generate_summary

# Cargar y procesar los datos
df = load_financial_data("../../data/processed")  # Ajusta si tu path es distinto
df = preprocess_data(df)

company = "NVIDIA"

# Mostrar gráficos
revenue_fig = plot_revenue(df, company)
margin_fig = plot_profit_margin(df, company)

# Mostrar predicción
forecast_df, forecast_fig = forecast_revenue(df, company)

# Mostrar resumen
summary = generate_summary(df, company)

revenue_fig.show()
margin_fig.show()
forecast_fig.show()
print(summary)