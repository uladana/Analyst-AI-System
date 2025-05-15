📊 Multimodales KI-System für Marktanalysen

Ein Abschlussprojekt im Rahmen des Intensivkurses zu Generativer KI. Ziel ist die Entwicklung eines intelligenten Multi-Agenten-Systems zur Beantwortung marktbezogener Fragen auf Basis offizieller Investor-Relations-Dokumente großer Tech-Konzerne.

🚀 Projektübersicht

Dieses multimodale KI-System kann:

Marktbezogene Fragen beantworten
Anlageeinsichten liefern
Historische Marktdaten analysieren
Prognosen erstellen
Finanzdaten visuell darstellen
Die Datenquelle beschränkt sich ausschließlich auf IR-Dokumente (2020–2024) von: Apple, Microsoft, Google, NVIDIA und Meta.

🧠 Systemarchitektur

Das System basiert auf einem modularen Multi-Agenten-Framework mit folgenden Agenten:

1. 🎛️ Multimodaler RAG-Agent

Funktion: Beantwortet multimodale Anfragen (Text, Tabellen, Diagramme, Bilder, PDFs)
Technologien: CLIP, SentenceTransformers, Chroma, Gemini
2. 📈 Data-Science- und Analyse-Agent

Funktion: Trendanalysen, Prognosemodelle, Visualisierungen
Technologien: Pandas, scikit-learn, Prophet, ARIMA, Plotly, Gemini
3. 🌐 Websuche- und Echtzeitmarkt-Agent

Funktion: Live-Marktnachrichten, Stimmungsanalysen, Ereignisse
Technologien: SerpAPI, Tavily, BeautifulSoup, NewsAPI
4. 🤝 Koordinations-Agent

Funktion: Teilaufgabenverteilung und Ergebnisaggregation
Technologien: LangChain, LangGraph, Gemini
(Optional) 5. ✅ Qualitäts- und Ethik-Agent

Funktion: Faktenprüfung, ethische Validierung
Technologien: GPT Moderation API, Hugging Face Evaluation Suite
🗓️ Projektablauf (Agil)

Woche 1

Datensammlung & IR-Vorverarbeitung
RAG- und Analyse-Agenten entwickeln
Woche 2

Web-Agent & Koordination implementieren
UI mit Gradio entwickeln
Qualitätssicherung & Deployment
💻 Technologien & Tools

Bereich	Tools / Frameworks
Embeddings	CLIP, SentenceTransformers
Datenanalyse	Pandas, scikit-learn
Prognosemodelle	Prophet, ARIMA
Visualisierung	Matplotlib, Plotly
UI-Entwicklung	Gradio
Agent-Frameworks	LangChain, LangGraph
Moderation	GPT Moderation API
Zusammenarbeit	GitHub, Jira
📦 Abgaben

✅ Gradio-App (z. B. über Hugging Face Spaces)
✅ GitHub-Repository mit Dokumentation
✅ Jira-Dokumentation (User Stories, Tasks, Epics)
✅ Präsentation inkl. Live-Demo
✅ Technischer Abschlussbericht
🎯 Lernziele

Multimodale Informationsverarbeitung & Generative KI
Finanzanalysen und Prognoseerstellung
Web Scraping und API-Integration
Agile Teamarbeit & Softwareentwicklung
Praxisrelevante Systemarchitektur und UI-Design
🔗 Weiterführende Ressourcen

LangGraph: Workflows & Agents
Agent Supervisor mit LangChain
Multimodales RAG mit semi-strukturierten Daten
Multimodale Inputs in LangChain
Quellenangabe in RAG-Systemen
Zitationen in QA mit RAG
📬 Kontakt

Für Fragen oder Beiträge zum Projekt:
[Dein Name oder GitHub-Nutzername]
📧 [Deine E-Mail oder Kontaktinfo]

Dieses Projekt wurde im Rahmen eines KI-Intensivkurses entwickelt und simuliert realitätsnahe Anwendungen, wie sie aktuell in der Industrie eingesetzt werden.