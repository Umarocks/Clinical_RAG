
from langchain_text_splitters import MarkdownHeaderTextSplitter
from transformers import AutoTokenizer
from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker
from langchain_docling.loader import ExportType
from langchain_docling import DoclingLoader
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from docling.chunking import HybridChunker
import openai
from langchain_community.vectorstores import FAISS
import os


with open("./OPEN_AI_API.txt", "r") as file:
    os.environ["OPENAI_API_KEY"] = file.read().strip()  

print("openai.api_key", os.environ["OPENAI_API_KEY"])
client = openai.OpenAI() 
embedding = OpenAIEmbeddings(model="text-embedding-3-small")
tokenizer =   AutoTokenizer.from_pretrained("gpt2-large")

def pdfPost():
    try:
        # Load and split PDF documents
        EXPORT_TYPE = ExportType.MARKDOWN
        FILE_PATH = "./PDF/Clinical Documentation/Clinical Documentation/A1.pdf"
        loader = DoclingLoader(
            file_path=FILE_PATH,
            export_type=EXPORT_TYPE,
            chunker=HybridChunker(tokenizer=tokenizer),
        )

        docs = loader.load()
        splitter = MarkdownHeaderTextSplitter(
                headers_to_split_on=[
                    ("#", "Header_1"),
                    ("##", "Header_2"),
                    ("###", "Header_3"),
                ],
            )
        splits = [split for doc in docs for split in splitter.split_text(doc.page_content)]

        vector_store = FAISS.from_documents(splits, embedding)
        vector_store.save_local("faiss_index")
        # Prepare response
        return({
            "status": "Successfully Uploaded",
            "doc_len": len(docs),
            "chunks": len(splits),
            "page1": docs[0].page_content,
        })
        

    except Exception as e:
        return {"status": "Error", "message": str(e)}, 500
    

answer=pdfPost();
print(answer)