# agents/analysis_agent/visualizations.py

import pandas as pd
import matplotlib.pyplot as plt

def plot_trend(df, column="document_count"):
    plt.figure(figsize=(10, 5))
    plt.plot(df["date"], df[column], marker="o", linestyle="-", color="blue")
    plt.title("Volumen der Finanzberichte pro Jahr (2019–2024)")
    plt.xlabel("Datum")
    plt.ylabel("Anzahl der Dokumente")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_trend_by_company(df, company_names=None):
    if company_names is None:
        company_names = ["Apple", "Microsoft", "Google", "NVIDIA", "Meta"]

    # Asegúrate de tener 'year' y 'company' en tu DataFrame
    plt.figure(figsize=(10, 6))
    for company in company_names:
        filtered = df[df["company"] == company]
        grouped = filtered.groupby("year")["document_count"].sum().reset_index()
        plt.plot(grouped["year"], grouped["document_count"], marker='o', label=company)

    plt.title("Investor Relations nach Unternehmen und Jahr (2019–2024)")
    plt.xlabel("Jahr")
    plt.ylabel("Anzahl der Dokumente")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_quarterly_trend(df):
    """
    Genera una gráfica por empresa agrupada por año y trimestre (Q1–Q4).
    """
    plt.figure(figsize=(12, 6))
    for company in df["company"].unique():
        subset = df[df["company"] == company].copy()
        subset = subset.sort_values(by=["year", "quarter"])

        # Crear etiquetas como '2020-Q1', '2020-Q2', etc.
        labels = subset["year"].astype(str) + "-" + subset["quarter"]
        plt.plot(labels, subset["document_count"], marker="o", label=company)

    plt.title("Investor Relations nach Unternehmen und Quartal (2019–2024)")
    plt.xlabel("Quartal")
    plt.ylabel("Anzahl der Dokumente")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()