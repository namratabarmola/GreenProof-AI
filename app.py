import streamlit as st
import pandas as pd
from document_verification import analyze_document
from document_reader import extract_text
from reason_extractor import extract_failure_reason
from final_decision import final_audit
from smart_report_generator import generate_smart_report
from html_report_generator import generate_html_report
from duplicate_detection.image_compare import compare_with_database
st.set_page_config(
    page_title="GreenProof AI",
    page_icon="🌱",
    layout="wide"
)

st.sidebar.title("🌱 GreenProof AI")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Duplicate Detection",
        "Geo-tag Verification",
        "Document Verification",
        "Intelligent Failure Analysis",
        "Final Audit Report",
        "Admin Panel"
    ]
)

if page == "Dashboard":
    st.title("🌍 GreenProof AI")
    st.subheader("AI-Based Plantation Verification & Fraud Detection System")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Reports", "128")

    with col2:
        st.metric("Verified Cases", "91")

    with col3:
        st.metric("Fraud Cases", "37")

    st.info("AI-powered plantation verification dashboard for fraud detection and sustainability monitoring.")

elif page == "Duplicate Detection":

    import os

    st.header("🖼 AI-Based Duplicate Plantation Detection")

    uploaded_images = st.file_uploader(
        "Upload Plantation Images",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )

    if uploaded_images:

        st.success(f"{len(uploaded_images)} image(s) uploaded successfully")

        upload_folder = "uploaded_images"
        os.makedirs(upload_folder, exist_ok=True)

        database_folder = "database_images"

        for img in uploaded_images:

            # Save uploaded image
            image_path = os.path.join(
                upload_folder,
                img.name
            )

            with open(image_path, "wb") as f:
                f.write(img.getbuffer())

            st.image(img, caption=img.name, width=300)

            # Compare with database
            similarity, status, risk, matched = compare_with_database(
                image_path,
                database_folder
            )

            # Display results
            st.subheader("🔍 Duplicate Detection Result")

            st.write(f"Similarity Score: {similarity}%")
            st.write(f"Detection Status: {status}")
            st.write(f"Fraud Risk Level: {risk}")

            if matched:
                st.write(f"Matched Database Image: {matched}")

            # Risk alerts
            if risk == "High Fraud Risk":
                st.error("⚠ Possible Duplicate Plantation Image Detected")

            elif risk == "Medium Fraud Risk":
                st.warning("⚠ Similar Plantation Image Found")

            else:
                st.success("✅ No Duplicate Image Detected")

            st.markdown("---")

elif page == "Document Verification":
    st.header("📄 Document Verification using BERT")

    uploaded_file = st.file_uploader(
        "Upload Report File",
        type=["pdf", "txt", "jpg", "jpeg", "png"]
    )

    if uploaded_file:
        st.success(f"Uploaded: {uploaded_file.name}")

        if st.button("Analyze Document"):

            report_text = extract_text(uploaded_file)

            if report_text.strip() == "":
                st.warning("No readable text found in file.")

            else:
                score, status, confidence, flags = analyze_document(report_text)

                st.success(f"Authenticity Score: {score}/100")
                st.info(f"Document Status: {status}")
                st.write(f"Confidence Level: {confidence}")

                if flags:
                    st.warning("Explainable AI Output")
                    for item in flags:
                        st.write(f"• {item}")

                # Auto Extract Failure Reasons
                detected_reasons, area_type = extract_failure_reason(report_text)

                st.subheader("🌱 Extracted Failure Reasons")

                if detected_reasons:
                    for reason in detected_reasons:
                        st.write(f"• {reason}")
                else:
                    st.write("No clear failure reason detected")

                st.write(f"Detected Area Type: {area_type}")

                # Save for next page
                st.session_state["detected_reasons"] = detected_reasons
                st.session_state["area_type"] = area_type
                st.session_state["document_score"] = score

                st.success(
                    "Data saved for Failure Analysis → Open Root Cause Analysis page"
                )
# Root Cause Analysis / Failure Validation Page
# Save all required values into session_state
# so LLM Report Generator can use real values

