import requests
import os
import json  # 🔺 NEU: Für das Speichern der Ergebnisse als JSON
from transformers import pipeline   
from textblob import TextBlob  # 🔺 NEU: Für Sentimentanalyse

# API-Schlüssel – direkt einfügen oder über Umgebungsvariable setzen
NEWS_API_KEY = "a012ad2d427b46fa95b99003107ee99a"


# Initialisierung des Summarization-Modells
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# 🔺 NEU: Funktion zur Sentimentanalyse
def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0.1:
        return "positive"
    elif polarity < -0.1:
        return "negative"
    else:
        return "neutral"
    
    
    
# Zusammenfassung der Artikel drucken
def summarize_articles(articles):   
    combined_text = " ".join([a['title'] + ". " + (a['description'] or "") for a in articles])
    summary = summarizer(combined_text[:3000], max_length=150, min_length=30, do_sample=False)[0]['summary_text']
    print("\n🧠 Zusammenfassung der Nachrichten:")
    print(summary)

# Hauptfunktion zum Abrufen und Verarbeiten von Nachrichten
def get_latest_news(company_name, max_results=5):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": company_name,
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": max_results,
        "apiKey": NEWS_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data.get("status") != "ok":
        print("❌ Fehler:", data.get("message"))
        return []

    articles = data.get("articles", [])
    for i, article in enumerate(articles, 1):
        print(f"\n🔹 Nachricht {i}: {article['title']}")
        print(f"📰 Quelle: {article['source']['name']}")
        print(f"🔗 Link: {article['url']}")
        print(f"🕒 Datum: {article['publishedAt']}")
        print(f"📄 Beschreibung: {article['description']}")
        
        
    summarize_articles(articles)  # Hier rufen wir die Zusammenfassung auf
    
    # 🔺 NEU: Sentimentanalyse hinzufügen
    for article in articles:
        text = article['title'] + ". " + (article['description'] or "")
        article['sentiment'] = analyze_sentiment(text)

    # 🔺 NEU: Zusammenfassung erneut generieren für die Datei
    combined_text = " ".join([a['title'] + ". " + (a['description'] or "") for a in articles])
    summary = summarizer(combined_text[:3000], max_length=150, min_length=30, do_sample=False)[0]['summary_text']

    # 🔺 NEU: Ergebnisse als JSON speichern
    result = {
        "company": company_name,
        "articles": articles,
        "summary": summary
    }

    with open(f"{company_name}_news.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Die Ergebnisse wurden in {company_name}_news.json gespeichert.")


# Testweise Ausführung
if __name__ == "__main__":
    get_latest_news("Google")
    
    #sdfghjklög
