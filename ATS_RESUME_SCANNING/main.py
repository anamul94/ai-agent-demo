import streamlit as st
from agent import extract_resume_data
import asyncio
import pandas as pd
from pathlib import Path
from langfuse.callback import CallbackHandler

langfuse_handler = CallbackHandler(
    public_key=
    secret_key=
    host=,
)

st.title("AI-Powered Resume Screening and Evaluation System")
st.subheader(
    "This project is an intelligent resume screening and evaluation system designed to assist hiring teams in efficiently shortlisting candidates"
)


FILE_NAME = "resume_evaluation.xlsx"
jd = st.text_area("Job Description", height=200)
requirements = st.text_area("Special Requirements (if any)", height=200)

async def handle_resume_extraction(jd, requirements):
    with st.spinner("Extracting resume data..."):
        resume_data = await extract_resume_data(FILE_NAME, jd, langfuse_handler, requirements)
        # st.json(resume_data)


if st.button("Scan Resumes"):
    if jd:
        asyncio.run(handle_resume_extraction(jd, requirements))
        df = pd.read_excel(FILE_NAME)
        st.write("Resume Data Extracted:")
        st.dataframe(df)
    else:
        st.warning("Please enter a job description.")
