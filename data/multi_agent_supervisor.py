#multiple_agent_supervisor.py

from dotenv import load_dotenv
import os
load_dotenv()  # Carga .env

from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor
from langchain_openai import ChatOpenAI

#  Importa tus herramientas
from agents.analysis_agent.explainer import generate_summary
from agents.analysis_agent.visualizations import plot_trend_by_company, plot_quarterly_trend
from agents.analysis_agent.forecast import predict_by_company
from agents.analysis_agent.agent_legacy import vergleiche_tendenzen


api_key = os.getenv("OPENAI_API_KEY")
model = ChatOpenAI(model="gpt-4", api_key=api_key)
response = model.invoke("Was ist die Hauptstadt von Frankreich?")
print(response.content)


#  Define agentes React
text_agent = create_react_agent(
    name="text_agent",
    model="openai:gpt-4",
    tools=[generate_summary],
    prompt="Erkläre Analyseergebnisse anhand von Datentabellen."
)

visual_agent = create_react_agent(
    name="visual_agent",
    model="openai:gpt-4",
    tools=[plot_trend_by_company, plot_quarterly_trend],
    prompt="Erzeuge nur visuelle Darstellungen aus den Eingabedaten."
)

forecast_agent = create_react_agent(
    name="forecast_agent",
    model="openai:gpt-4",
    tools=[predict_by_company],
    prompt="Führe Marktprognosen mit Prophet aus."
)

compare_agent = create_react_agent(
    name="compare_agent",
    model="openai:gpt-4",
    tools=[vergleiche_tendenzen],
    prompt="Vergleiche die Wachstumstendenz von Unternehmen zwischen 2019 und 2024."
)

#  Supervisor erstellen
supervisor = create_supervisor(
    model=ChatOpenAI(model="gpt-4"),
    agents=[text_agent, visual_agent, forecast_agent, compare_agent],
    prompt=(
        "Du bist ein Supervisor für vier spezialisierte Agenten:\n"
        "- text_agent: Erklärt Analyseergebnisse.\n"
        "- visual_agent: Erstellt visuelle Darstellungen.\n"
        "- forecast_agent: Führt Prognosen durch.\n"
        "- compare_agent: Führt Unternehmensvergleiche aus.\n"
        "Ordne die Aufgaben logisch und sequenziell zu. Arbeite nicht parallel."
    ),
    add_handoff_back_messages=True,
    output_mode="full_history"
).compile()

# ✅ Eingabe testen
if __name__ == "__main__":
    while True:
        prompt = input("\n Gib deine Frage ein (oder 'beenden'): ")
        if prompt.lower() in ["beenden", "exit"]:
            break
        result = supervisor.invoke(prompt)
        print("\n Antwort:")
        print(result)