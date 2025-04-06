from flask import Flask, request,jsonify

# from langchain_community.vectorstores import Chroma
# from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain import hub
# from langchain_community.document_loaders import PDFPlumberLoader
# from langchain_community.document_loaders import PyPDFLoader
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.prompts import PromptTemplate
from flask_cors import CORS
from langchain_openai import OpenAIEmbeddings
from pdf2image import convert_from_path
from langchain_openai import ChatOpenAI
from langchain import hub
from io import BytesIO
from PyPDF2 import PdfReader, PdfWriter
from transformers import AutoTokenizer
# from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker
from langchain_docling.loader import ExportType
from langchain_docling import DoclingLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain.schema import Document

import os
import base64
import openai

app = Flask(__name__)
CORS(app) 
folder_path = "db"
with open("../OPEN_AI_API.txt", "r") as file:
    os.environ["OPENAI_API_KEY"] = file.read().strip()  
os.environ["KMP_DUPLICATE_LIB_OK"] = "True"
client = openai.OpenAI() 
# cached_llm = Ollama(model="llama3")
cached_llm = ChatOpenAI(model="gpt-4o")
# tokenizer =   AutoTokenizer.from_pretrained("gpt2-large")
tokenizer = "sentence-transformers/all-MiniLM-L6-v2"
embedding = OpenAIEmbeddings(model="text-embedding-3-small")

# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=1024, chunk_overlap=80, length_function=len, is_separator_regex=False
# )
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50, separator="\n")

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

@app.route("/get_pdf_page", methods=["POST"])
def get_pdf_page_Post(poppler_path=POPPLER_PATH):

    """
    Extracts a specific page from a PDF, converts it to an image, and encodes it to Base64.

    Args:
        pdf_path (str): Path to the input PDF.
        page_number (int): 1-based page number to extract.
        poppler_path (str): Path to the Poppler binaries.

    Returns:
        dict: Contains the Base64-encoded image and file name.
    """
    json_content = request.json
    pdf_path = json_content.get("pdf_path")
    # page_number = [3,4]
    page_numbers = json_content.get("page_number", [])

    page_number_offset=0
    # pdf_path = request.args.get("pdf_path")
    # page_number = int(request.args.get("page_number"))
    if(pdf_path == "Clinical Validation and Documentation for Coding _eCDCG25_eBook.pdf"):
        page_number_offset+=4
    if(pdf_path == "ICD_Cm_Expert_for_Hospitals.pdf"):
        page_number_offset+=16
    if(pdf_path == "DRG Expert _2025_eBook.pdf"):
        page_number_offset+=4
    if(pdf_path == "Coders Desk Reference for ICD 10 CM Diagnoses eITDRD25_eBook.pdf"):
        page_number_offset+=8
    pdf_path="../PDF/Clinical Documentation/Clinical Documentation/"+pdf_path
    encoded_image = []
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
        for page_number in page_numbers:
            writer.add_page(reader.pages[page_number - 1])  # Convert to zero-indexed
            with open(temp_pdf_path, "wb") as f:
                writer.write(f)

            # Convert the extracted page to an image
            pages = convert_from_path(temp_pdf_path, 500, poppler_path=poppler_path)
            converted_page = pages[0]
            converted_page.save(output_image_path, "JPEG")

            # Encode the image to Base64
            with open(output_image_path, "rb") as img_file:
                encoded_image.append(base64.b64encode(img_file.read()).decode("utf-8"))

            # Clean up temporary files
            os.remove(temp_pdf_path)
            os.remove(output_image_path)

        return jsonify({"page_image": encoded_image })
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
    # vector_store = Chroma(persist_directory="./db/", embedding_function=embedding)
    vector_store = FAISS.load_local(
        "faiss_index", embedding, allow_dangerous_deserialization=True
    )
    print("vector store loaded")
    raw_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    print("Creating chain")
    # retriever = vector_store.as_retriever(
    #     search_type="similarity_score_threshold",
    #     search_kwargs={
    #         "k": 10,
    #         "score_threshold": 0.2,
    #     },
    # )
    print("retreiver created")
    combine_docs_chain = create_stuff_documents_chain(
       cached_llm, raw_prompt
    )
    # document_chain = create_stuff_documents_chain(cached_llm, raw_prompt)
    print("document chain created")
    # chain = create_retrieval_chain(retriever, document_chain)
    print("chain created")
    retrieval_chain = create_retrieval_chain(
       vector_store.as_retriever(kwargs=2), combine_docs_chain
    )
    result = retrieval_chain.invoke({"input": query, "context": vector_store})

    # print(result)
    # for res in result[:2]:
    #     print(res)
    #     print("...\n\n")
    sources = []
    # for doc in result["context"]:
    #     # pdfJson = process_pdf_page(doc.metadata["source"], doc.metadata["page"]+1);
    #     # sources.append(
    #     #      {"title": doc.metadata["source"].replace("../PDF/Clinical Documentation/Clinical Documentation/", ""),"type":"Medical Protocol", "page_image":pdfJson,"page_content":doc.page_content ,"relevance":doc.metadata["page"]-11}
    #     # )
    #     sources.append(
    #          {"title": doc.metadata["source"].replace("../PDF/Clinical Documentation/Clinical Documentation/", ""),"type":"Medical Protocol", "page_image":"pdfJson","page_content":doc.page_content ,"relevance":doc.metadata.prov["page_no"]}
    #     )
        
    #     # doc.metadata

    for doc in result["context"]:
        # pdfJson = get_pdf_page_Post(doc.metadata["source"], doc['metadata']['dl_meta']['doc_items'][0]['prov'][0]['page_no']);
        # sources.append(
        #      {"title": doc.metadata["source"].replace("../PDF/Clinical Documentation/Clinical Documentation/", ""),"type":"Medical Protocol", "page_image":pdfJson,"page_content":doc.page_content ,"relevance":doc.metadata["page"]-11}
        # )
        page_no = []
        for item in doc.metadata['dl_meta']['doc_items']:
            for prov in item['prov']:
                page_no.append(prov['page_no'])
        sources.append(
            {
                "title": doc.metadata["source"].replace("../PDF/Clinical Documentation/Clinical Documentation/", ""),
                "type": "Medical Protocol",
                "page_image": "pdfJson",  # Adjust this line
                "page_content": doc.page_content,
                "relevance": list(set(page_no))  # Ensure only unique page numbers are included
            }
        )
        print(sources)
        print("....\n\n\n")
    # for doc in result['context']:
    #     page_content = doc.get('page_content', '')
    #     try:
    #         page_no = doc['metadata']['dl_meta']['doc_items'][0]['prov'][0]['page_no']
    #     except (KeyError, IndexError):
    #         page_no = 'Unknown'
    #     print(f"Page {page_no}:")
    #     print(page_content)
    #     print("-" * 50)

    response_answer = {"answer": result["answer"], "sources": sources}
    # response_answer = {"answer": result["answer"]}
    
    return response_answer



