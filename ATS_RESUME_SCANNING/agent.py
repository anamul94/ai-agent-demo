import os
from dotenv import load_dotenv

from langchain_aws import ChatBedrock
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
import pandas as pd
from schemas import Resume, Grade

load_dotenv()


model = ChatBedrock(
    model_id="apac.amazon.nova-pro-v1:0",
    region=os.getenv("REGION_NAME"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    beta_use_converse_api=True,
)

from langchain_core.prompts import PromptTemplate
async def grade_resume(resume: str, jd: str, requirements:str = "") -> Grade:
    """
    Function to grade a resume using the Bedrock model.
    """
    # Convert the resume object to a dictionary
    # resume_dict = resume.dict()

    # Create the prompt for the model
    template = """
You are an expert in evaluating resumes for applicant tracking systems.

Evaluate the following resume based on the job description and determine if the candidate is a suitable match.

Resume: {resume}

Job Description: {jd}
Special Requirements (if any): {requirements}

Use the following criteria for evaluation:
- Relevance to the job description (skills, experience, qualifications)
- Clarity and conciseness of the resume content
- Formatting and professional presentation
- Overall suitability and impression

Respond with only one word: `true` if the resume is a good fit for the job, otherwise `false`.

Do not include any explanation or additional text.
"""

    # Call the model with the prompt
    llm_with_structured_output = model.with_structured_output(Grade)
    prompt = PromptTemplate.from_template(template)
    grad_chain = prompt | llm_with_structured_output

    # Extract the grade from the response
    grade = await grad_chain.ainvoke({"resume": resume, "jd": jd, "requirements": requirements})

    return grade.grade


async def evaluate_resume(resume: Resume, jd: str, config, requirements: str = "",) -> Grade:
    """
    Function to evaluate a resume using the Bedrock model.
    """
    # Convert the resume object to a dictionary

    template = """
You are an expert in evaluating resumes for applicant tracking systems.

Evaluate the following resume based on the job description and determine if the candidate is a suitable match.

Resume: {resume}

Job Description: {jd}
Special Requirements (if any): {requirements}

Use the following criteria for evaluation:
- Relevance to the job description (skills, experience, qualifications)
- Clarity and conciseness of the resume content
- Formatting and professional presentation
- Overall suitability and impression
Do not include any explanation or additional text.
"""

    # Call the model with the prompt
    llm_with_structured_output = model.with_structured_output(Resume)
    prompt = PromptTemplate.from_template(template)
    resume_chain = prompt | llm_with_structured_output
    result = await resume_chain.ainvoke(
        {"resume": resume, "jd": jd, "requirements": requirements},
        config={"callbacks": [config]},
    )
    return result

async def extract_resume_data( file_path:str, jd: str, config, requirements: str = "") -> None:
    directory_path = Path("./resume")

    for file in directory_path.iterdir():
        if file.is_file():
            # print(f"Reading: {file}")
            loader = PyPDFLoader(file_path=file)

            docs = loader.load()
            content = "".join([doc.page_content for doc in docs])
            # content = file.read_text(encoding="utf-8")
            grade = await grade_resume(content, jd, requirements)
            print("Scanning Resume: " + str(file))
            if grade:
                result = await evaluate_resume(content, jd, config, requirements)
                df = pd.DataFrame(list(result), columns=["Field", "Value"])

                df_columnwise = df.set_index("Field").T.reset_index(drop=True)
                df_columnwise["filename"] = file.name

                # print(df)

                # Check if the file already exists
                if os.path.exists(file_path):
                    existing_df = pd.read_excel(file_path, engine="openpyxl")
                    updated_df = pd.concat([existing_df, df_columnwise], ignore_index=True)
                    updated_df.to_excel(file_path, index=False, engine="openpyxl")
                else:
                    # If file doesn't exist, create a new file
                    df_columnwise.to_excel(file_path, index=False, engine="openpyxl")
                    # print(result)
            print(grade)
