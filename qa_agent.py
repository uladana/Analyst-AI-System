# qa_agent.py

import openai
from transformers import pipeline
from evaluate import load

# === Konfiguration ===
openai.api_key = "DEIN_API_KEY"  # 🔐 Ersetze durch deinen echten Key

# === Lade Modelle ===
bias_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
fact_checker = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
rouge = load("rouge")


# === 1. Toxizität / Moderation ===
def moderate_text(text: str) -> bool:
    try:
        response = openai.Moderation.create(input=text)
        return response["results"][0]["flagged"]
    except Exception as e:
        print(f"⚠️ Fehler bei Moderation: {e}")
        return False


# === 2. Bias-Erkennung (z. B. Geschlecht, Ethnie) ===
def detect_bias(text: str):
    try:
        result = bias_classifier(
            sequence_to_classify=text,
            candidate_labels=["neutral", "gender bias", "racial bias", "toxicity", "unethisch"]
        )
        return result['labels'][0], result['scores'][0]
    except Exception as e:
        print(f"⚠️ Fehler bei Bias-Erkennung: {e}")
        return "unbekannt", 0.0


# === 3. Faktentreue / Konsistenzprüfung ===
def fact_check(statement: str, reference_text: str):
    try:
        result = fact_checker(
            sequence_to_classify=statement,
            candidate_labels=["wahr", "falsch"],
            hypothesis_template="Dieser Satz ist {} basierend auf dem Kontext."
        )
        return result["labels"][0], result["scores"][0]
    except Exception as e:
        print(f"⚠️ Fehler bei Faktenprüfung: {e}")
        return "unbekannt", 0.0


# === 4. Evaluierung (Zusammenfassung, Antwortqualität) ===
def evaluate_summary(reference: str, generated: str):
    try:
        return rouge.compute(predictions=[generated], references=[reference])
    except Exception as e:
        print(f"⚠️ Fehler bei ROUGE-Evaluierung: {e}")
        return {}


# === 5. Gesamtprüfung einer Antwort ===
def run_qa_check(answer: str, reference_text: str = ""):
    result = {}

    # Schritt 1: Moderation
    result["flagged_moderation"] = moderate_text(answer)

    # Schritt 2: Bias
    bias_label, bias_score = detect_bias(answer)
    result["bias_label"] = bias_label
    result["bias_score"] = bias_score

    # Schritt 3: Faktentreue (nur wenn Kontext gegeben)
    if reference_text.strip():
        fact_label, fact_score = fact_check(answer, reference_text)
        result["fact_check"] = {"label": fact_label, "score": fact_score}
    else:
        result["fact_check"] = {"label": "nicht geprüft", "score": 0.0}

    return result
