import boto3
import time
import random
from dotenv import load_dotenv
load_dotenv()

bedrock_runtime = boto3.client('bedrock-runtime')

def call_converse_with_retry(model_id, messages, max_retries=5, base_delay=0.1):
    retries = 0
    while retries <= max_retries:
        try:
            response = bedrock_runtime.converse(
                modelId=model_id,
                messages=messages
            )
            return response
        except bedrock_runtime.exceptions.ThrottlingException:
            if retries == max_retries:
                raise
            
            # Calculate delay with exponential backoff and jitter
            delay = base_delay * (2 ** retries) * (0.5 + random.random())
            print(f"Throttled. Retrying in {delay:.2f} seconds...")
            time.sleep(delay)
            retries += 1