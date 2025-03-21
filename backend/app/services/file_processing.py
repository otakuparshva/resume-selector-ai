from .s3_service import upload_to_s3
from ..config import Config
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract
import docx
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def extract_text_from_file(file):
    try:
        if file is None:
            return ""
        
        if file.type == "application/pdf":
            reader = PdfReader(file)
            text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
            return text if text else "No text could be extracted from this PDF."
        
        elif file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"]:
            doc = docx.Document(file)
            return "\n".join([para.text for para in doc.paragraphs])
        
        elif file.type in ["image/jpeg", "image/png"]:
            image = Image.open(file)
            return pytesseract.image_to_string(image)
        
        else:
            return f"Unsupported file type: {file.type}"
        
    except Exception as e:
        logger.error(f"Error extracting text from file: {e}")
        return f"Error processing file: {str(e)}"

def save_resume_to_s3(file, job_id, candidate_email):
    try:
        object_name = f"{job_id}/{candidate_email}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        file_url = upload_to_s3(file, Config.S3_BUCKET_NAME, object_name)
        return file_url
    except Exception as e:
        logger.error(f"Error saving resume to S3: {e}")
        return None