from agents.analysis_agent.explainer import generate_summary
from agents.analysis_agent.visualizations import plot_trend_by_company, plot_quarterly_trend
from agents.analysis_agent.forecast import predict_by_company

def create_react_agent(df_raw, df_clean):
    def run(prompt: str):
        if "zusammenfassung" in prompt.lower():
            unternehmen = extract_company_from_prompt(prompt)
            return generate_summary(df_raw, unternehmen)

        elif "grafik" in prompt.lower() and "quartal" in prompt.lower():
            plot_quarterly_trend(df_clean)
            return " Quartalsdiagramm generiert."

        elif "grafik" in prompt.lower():
            plot_trend_by_company(df_clean)
            return "📈 Jahresdiagramm generiert."

        elif "prognose" in prompt.lower():
            unternehmen = extract_company_from_prompt(prompt)
            predict_by_company(df_clean, unternehmen, show_plot=True)
            return f"Prognose für {unternehmen} generiert."

        elif any(stichwort in prompt.lower() for stichwort in ["vergleich", "beste firma", "vergleichung", "beste unternehmen"]):
            return vergleiche_tendenzen(df_clean, prompt)

        else:
            return "Anweisung nicht erkannt. Bitte verwende: zusammenfassung, diagramm, quartal, prognose, vergleich."

    return run

def extract_company_from_prompt(prompt: str) -> str:
    empresas = ["Apple", "Microsoft", "Google", "NVIDIA", "Meta"]
    for empresa in empresas:
        if empresa.lower() in prompt.lower():
            return empresa
    return "Apple"  # por defecto

import matplotlib.pyplot as plt

def vergleiche_tendenzen(df_clean, prompt=None):
    # Detectar empresas mencionadas
    alle_unternehmen = df_clean["company"].unique().tolist()
    if prompt:
        gefilterte = [u for u in alle_unternehmen if u.lower() in prompt.lower()]
    else:
        gefilterte = alle_unternehmen

    if len(gefilterte) < 2:
        return " Bitte gib mindestens zwei Unternehmen für den Vergleich an."

    tendenzen = {}
    for unternehmen in gefilterte:
        df_unternehmen = df_clean[df_clean["company"] == unternehmen]
        df_unternehmen = df_unternehmen.groupby("year")["document_count"].sum().sort_index()

        if len(df_unternehmen) >= 2:
            differenz = df_unternehmen.iloc[-1] - df_unternehmen.iloc[0]
            tendenzen[unternehmen] = differenz

    if not tendenzen:
        return " Nicht genügend Daten für einen Vergleich."

    bestes = max(tendenzen, key=tendenzen.get)
    vergleich_text = ", ".join([f"{k}: {'+' if v >= 0 else ''}{v}" for k, v in tendenzen.items()])
    # Analytische Formulierung im professionellen Stil
    teile = []
    for unternehmen, diff in tendenzen.items():
        t = f"{unternehmen} {'steigerte sich um' if diff >= 0 else 'verzeichnete einen Rückgang von'} {abs(diff)} Dokumenten"
        teile.append(t)

    beschreibung = "; ".join(teile)


    from agents.analysis_agent.explainer import generate_summary
from agents.analysis_agent.visualizations import plot_trend_by_company, plot_quarterly_trend
from agents.analysis_agent.forecast import predict_by_company

def create_react_agent(df_raw, df_clean):
    def run(prompt: str):
        if "zusammenfassung" in prompt.lower():
            unternehmen = extract_company_from_prompt(prompt)
            return generate_summary(df_raw, unternehmen)

        elif "grafik" in prompt.lower() and "quartal" in prompt.lower():
            plot_quarterly_trend(df_clean)
            return " Quartalsdiagramm generiert."

        elif "grafik" in prompt.lower():
            plot_trend_by_company(df_clean)
            return "📈 Jahresdiagramm generiert."

        elif "prognose" in prompt.lower():
            unternehmen = extract_company_from_prompt(prompt)
            predict_by_company(df_clean, unternehmen, show_plot=True)
            return f"Prognose für {unternehmen} generiert."

        elif any(stichwort in prompt.lower() for stichwort in ["vergleich", "beste firma", "vergleichung", "beste unternehmen"]):
            return vergleiche_tendenzen(df_clean, prompt)

        else:
            return "Anweisung nicht erkannt. Bitte verwende: zusammenfassung, diagramm, quartal, prognose, vergleich."

    return run

def extract_company_from_prompt(prompt: str) -> str:
    empresas = ["Apple", "Microsoft", "Google", "NVIDIA", "Meta"]
    for empresa in empresas:
        if empresa.lower() in prompt.lower():
            return empresa
    return "Apple"  # por defecto

import matplotlib.pyplot as plt

