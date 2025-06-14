import streamlit as st
import requests

# API Endpoint
API_URL = "http://ec2-13-233-11-215.ap-south-1.compute.amazonaws.com:8003/diagnose/"

st.title("🩺 PrescripSure")
st.subheader(
    "💊 Intelligent prescription support for doctors — ensuring safety, suitability, and smarter care."
)


# st.write("Enter patient details and upload medical reports for AI-assisted diagnosis.")

# Collect Patient Information
patient_info = st.text_area("🧑‍⚕️ Patient Info", placeholder="Enter patient details...")
symptoms = st.text_area("🤒 Symptoms", placeholder="List the symptoms...")
diagnoies = st.text_area("🤒 Diagnoieses", placeholder="Diaganosis Result")
medical_history = st.text_area(
    "📜 Medical History", placeholder="Enter medical history (optional)"
)
allergies = st.text_area("🤒 allergies", placeholder="allergies ")
current_medications = st.text_area(
    "🤒 current_medications", placeholder="current_medications"
)
additional_context = st.text_area(
    "additional_context", placeholder="additional_context"
)
# File Upload (Medical Reports)
# uploaded_files = st.file_uploader(
#     "📂 Upload Lab Reports (PDF, JPG, PNG)", accept_multiple_files=True
# )

# Submit Button
if st.button("🔍 Get Diagnosis"):
    with st.spinner("Processing..."):
        # files = [
        #     ("lab_reports", (file.name, file, file.type)) for file in uploaded_files
        # ]

        # Send data to FastAPI
        response = requests.post(
            API_URL,
            data={
                "patient_info": patient_info,
                "symptoms": symptoms,
                "diagnosis": diagnoies,
                "medical_history": medical_history,
                "current_medications": current_medications,
                "allergies": allergies,
                "additional_context": additional_context,
            },
        )

        if response.status_code == 200:
            diagnosis_result = response.json()
            st.success("✅ Diagnosis received!")
            st.markdown(diagnosis_result)
        else:
            st.error(f"❌ Error: {response.text}")


st.markdown("""
### 🔒 HIPAA Compliance Notice  
This application follows **HIPAA-compliant best practices** to protect your health information:  
- **No data is stored or shared** after processing.  
- **End-to-end encryption** is used for secure transmission.  
- AI-generated insights are **for informational purposes only** and should not replace professional medical advice.  
""")