from transformers import pipeline

# Lightweight pretrained model
classifier = pipeline(
    "text-classification",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

def analyze_document(text):
    score = 100
    flags = []

    suspicious_words = [
        "many trees",
        "highly successful",
        "excellent results",
        "positive impact",
        "successful campaign",
        "overall successful",
        "impactful",
        "encouraging results",
        "कम वर्षा",
        "सिंचाई की कमी",
        "बहुत सफल अभियान"
    ]

    important_keywords = [
        "date",
        "district",
        "location",
        "geo-tag",
        "saplings",
        "neem",
        "watering",
        "maintenance",
        "irrigation",
        "दिनांक",
        "स्थान",
        "पौधे",
        "सिंचाई"
    ]

    # Rule-based detection
    for word in suspicious_words:
        if word.lower() in text.lower():
            score -= 10
            flags.append(f"Detected phrase: {word}")

    found_keywords = 0

    for keyword in important_keywords:
        if keyword.lower() in text.lower():
            found_keywords += 1

    if found_keywords < 3:
        score -= 25
        flags.append("Missing measurable plantation details")

    if len(text.split()) < 40:
        score -= 15
        flags.append("Report too short / weak evidence")

    # BERT semantic check
    try:
        bert_result = classifier(text[:512])[0]

        label = bert_result["label"]
        confidence_score = round(bert_result["score"] * 100, 2)

        if label == "NEGATIVE":
            score -= 20
            flags.append("BERT detected suspicious semantic pattern")

    except:
        confidence_score = 75
        flags.append("BERT fallback used")

    # Final classification
    if score >= 80:
        status = "Likely Genuine ✅"
        confidence = "High"

    elif score >= 50:
        status = "Suspicious ⚠"
        confidence = "Medium"

    else:
        status = "Likely Fake ❌"
        confidence = "High"

    return score, status, confidence, flags