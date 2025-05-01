import google.generativeai as genai
from langchain.text_splitter import CharacterTextSplitter
from app.config import GEMINI_API_KEY

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Use the correct model ID
model = genai.GenerativeModel('models/gemini-1.5-flash')  # or 'models/gemini-1.5-pro'

def answer_question(document_text: str, question: str) -> str:
    try:
        # Split document into manageable chunks
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        texts = text_splitter.split_text(document_text)
        
        # Join chunks into a context string
        context = "\n\n".join(texts)
        prompt = f"""You are a helpful assistant. Based on the following document, answer the user's question.
If the answer cannot be found in the document, say "The answer is not available in the document."

Document:
{context}

Question: {question}

Answer:"""

        # Generate and return response
        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        raise RuntimeError(f"Failed to process question: {e}")