def vergleiche_tendenzen(df_clean, prompt=None):
    # Detectar empresas mencionadas
    alle_unternehmen = df_clean["company"].unique().tolist()
    if prompt:
        gefilterte = [u for u in alle_unternehmen if u.lower() in prompt.lower()]
    else:
        gefilterte = alle_unternehmen

    if len(gefilterte) < 2:
        return " Bitte gib mindestens zwei Unternehmen für den Vergleich an."

    tendenzen = {}
    for unternehmen in gefilterte:
        df_unternehmen = df_clean[df_clean["company"] == unternehmen]
        df_unternehmen = df_unternehmen.groupby("year")["document_count"].sum().sort_index()

        if len(df_unternehmen) >= 2:
            differenz = df_unternehmen.iloc[-1] - df_unternehmen.iloc[0]
            tendenzen[unternehmen] = differenz

    if not tendenzen:
        return " Nicht genügend Daten für einen Vergleich."

    bestes = max(tendenzen, key=tendenzen.get)
    vergleich_text = ", ".join([f"{k}: {'+' if v >= 0 else ''}{v}" for k, v in tendenzen.items()])
    # Analytische Formulierung im professionellen Stil
    teile = []
    for unternehmen, diff in tendenzen.items():
        t = f"{unternehmen} {'steigerte sich um' if diff >= 0 else 'verzeichnete einen Rückgang von'} {abs(diff)} Dokumenten"
        teile.append(t)

    beschreibung = "; ".join(teile)

    from agents.analysis_agent.explainer import generate_summary
from agents.analysis_agent.visualizations import plot_trend_by_company, plot_quarterly_trend
from agents.analysis_agent.forecast import predict_by_company

def create_react_agent(df_raw, df_clean):
    def run(prompt: str):
        if "zusammenfassung" in prompt.lower():
            unternehmen = extract_company_from_prompt(prompt)
            return generate_summary(df_raw, unternehmen)

        elif "grafik" in prompt.lower() and "quartal" in prompt.lower():
            plot_quarterly_trend(df_clean)
            return " Quartalsdiagramm generiert."

        elif "grafik" in prompt.lower():
            plot_trend_by_company(df_clean)
            return "📈 Jahresdiagramm generiert."

        elif "prognose" in prompt.lower():
            unternehmen = extract_company_from_prompt(prompt)
            predict_by_company(df_clean, unternehmen, show_plot=True)
            return f"Prognose für {unternehmen} generiert."

        elif any(stichwort in prompt.lower() for stichwort in ["vergleich", "beste firma", "vergleichung", "beste unternehmen"]):
            return vergleiche_tendenzen(df_clean, prompt)

        else:
            return "Anweisung nicht erkannt. Bitte verwende: zusammenfassung, diagramm, quartal, prognose, vergleich."

    return run

def extract_company_from_prompt(prompt: str) -> str:
    empresas = ["Apple", "Microsoft", "Google", "NVIDIA", "Meta"]
    for empresa in empresas:
        if empresa.lower() in prompt.lower():
            return empresa
    return "Apple"  # por defecto

import matplotlib.pyplot as plt

def vergleiche_tendenzen(df_clean, prompt=None):
    # Detectar empresas mencionadas
    alle_unternehmen = df_clean["company"].unique().tolist()
    if prompt:
        gefilterte = [u for u in alle_unternehmen if u.lower() in prompt.lower()]
    else:
        gefilterte = alle_unternehmen

    if len(gefilterte) < 2:
        return " Bitte gib mindestens zwei Unternehmen für den Vergleich an."

    tendenzen = {}
    for unternehmen in gefilterte:
        df_unternehmen = df_clean[df_clean["company"] == unternehmen]
        df_unternehmen = df_unternehmen.groupby("year")["document_count"].sum().sort_index()

        if len(df_unternehmen) >= 2:
            differenz = df_unternehmen.iloc[-1] - df_unternehmen.iloc[0]
            tendenzen[unternehmen] = differenz

    if not tendenzen:
        return " Nicht genügend Daten für einen Vergleich."

    bestes = max(tendenzen, key=tendenzen.get)
    vergleich_text = ", ".join([f"{k}: {'+' if v >= 0 else ''}{v}" for k, v in tendenzen.items()])
    # Analytische Formulierung im professionellen Stil
    teile = []
    for unternehmen, diff in tendenzen.items():
        t = f"{unternehmen} {'steigerte sich um' if diff >= 0 else 'verzeichnete einen Rückgang von'} {abs(diff)} Dokumenten"
        teile.append(t)

    beschreibung = "; ".join(teile)

    #  Balkendiagramm erstellen
    plt.figure(figsize=(6, 4))
    farben = ["green" if v >= 0 else "red" for v in tendenzen.values()]
    plt.bar(tendenzen.keys(), tendenzen.values(), color=farben)
    plt.title("Dokumentenzuwachs 2019–2024")
    plt.ylabel("Differenz der Dokumentenanzahl")
    plt.tight_layout()

    dateiname = "vergleich_tendenzen.png"
    plt.savefig(dateiname, dpi=300)
    plt.show()

    print(f"📁 Grafik gespeichert als: {dateiname}")

    return f" Vergleichsergebnis:\nIm Zeitraum 2019–2024 zeigt **{bestes}** eine stärkere Wachstumstendenz.\n{beschreibung}."
