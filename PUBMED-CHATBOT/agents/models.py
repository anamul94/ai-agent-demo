from langchain_aws import ChatBedrock
from settings import (
    INFERENCE_PROFILE_ARN,
    INFERENCE_PROFILE_ID,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    REGION_NAME,
)

nova_model = ChatBedrock(
    model_id="apac.amazon.nova-pro-v1:0",  # Use the inference profile ID
    region_name=REGION_NAME,  # Specify your AWS region
    beta_use_converse_api=True,  # Enable the Converse API
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    cache=None,
    temperature=0.3,
    verbose=True,
)
