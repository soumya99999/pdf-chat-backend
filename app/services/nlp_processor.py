from langchain_ollama import OllamaLLM
from langchain.chains.question_answering import load_qa_chain
from langchain.docstore.document import Document as LangDocument
from langchain.text_splitter import CharacterTextSplitter

llm = OllamaLLM(model="llama3")  # Make sure `ollama run llama3` is active

def answer_question(document_text: str, question: str) -> str:
    try:
        # Split into chunks
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        texts = text_splitter.split_text(document_text)
        docs = [LangDocument(page_content=t) for t in texts]

        # QA chain using LangChain
        chain = load_qa_chain(llm, chain_type="stuff")
        result = chain.invoke({"input_documents": docs, "question": question})
        return result["output_text"]
    except Exception as e:
        raise RuntimeError(f"Failed to process question: {e}")