# @app.route("/pdf", methods=["POST"])
# def pdfPost():
#     try:
#         # Load and split PDF documents
#         EXPORT_TYPE = ExportType.MARKDOWN
#         FILE_PATH = "../PDF/Clinical Documentation/Clinical Documentation/Clinical Validation and Documentation for Coding _eCDCG25_eBook.pdf"
#         # loader =  DocumentConverter().convert("../PDF/Clinical Documentation/Clinical Documentation/DRG Expert _2025_eBook.pdf")
#         # print("loader loaded")
#         # docs = loader
#         # print(f"docs len={len(docs)}")
#         loader = DoclingLoader(
#             file_path=FILE_PATH,
#             export_type=EXPORT_TYPE,
#             chunker=HybridChunker(tokenizer=embedding.tokenizer),
#         )

#         docs = loader.load()
#         splitter = MarkdownHeaderTextSplitter(
#                 headers_to_split_on=[
#                     ("#", "Header_1"),
#                     ("##", "Header_2"),
#                     ("###", "Header_3"),
#                 ],
#             )
#         splits = [split for doc in docs for split in splitter.split_text(doc.page_content)]
#         # Split documents into smaller chunks
#         # chunks = text_splitter.split_documents(docs)
#         # chunker = HybridChunker(tokenizer=AutoTokenizer.from_pretrained(embedding));
#         # # print(f"chunks len={len(chunks)}")

#         # # Generate embeddings using OpenAI API

#         # chunk_texts = [chunk.page_content for chunk in chunks]

#         # # Create vector store using OpenAI embeddings
#         # # vector_store = Chroma.from_documents(
#         # #     documents=chunks,
#         # #     embedding=embedding,
#         # #     persist_directory="./db"
#         # # )
#         vector_store = FAISS.from_documents(splits, embedding)
#         vector_store.save_local("faiss_index")
        

#         # # Persist vector store
#         # vector_store.persist()

#         # Prepare response
#         response = {
#             "status": "Successfully Uploaded",
#             "doc_len": len(docs),
#             "chunks": len(splits),
#             "page1": docs[0].page_content,
#         }
#         return response, 200

#     except Exception as e:
#         return {"status": "Error", "message": str(e)}, 500

@app.route("/pdf", methods=["POST"])
def pdfPost():
    try:
        # Load and split PDF documents
        EXPORT_TYPE = ExportType.DOC_CHUNKS
        FILE_PATH = "../PDF/Clinical Documentation/Clinical Documentation/A1.pdf"
        loader = DoclingLoader(
            file_path=FILE_PATH,
            export_type=EXPORT_TYPE,
            chunker=HybridChunker(tokenizer=tokenizer),
        )

        docs = loader.load()
        # splits = docs
        splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("#", "Header_1"),
            ("##", "Header_2"),
            ("###", "Header_3"),
        ],
        )
        splits = []
        for doc in docs:
            # Split the document content with header metadata
            doc_splits = splitter.split_text(doc.page_content)
            
            # Add position-aware metadata
            for split_idx, split in enumerate(doc_splits):
                # Merge existing metadata with header metadata
                # print(f"doc.metadata={doc.metadata}")
                merged_metadata = {
                    **doc.metadata,              # Original document metadata
                    **split.metadata,            # Header metadata from markdown
                    "split_id": split_idx + 1,   # Add position information
                    "total_splits": len(doc_splits),
                    "parent_doc": doc.metadata.get("source", FILE_PATH)
                }
                
                # Create new document with combined information
                new_doc = Document(
                    page_content=split.page_content,
                    metadata=merged_metadata
                )
                splits.append(new_doc)
        # print(splits)
        for d in splits[:1]:
            print(f"- {d}")
            print("...")
        print("Loading vector store")
        vector_store = FAISS.from_documents(splits, embedding)
        vector_store.save_local("faiss_index")
        

        # # Persist vector store
        # vector_store.persist()

        # Prepare response
        response = {
            "status": "Successfully Uploaded",
            "doc_len": len(docs),
            "chunks": len(splits),
            "page1": docs[0].page_content,

        }
        return response, 200
        

    except Exception as e:
        return {"status": "Error", "message": str(e)}, 500
    

def start_app():
    app.run(debug=True)


if __name__ == "__main__":
    start_app()

    