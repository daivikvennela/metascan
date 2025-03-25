import os
import boto3
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
S3_BUCKET = 'testmetascan'
BEDROCK_MODEL_ID = os.environ.get('BEDROCK_MODEL_ID', 'anthropic.claude-3-5-haiku-20241022-v1:0')

# Initialize AWS clients
s3_client = boto3.client('s3')
bedrock_runtime = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')

def read_from_s3(key):
    """Read content from S3 bucket with encoding fallback."""
    try:
        response = s3_client.get_object(Bucket=S3_BUCKET, Key=key)
        content = response['Body'].read()
        # Try UTF-8 first
        try:
            return content.decode('utf-8')
        except UnicodeDecodeError:
            # If UTF-8 fails, try with latin-1
            try:
                logger.warning(f"UTF-8 decoding failed for {key}, falling back to latin-1")
                return content.decode('latin-1')
            except UnicodeDecodeError:
                # If latin-1 fails, try with cp1252
                logger.warning(f"latin-1 decoding failed for {key}, falling back to cp1252")
                return content.decode('cp1252')
    except Exception as e:
        logger.error(f"Error reading from S3: {str(e)}")
        raise

def download_from_s3(key, local_path):
    """Download a file from S3 to a local path."""
    try:
        s3_client.download_file(S3_BUCKET, key, local_path)
        logger.info(f"Successfully downloaded {key} from S3 to {local_path}")
    except Exception as e:
        logger.error(f"Error downloading from S3: {str(e)}")
        raise

def invoke_bedrock_model(prompt):
    """Invoke Bedrock model with the given prompt."""
    try:
        body = json.dumps({
            "prompt": prompt,
            "max_tokens_to_sample": 300,
            "temperature": 0.7,
            "top_p": 0.9,
        })
        response = bedrock_runtime.invoke_model(
            body=body,
            modelId=BEDROCK_MODEL_ID,
            accept='application/json',
            contentType='application/json'
        )
        return json.loads(response['body'].read())['completion']
    except Exception as e:
        logger.error(f"Error invoking Bedrock model: {str(e)}")
        raise

def main():
    
    try:

        # Read script from S3
        script_content = read_from_s3('daivikresume.pdf')
        logger.info("Successfully read script from S3")

        s3_key = 'daivikresume.pdf'
        local_file_path = 'local_daivikresume.pdf'

        # # Download the file from S3
        download_from_s3(s3_key, local_file_path)
        # # Prepare prompt for LLM
        prompt = f"Analyze the following article and suggest improvements:\n\n{script_content}"

        # # Invoke Bedrock model
        llm_response = invoke_bedrock_model(prompt)
        logger.info("Successfully received response from Bedrock model")

        # # Write LLM response back to S3
        #write_to_s3('results/analysis_result.txt', llm_response)
        #logger.info("Analysis result written to S3")




    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
