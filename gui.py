import gradio as gr
from dotenv import load_dotenv
from rag_with_qa_gemini import qa_chain, run_qa_check
import pandas as pd
import plotly.express as px
import os

load_dotenv()

# === Beispiel-Chart ===
def generate_sample_chart():
    df = pd.DataFrame({
        "Quartal": ["Q1", "Q2", "Q3", "Q4"],
        "Umsatz (Mrd $)": [18.4, 20.1, 22.3, 24.7]
    })
    fig = px.bar(df, x="Quartal", y="Umsatz (Mrd $)", title="Umsatzentwicklung NVIDIA FY24")
    return fig

# === Frage beantworten + QA ===
def answer_and_validate(user_query):
    try:
        antwort = qa_chain.invoke({"query": user_query})
        antwort_text = antwort["result"]
        quellen = antwort["source_documents"]
        kontext = "\n".join([doc.page_content for doc in quellen])
        qa_result = run_qa_check(antwort_text, kontext)

        quellen_text = "\n".join([
            f"- {doc.metadata.get('source', '?')} (Seite {doc.metadata.get('page', '?')})"
            for doc in quellen
        ])

        result = f"**Antwort:**\n{antwort_text}\n\n**Quellen:**\n{quellen_text}\n\n"
        result += "**QA-Prüfung:**\n"
        for k, v in qa_result.items():
            result += f"- {k}: {v}\n"

        return result

    except Exception as e:
        return f"❌ Fehler: {str(e)}"

# === Gradio UI ===
demo = gr.Blocks()

with demo:
    gr.Markdown("# Multimodales KI-System mit Gemini")
    with gr.Row():
        frage = gr.Textbox(label="Ihre Frage", placeholder="Z. B. Wie war NVIDIAs Umsatz im Q4 2024?")
        antwortfeld = gr.Markdown(label="Antwort & QA")
    frage.submit(fn=answer_and_validate, inputs=frage, outputs=antwortfeld)

    with gr.Row():
        gr.Markdown("### 📊 Beispielhafte Umsatzentwicklung")
        plot = gr.Plot(label="Chart")
        gr.Button("Chart anzeigen").click(fn=generate_sample_chart, inputs=[], outputs=plot)

    with gr.Row():
        gr.Markdown("### 🧠 Agentensteuerung")
        gr.Markdown("""
        - 🤖 Retriever-Agent (ChromaDB)
        - ✨ Gemini LLM (Google Generative AI)
        - 🔍 QA-/Ethik-Agent für Prüfung
    """)

if __name__ == "__main__":
    demo.launch()
