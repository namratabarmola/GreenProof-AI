def calculate_trust_score(
    duplicate_found,
    geo_status,
    document_score,
    survival_score
):
    score = 0

    if duplicate_found == "No":
        score += 25

    if geo_status == "Found ✅":
        score += 25

    score += int(document_score * 0.25)
    score += int(survival_score * 0.25)

    if score >= 80:
        status = "VERIFIED PLANTATION ✅"
    elif score >= 50:
        status = "NEEDS MANUAL REVIEW ⚠"
    else:
        status = "HIGH FRAUD RISK ❌"

    return score, status