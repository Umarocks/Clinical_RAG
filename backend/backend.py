from flask import Flask, request,jsonify
from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.document_loaders import PDFPlumberLoader
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.prompts import PromptTemplate
from flask_cors import CORS
from langchain.embeddings import OpenAIEmbeddings
from pdf2image import convert_from_path
from langchain_openai import ChatOpenAI
from io import BytesIO
from PyPDF2 import PdfReader, PdfWriter
from pdf2image import convert_from_path
import os
import base64
import openai

app = Flask(__name__)
CORS(app) 
folder_path = "db"
with open("../OPEN_AI_API.txt", "r") as file:
    os.environ["OPENAI_API_KEY"] = file.read().strip()  
    # openai.api_key = file.read().strip()
client = openai.OpenAI() 
# cached_llm = Ollama(model="llama3")
cached_llm = ChatOpenAI(model="gpt-4o")

embedding = OpenAIEmbeddings()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1024, chunk_overlap=80, length_function=len, is_separator_regex=False
)

raw_prompt = PromptTemplate.from_template(
    """ 
    you are an assistant to a doctor and provide comprehensive answewrs to the question.if you are not sure about the answer, say you are not sure in short in a polite way. 
    if the question is irrelevant, say the question is irrelevant in a polite way and say you can only help with medical related questions.
     {input}
     {context}
           Answer:
    
"""
)

TEMP_FOLDER = "./temp"
os.makedirs(TEMP_FOLDER, exist_ok=True)

POPPLER_PATH = "C:/poppler-24.08.0/Library/bin"  # Update with your Poppler path

def process_pdf_page(pdf_path, page_number, poppler_path=POPPLER_PATH):
    """
    Extracts a specific page from a PDF, converts it to an image, and encodes it to Base64.

    Args:
        pdf_path (str): Path to the input PDF.
        page_number (int): 1-based page number to extract.
        poppler_path (str): Path to the Poppler binaries.

    Returns:
        dict: Contains the Base64-encoded image and file name.
    """
    try:
        # Validate file existence
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"File '{pdf_path}' does not exist")

        # Prepare paths
        temp_pdf_path = os.path.join(TEMP_FOLDER, "extracted_page.pdf")
        output_image_path = os.path.join(TEMP_FOLDER, "converted_page.jpg")

        # Extract the specified page
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        writer.add_page(reader.pages[page_number - 1])  # Convert to zero-indexed
        with open(temp_pdf_path, "wb") as f:
            writer.write(f)

        # Convert the extracted page to an image
        pages = convert_from_path(temp_pdf_path, 500, poppler_path=poppler_path)
        converted_page = pages[0]
        converted_page.save(output_image_path, "JPEG")

        # Encode the image to Base64
        with open(output_image_path, "rb") as img_file:
            encoded_image = base64.b64encode(img_file.read()).decode("utf-8")

        # Clean up temporary files
        os.remove(temp_pdf_path)
        os.remove(output_image_path)

        return encoded_image

    except Exception as e:
        return {"error": str(e)}
    
@app.route("/ai", methods=["POST"])
def aiPost():
    print("Post /ai called")
    json_content = request.json
    query = json_content.get("query")

    print(f"query: {query}")

    response = cached_llm.invoke(query)

    print(response)

    response_answer = {"answer": response}
    return response_answer


@app.route("/ask_pdf", methods=["POST"])
def askPDFPost():
    print("Post /ask_pdf called")
    json_content = request.json
    query = json_content.get("query")

    print(f"query: {query}")

    print("Loading vector store")
    vector_store = Chroma(persist_directory=folder_path, embedding_function=embedding)

    print("Creating chain")
    retriever = vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            "k": 5,
            "score_threshold": 0.4,
        },
    )

    document_chain = create_stuff_documents_chain(cached_llm, raw_prompt)
    chain = create_retrieval_chain(retriever, document_chain)

    result = chain.invoke({"input": query})

    print(result)

    sources = []
    for doc in result["context"]:
        pdfJson = process_pdf_page(doc.metadata["source"], doc.metadata["page"]+1);
        sources.append(
             {"title": doc.metadata["source"].replace("../PDF/", ""),"type":"Medical Protocol", "page_image":pdfJson,"page_content":doc.page_content ,"relevance":doc.metadata["page"]-11}
        )
        doc.metadata

    response_answer = {"answer": result["answer"], "sources": sources}
    
    return response_answer


# @app.route("/pdf", methods=["POST"])
# def pdfPost():

#     loader = PDFPlumberLoader("../PDF/RPHCM_CPM_Manual_5thEd.pdf")
#     docs = loader.load_and_split()
#     print(f"docs len={len(docs)}")

#     chunks = text_splitter.split_documents(docs)
#     print(f"chunks len={len(chunks)}")

#     vector_store = Chroma.from_documents(
#         documents=chunks, embedding=embedding, persist_directory=folder_path
#     )

#     vector_store.persist()

#     response = {
#         "status": "Successfully Uploaded",
#         "doc_len": len(docs),
#         "chunks": len(chunks),
#         "page1": docs[0].page_content,
#     }
#     return response




@app.route("/pdf", methods=["POST"])
def pdfPost():
    try:
        # Load and split PDF documents
        loader = PDFPlumberLoader("../PDF/RPHCM_CPM_Manual_5thEd.pdf")
        docs = loader.load_and_split()
        print(f"docs len={len(docs)}")

        # Split documents into smaller chunks
        chunks = text_splitter.split_documents(docs)
        print(f"chunks len={len(chunks)}")

        # Generate embeddings using OpenAI API

        chunk_texts = [chunk.page_content for chunk in chunks]
        # embeddings = []
        # for text in chunk_texts:
        #     response = openai.embeddings.create(
        #         model="text-embedding-3-small",
        #         input=text
        #     ).data[0].embedding
        #     # embeddings.append(response["data"][0]["embedding"])
        #     embedding = response
        #     embeddings.append(embedding)
        # print(f"embeddings len={len(embeddings)}")
        # Create vector store using OpenAI embeddings
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embedding,
            persist_directory="./db"
        )

        # # Persist vector store
        # vector_store.persist()

        # Prepare response
        response = {
            "status": "Successfully Uploaded",
            "doc_len": len(docs),
            "chunks": len(chunks),
            "page1": docs[0].page_content,
        }
        return response, 200

    except Exception as e:
        return {"status": "Error", "message": str(e)}, 500


def start_app():
    app.run()


if __name__ == "__main__":
    start_app()