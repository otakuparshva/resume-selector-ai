import boto3
from botocore.exceptions import NoCredentialsError
import logging
from ..config import Config

logger = logging.getLogger(__name__)

def upload_to_s3(file, bucket_name, object_name):
    s3 = boto3.client(
        's3',
        aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
        region_name=Config.AWS_REGION
    )
    try:
        s3.upload_fileobj(file, bucket_name, object_name)
        logger.info(f"File uploaded to S3: {object_name}")
        return f"https://{bucket_name}.s3.amazonaws.com/{object_name}"
    except NoCredentialsError:
        logger.error("AWS credentials not available")
        return None
    except Exception as e:
        logger.error(f"Error uploading to S3: {e}")
        return None