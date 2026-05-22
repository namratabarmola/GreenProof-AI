def extract_failure_reason(text):
    text = text.lower()

    detected_reasons = []

    keywords = {
        "Low Rainfall": [
            "low rainfall",
            "less rainfall",
            "rainfall shortage",
            "drought",
            "कम वर्षा",
            "कम बारिश",
            "सूखा"
        ],

        "Poor Soil": [
            "poor soil",
            "bad soil",
            "soil issue",
            "खराब मिट्टी",
            "मिट्टी की समस्या"
        ],

        "Lack of Irrigation": [
            "lack of irrigation",
            "no irrigation",
            "water shortage",
            "सिंचाई की कमी",
            "पानी की कमी",
            "सिंचाई नहीं"
        ],

        "Wrong Tree Species": [
            "wrong species",
            "unsuitable species",
            "गलत प्रजाति",
            "अनुपयुक्त प्रजाति"
        ],

        "Animal Damage": [
            "animal damage",
            "damaged by animals",
            "grazing",
            "जानवरों से नुकसान",
            "पशु नुकसान"
        ]
    }

    for reason, phrases in keywords.items():
        for phrase in phrases:
            if phrase.lower() in text:
                detected_reasons.append(reason)
                break

    # Area detection
    if "rural" in text or "ग्रामीण" in text:
        area_type = "Rural"

    elif "urban" in text or "शहरी" in text:
        area_type = "Urban"

    else:
        area_type = "Not Clearly Mentioned"

    return detected_reasons, area_type