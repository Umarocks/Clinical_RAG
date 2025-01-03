from flask import Flask, request
from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.document_loaders import PDFPlumberLoader
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.prompts import PromptTemplate
from flask_cors import CORS
app = Flask(__name__)
CORS(app) 
folder_path = "db"

cached_llm = Ollama(model="llama3")

embedding = FastEmbedEmbeddings()

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
        sources.append(
             {"title": doc.metadata["source"].replace("../PDF/", ""),"type":"Medical Protocol", "page_content": doc.page_content,"relevance":doc.metadata["page"]-11}
        )
        doc.metadata

    response_answer = {"answer": result["answer"], "sources": sources}
    # response_answer = {"sources": sources}
    return response_answer


@app.route("/pdf", methods=["POST"])
def pdfPost():

    loader = PDFPlumberLoader("../PDF/RPHCM_CPM_Manual_5thEd.pdf")
    docs = loader.load_and_split()
    print(f"docs len={len(docs)}")

    chunks = text_splitter.split_documents(docs)
    print(f"chunks len={len(chunks)}")

    vector_store = Chroma.from_documents(
        documents=chunks, embedding=embedding, persist_directory=folder_path
    )

    vector_store.persist()

    response = {
        "status": "Successfully Uploaded",
        "doc_len": len(docs),
        "chunks": len(chunks),
        "page1": docs[0].page_content,
    }
    return response


def start_app():
    app.run()


if __name__ == "__main__":
    start_app()