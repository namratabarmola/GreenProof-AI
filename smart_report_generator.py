def generate_smart_report(
    final_status,
    trust_score,
    failure_reasons,
    rainfall_status,
    irrigation_status,
    geo_tag_status,
    area_type,
    report_language
):
    """
    Controlled Professional Report Generator
    Stable Hindi + English official report generation
    """

    # Default reasons
    if not failure_reasons:
        if report_language == "Hindi":
            failure_reasons = ["कोई प्रमुख समस्या नहीं मिली"]
        else:
            failure_reasons = ["No major issue detected"]

    # Reason translation for Hindi
    if report_language == "Hindi":

        reason_map = {
            "No major issue detected": "कोई प्रमुख समस्या नहीं मिली",
            "Low rainfall": "कम वर्षा",
            "Water shortage": "पानी की कमी",
            "Poor maintenance": "खराब रखरखाव",
            "No irrigation": "सिंचाई सुविधा का अभाव",
            "Duplicate image found": "डुप्लिकेट छवि पाई गई",
            "Geo-tag missing": "जियो टैग अनुपलब्ध",
            "Fake plantation suspected": "संभावित फर्जी वृक्षारोपण",
            "Officer explanation mismatch": "अधिकारी के स्पष्टीकरण में असंगति",

            "Eaten by animals": "पशुओं द्वारा नष्ट",
            "Destroyed by animals": "पशुओं द्वारा नष्ट",
            "Damaged by animals": "पशुओं द्वारा क्षति",
            "Plants eaten by animals": "पौधों को पशुओं द्वारा खा लिया गया"
        }

        translated_reasons = []

        for reason in failure_reasons:
            translated_reasons.append(
                reason_map.get(reason, reason)
            )

        failure_reasons = translated_reasons

    reasons_text = ", ".join(failure_reasons)

    # Value translation for Hindi
    if report_language == "Hindi":

        value_map = {
            "Normal": "सामान्य",
            "Low": "कम",
            "High": "अधिक",

            "Yes": "उपलब्ध",
            "No": "अनुपलब्ध",

            "Found": "प्राप्त",
            "Missing": "अनुपलब्ध",

            "Rural": "ग्रामीण",
            "Urban": "शहरी",

            "Successfully Verified Plantation": "सफलतापूर्वक सत्यापित वृक्षारोपण",
            "Genuine Failure": "वास्तविक विफलता",
            "Suspicious Failure Reason": "संदिग्ध विफलता",
            "Likely Fake Plantation": "संभावित फर्जी वृक्षारोपण"
        }

        rainfall_status = value_map.get(rainfall_status, rainfall_status)
        irrigation_status = value_map.get(irrigation_status, irrigation_status)
        geo_tag_status = value_map.get(geo_tag_status, geo_tag_status)
        area_type = value_map.get(area_type, area_type)
        final_status = value_map.get(final_status, final_status)

    # Hindi report
    if report_language == "Hindi":
        report = f"""
अंतिम ऑडिट रिपोर्ट के अनुसार वृक्षारोपण स्थल का सफलतापूर्वक सत्यापन किया गया।

जियो टैग स्थिति: {geo_tag_status}
वर्षा स्थिति: {rainfall_status}
सिंचाई व्यवस्था: {irrigation_status}
क्षेत्र प्रकार: {area_type}

प्रमुख निष्कर्ष:
{reasons_text}

उपलब्ध अभिलेखों एवं स्थल सत्यापन के आधार पर कोई महत्वपूर्ण विसंगति प्राप्त नहीं हुई।

अतः यह वृक्षारोपण वास्तविक एवं सफलतापूर्वक सत्यापित माना जाता है।

सिफारिश:
वृक्षारोपण क्षेत्र की नियमित निगरानी, संरक्षण एवं रखरखाव सुनिश्चित किया जाए।
"""

    # English report
    else:

        report = f"""
Final audit report confirms that the plantation site has been successfully verified.

Geo-tag status: {geo_tag_status}
Rainfall status: {rainfall_status}
Irrigation status: {irrigation_status}
Area type: {area_type}

Key observations:
{reasons_text}

No major discrepancies were found.

Recommendation:
Regular monitoring and maintenance should be continued.
"""

    return report.strip()