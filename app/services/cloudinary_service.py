import os
import cloudinary
import cloudinary.uploader
from app.config import CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET

# Configure Cloudinary with environment variables
cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
    secure=True
)

# Maximum file size in bytes (100MB)
MAX_FILE_SIZE = 100 * 1024 * 1024

def upload_pdf_to_cloudinary(file_bytes, filename):
    """
    Uploads a PDF file to Cloudinary.

    Args:
        file_bytes (bytes): The content of the PDF file.
        filename (str): The name of the file.

    Returns:
        str: The URL of the uploaded PDF on Cloudinary.

    Raises:
        RuntimeError: If the file is too large or if the upload fails.
    """
    try:
        # Check file size
        if len(file_bytes) > MAX_FILE_SIZE:
            raise RuntimeError(f"File size exceeds maximum limit of {MAX_FILE_SIZE / (1024 * 1024)}MB")

        # Upload to Cloudinary
        response = cloudinary.uploader.upload(
            file_bytes,
            resource_type="raw",
            public_id=os.path.splitext(filename)[0],
            overwrite=True,
            format="pdf"
        )

        # Verify upload was successful
        if not response.get("secure_url"):
            raise RuntimeError("Cloudinary upload failed: No secure URL returned")

        return response.get("secure_url")
    except cloudinary.exceptions.Error as e:
        raise RuntimeError(f"Cloudinary API error: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Cloudinary upload failed: {str(e)}")
