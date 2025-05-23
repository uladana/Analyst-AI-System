import gradio as gr
from Websuche_Agent import get_latest_news  # Verwenden der bestehenden Funktion aus a.py

def run_agent_ui(company):
    # Abruf der Nachrichten und Analyse über die vorhandene Funktion
    get_latest_news(company)
    filename = f"{company}_news.json"
    with open(filename, "r", encoding="utf-8") as f:
        data = f.read()
    return data

# Gradio-Interface definieren
demo = gr.Interface(
    fn=run_agent_ui,
    inputs=gr.Textbox(
        label="Unternehmensname (z. B. Google)",
        placeholder="Gib einen Firmennamen ein..."
    ),
    outputs=gr.Textbox(
        label="Ergebnisse (Nachrichten, Sentiment, Zusammenfassung im JSON-Format)",
        lines=20
    ),
    title="📈 Echtzeit Markt-Agent",
    description="Gib einen Firmennamen ein, um aktuelle Finanznachrichten, Zusammenfassungen und Sentimentanalysen zu erhalten."
)

# Start des Web-Interface
if __name__ == "__main__":
    demo.launch()
