# agents/analysis_agent/explainer.py

import pandas as pd
import matplotlib.pyplot as plt

def generate_summary(df: pd.DataFrame, company: str) -> str:
    # Normalizar nombres de columnas
    df.columns = [col.lower() for col in df.columns]

    # Verificar columnas requeridas
    if "company" not in df.columns or "year" not in df.columns:
        return f"Erforderliche Spalten sind in DataFrame nicht vorhanden."

    df_company = df[(df["company"] == company) & (df["year"].between(2019, 2024))]

    if df_company.empty:
        return f" Keine Daten für das Unternehmen '{company}' zwischen 2019 und 2024 gefunden."

    # Contar por año
    counts_by_year = df_company.groupby("year").size().sort_index()
    tendenz = " steigend" if counts_by_year.iloc[-1] > counts_by_year.iloc[0] else " rückläufig"
    durchschnitt = counts_by_year.mean()

    return f"{company}: Tendenz {tendenz}. Durchschnittliche Anzahl an Dokumenten pro Jahr: {durchschnitt:.1f}."

def generate_summary_table(df: pd.DataFrame, show_plot=False):
    df.columns = [col.lower() for col in df.columns]

    if "company" not in df.columns or "year" not in df.columns:
        print("Unvollständige Daten zur Erstellung der Tabelle.")
        return

    # Contar documentos por empresa y año
    grouped = df.groupby(["company", "year"]).size().reset_index(name="document_count")

    resumen = grouped.groupby("company")["document_count"].agg(
        Gesamt="sum",
        Durchschnitt_Jahr=lambda x: round(x.sum() / df["year"].nunique(), 2)
    ).reset_index()

    print("\n Übersichtstabelle nach Unternehmen (2019–2024):")
    print(resumen.to_string(index=False))

    # Tabla visual
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.axis("off")
    table = ax.table(
        cellText=resumen.values,
        colLabels=resumen.columns,
        loc="center",
        cellLoc="center"
    )
    table.scale(1.2, 1.2)
    plt.title(" Zusammenfassung nach Unternehmen (2019–2024)", pad=20)
    plt.tight_layout()
    plt.savefig("summary_table.png", dpi=300)

    if show_plot:
        plt.show()

def export_summaries_to_txt(df: pd.DataFrame, companies: list, filename="Zusammenfassung_Unternehmen.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(" Trendübersicht nach Unternehmen (2019–2024)\n\n")
        for company in companies:
            zusammenfassung = generate_summary(df, company)
            f.write(f"{zusammenfassung}\n")
        f.write("\nAutomatisch generiert vom Analyst-AI-System.\n")

    print(f"Datei '{filename}' wurde erfolgreich erstellt.")
