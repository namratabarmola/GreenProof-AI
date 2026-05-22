def final_audit(
    duplicate_found,
    geo_status,
    document_score,
    root_cause_detected
):
    score = 0
    reasons = []

    # Duplicate Detection
    if duplicate_found == "No":
        score += 30
        reasons.append("No duplicate plantation images found")
    else:
        score += 5
        reasons.append("Duplicate plantation images detected")

    # Geo-tag Verification
    if geo_status == "Found ✅":
        score += 25
        reasons.append("Geo-tag verified successfully")
    else:
        score += 5
        reasons.append("Geo-tag missing from plantation image")

    # Document Verification
    if document_score >= 80:
        score += 25
        reasons.append("Strong document authenticity score")
    elif document_score >= 50:
        score += 15
        reasons.append("Moderate document authenticity")
    else:
        score += 5
        reasons.append("Weak or suspicious plantation report")

    # Root Cause Validation
    if root_cause_detected == "Yes":
        score += 20
        reasons.append("Valid plantation failure reason detected")
    else:
        reasons.append("No valid root cause found")

    # Final Decision
    if score >= 75:
        final_status = "VERIFIED ✅"
    elif score >= 50 and root_cause_detected == "Yes":
        final_status = "GENUINE BUT FAILED 🌱"
    else:
        final_status = "LIKELY FAKE ❌"

    return score, final_status, reasons