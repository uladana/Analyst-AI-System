import requests
import os
from transformers import pipeline   # 🔺

# Falls du keine .env-Datei verwendest, kannst du den API-Key direkt hier einfügen
NEWS_API_KEY = "a012ad2d427b46fa95b99003107ee99a"


# 🔺 Summarizer initialisieren
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


def summarize_articles(articles):   # 🔺
    combined_text = " ".join([a['title'] + ". " + (a['description'] or "") for a in articles])
    summary = summarizer(combined_text[:3000], max_length=150, min_length=30, do_sample=False)[0]['summary_text']
    print("\n🧠 Zusammenfassung der Nachrichten:")
    print(summary)


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
        
        
    summarize_articles(articles)  # 🔺 Hier rufen wir die Zusammenfassung auf

# Testweise Ausführung der Funktion
if __name__ == "__main__":
    get_latest_news("Google")
