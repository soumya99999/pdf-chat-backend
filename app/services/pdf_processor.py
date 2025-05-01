import fitz  # PyMuPDF

def extract_text_from_pdf_bytes(file_bytes: bytes) -> str:
    try:
        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            text = "\n".join([page.get_text() for page in doc])
        return text
    except Exception as e:
        raise RuntimeError(f"Failed to extract text from PDF bytes: {e}")
