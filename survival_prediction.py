def predict_survival(
    soil,
    rainfall,
    irrigation,
    tree_species,
    maintenance
):
    """
    Predict plantation survival probability
    using environmental conditions
    """

    score = 0
    reasons = []

    # -----------------------------------
    # Soil Quality
    # -----------------------------------
    if soil == "Good":
        score += 20
        reasons.append("Good soil quality detected")

    elif soil == "Average":
        score += 10
        reasons.append("Average soil quality")

    else:
        reasons.append("Poor soil quality")

    # -----------------------------------
    # Rainfall
    # -----------------------------------
    if rainfall == "High":
        score += 20
        reasons.append("High rainfall support")

    elif rainfall == "Moderate":
        score += 10
        reasons.append("Moderate rainfall support")

    else:
        reasons.append("Low rainfall detected")

    # -----------------------------------
    # Irrigation
    # -----------------------------------
    if irrigation == "Yes":
        score += 20
        reasons.append("Irrigation facility available")

    else:
        reasons.append("No irrigation support")

    # -----------------------------------
    # Tree Species Suitability
    # -----------------------------------
    if tree_species == "Correct":
        score += 20
        reasons.append("Suitable tree species selected")

    else:
        reasons.append("Unsuitable tree species")

    # -----------------------------------
    # Maintenance
    # -----------------------------------
    if maintenance == "Good":
        score += 20
        reasons.append("Good plantation maintenance")

    elif maintenance == "Average":
        score += 10
        reasons.append("Average maintenance quality")

    else:
        reasons.append("Poor maintenance detected")

    # -----------------------------------
    # Final Prediction
    # -----------------------------------
    if score >= 80:

        result = "High Survival Chance 🌱"

        recommendation = (
            "Plantation conditions are highly favorable."
        )

    elif score >= 50:

        result = "Medium Survival Chance ⚠"

        recommendation = (
            "Additional monitoring and irrigation recommended."
        )

    else:

        result = "Low Survival Chance ❌"

        recommendation = (
            "Immediate intervention required to improve survival."
        )

    return {
        "score": score,
        "result": result,
        "reasons": reasons,
        "recommendation": recommendation
    }