elif page == "Intelligent Failure Analysis":

    st.header("🌱 Failure Reason Validation Engine")
    st.header("🧠 Intelligent Failure Analysis Engine")
    st.info("AI-based validation of plantation failure claims")

    # -----------------------------------
    # Get values from previous page
    # -----------------------------------
    detected_reasons = st.session_state.get(
        "detected_reasons",
        []
    )

    area_type = st.session_state.get(
        "area_type",
        "Rural"
    )

    st.subheader("Detected Failure Reasons")

    if detected_reasons:
        for reason in detected_reasons:
            st.write(f"• {reason}")
    else:
        st.write("No failure reason detected")

    st.write(f"Detected Area Type: {area_type}")

    # -----------------------------------
    # Manual validation fields
    # -----------------------------------
    rainfall_status = st.selectbox(
        "Actual Rainfall Status",
        ["Low", "Normal"],
        key="rainfall_validation"
    )

    irrigation_status = st.selectbox(
        "Irrigation Budget Released?",
        ["Yes", "No"],
        key="irrigation_validation"
    )

    geo_tag_status = st.selectbox(
        "Geo-tag Status",
        ["Found", "Missing"],
        key="geo_validation"
    )

    duplicate_found = st.selectbox(
        "Duplicate Image Found?",
        ["No", "Yes"],
        key="duplicate_validation"
    )

    # -----------------------------------
    # Final validation engine
    # -----------------------------------
    if st.button("Validate Failure Reason"):

        score = 100
        final_status = "Successfully Verified Plantation"

        # Basic logic
        if rainfall_status == "Low":
            score -= 10

        if irrigation_status == "No" and area_type == "Urban":
            score -= 30

        if geo_tag_status == "Missing":
            score -= 25

        if duplicate_found == "Yes":
            score -= 35

        # Final status decision
        if score >= 80:
            final_status = "Successfully Verified Plantation"

        elif score >= 60:
            final_status = "Genuine Failure"

        elif score >= 40:
            final_status = "Suspicious Failure Reason"

        else:
            final_status = "Likely Fake Plantation"

        # -----------------------------------
        # Save for Final Audit Page
        # -----------------------------------
        st.session_state["failure_status"] = final_status
        st.session_state["failure_score"] = score
        st.session_state["failure_reasons"] = detected_reasons
        st.session_state["rainfall_status"] = rainfall_status
        st.session_state["irrigation_status"] = irrigation_status
        st.session_state["geo_status"] = geo_tag_status
        st.session_state["area_type"] = area_type

        st.success(f"Final Status: {final_status}")
        st.success(f"Trust Score: {score}/100")

        st.info(
            "Data saved successfully → Open Final Audit Report page"
        )
        # Final classification
        if score >= 50:
            final_status = "Genuine Failure 🌱"

        elif score >= 20:
            final_status = "Suspicious Failure Reason ⚠"

        else:
            final_status = "Likely Fake Plantation ❌"

        st.success(f"Failure Validation Score: {score}")
        st.info(f"Final Result: {final_status}")

        st.subheader("🧠 Explainable AI Output")

        for item in reasons:
            st.write(f"• {item}")

        # Save results for Final Audit page
        st.session_state["failure_status"] = final_status
        st.session_state["failure_score"] = score
        st.session_state["failure_reasons"] = reasons
# app.py → Final Audit Report Section (LLM Integration)

# app.py → Final Audit Report Section (HTML Report Version)

elif page == "Final Audit Report":

    st.header("📄 Final Audit Report Generator")
    st.info("LLM-based Hindi + English Official Audit Report")

    # -----------------------------------
    # Get values from previous pages
    # -----------------------------------
    final_status = st.session_state.get(
        "failure_status",
        "Successfully Verified Plantation"
    )

    trust_score = st.session_state.get(
        "failure_score",
        80
    )

    failure_reasons = st.session_state.get(
        "failure_reasons",
        ["No major issue detected"]
    )

    rainfall_status = st.session_state.get(
        "rainfall_status",
        "Normal"
    )

    irrigation_status = st.session_state.get(
        "irrigation_status",
        "Yes"
    )

    geo_tag_status = st.session_state.get(
        "geo_status",
        "Found"
    )

    area_type = st.session_state.get(
        "area_type",
        "Rural"
    )

    # -----------------------------------
    # Language Selection
    # -----------------------------------
    report_language = st.selectbox(
        "Select Report Language",
        ["English", "Hindi"],
        key="report_language_final"
    )

    # -----------------------------------
    # Generate LLM Report
    # -----------------------------------
    if st.button("Generate AI Audit Report"):
        from smart_report_generator import generate_smart_report
        from html_report_generator import generate_html_report
        with st.spinner("Generating AI-based official report..."):

            # Step 1 → Generate report text using LLM
            generated_report = generate_smart_report(
                final_status,
                trust_score,
                failure_reasons,
                rainfall_status,
                irrigation_status,
                geo_tag_status,
                area_type,
                report_language
            )

            st.subheader("🧠 AI Generated Audit Report")
            st.write(generated_report)

            # Step 2 → Generate HTML Report
            html_path = generate_html_report(
                final_status,
                trust_score,
                failure_reasons,
                generated_report,
                report_language
            )

            st.success("HTML Report Generated Successfully ✅")
            st.info(
                "Browser opened automatically → Press Ctrl + P → Save as PDF"
            )

            st.write(f"Generated File: {html_path}")
elif page == "Admin Panel":
    st.header("🛠 Admin Panel")
    st.info("Admin monitoring and approval system")

    if st.button("Approve Verified Cases"):
        st.success("Approved successfully ✅")

else:
    st.header(page)
    st.info("This page is ready for your AI module integration.")
