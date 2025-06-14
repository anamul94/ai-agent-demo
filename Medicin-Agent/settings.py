from dotenv import load_dotenv
import os
load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION_NAME = os.getenv("REGION_NAME")
INFERENCE_PROFILE_ARN = os.getenv("INFERENCE_PROFILE_ARN")
INFERENCE_PROFILE_ID = os.getenv("INFERENCE_PROFILE_ID")
MODEl_ARN = os.getenv("MODEL_ARN")

