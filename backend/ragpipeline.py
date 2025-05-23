import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.llms import LlamaCpp
from langchain_core.documents import Document
from pdf2image import convert_from_path
import pytesseract
class RAGPipeline:
    def __init__(self, model_path: str):
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.llm = LlamaCpp(
            model_path=model_path,
            n_ctx=2048,
            n_threads=4,
            temperature=0.3
        )
        self.vectorstore = None
        self.qa_chain = None

    def extract_text_from_pdf_with_ocr(self, file_path: str) -> str:
        try:
            loader = PyPDFLoader(file_path)
            docs = loader.load()
            text = " ".join([doc.page_content for doc in docs])
            if text.strip():
                return text
        except Exception:
            pass
        images = convert_from_path(file_path, dpi=300)
        ocr_text = ""
        for img in images:
            ocr_text += pytesseract.image_to_string(img)
        return ocr_text

    def load_and_split_documents(self, file_path: str) -> List[Document]:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            text = self.extract_text_from_pdf_with_ocr(file_path)
            docs = [Document(page_content=text)]
        elif ext in [".txt", ".md"]:
            loader = TextLoader(file_path)
            docs = loader.load()
        else:
            raise ValueError(f"Unsupported file extension: {ext}")

        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        split_docs = splitter.split_documents(docs)
        return split_docs
    def build_vectorstore(self, docs: List[Document]):
        self.vectorstore = FAISS.from_documents(docs, self.embeddings)

    def create_qa_chain(self):
        if self.vectorstore is None:
            raise ValueError("Vectorstore not built yet!")
        retriever = self.vectorstore.as_retriever()
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=retriever,
            return_source_documents=True,
        )

    def process_file(self, file_path: str):
        docs = self.load_and_split_documents(file_path)
        self.build_vectorstore(docs)
        self.create_qa_chain()
        return len(docs)

    def query(self, question: str):
        if self.qa_chain is None:
            return "Please upload and process a document first."
        response = self.qa_chain.invoke({"query": question})
        result = response["result"]
        return result
