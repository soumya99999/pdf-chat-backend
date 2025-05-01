import fitz  # PyMuPDF

def extract_text_from_pdf(file_path: str) -> str:
    try:
        with fitz.open(file_path) as doc:
            text = "\n".join([page.get_text() for page in doc])
        return text
    except Exception as e:
        raise RuntimeError(f"Failed to extract text from PDF: {e}")
