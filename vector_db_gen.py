from langchain_community.document_loaders import CSVLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
import pandas as pd
import os


def create_vector_db(csv_file_path: str, persist_directory: str):
    # Check if database already exists
    if os.path.exists(os.path.join(persist_directory, "chroma.sqlite3")):
        print("Database already exists. Loading existing database...")
        return load_vector_db(persist_directory)

    print("Creating new database...")
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=os.environ.get("OPENAI_API_KEY")
    )

    # Read CSV and create documents
    df = pd.read_csv(csv_file_path)
    documents = []
    for idx, row in df.iterrows():
        text = f"Preconditions: {row['Preconditions']}\nGuideline: {
            row['Secure Coding Guidelines']}"
        doc = Document(
            page_content=text,
            metadata={
                "id": row["ID"],
                "cwe_id": row["ID.1"]
            }
        )
        documents.append(doc)

    # Create and persist vector store
    vectordb = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    vectordb.persist()
    return vectordb


def load_vector_db(persist_directory: str):
    if not os.path.exists(os.path.join(persist_directory, "chroma.sqlite3")):
        raise FileNotFoundError(
            f"No existing database found in {persist_directory}")

    print("Loading existing database...")
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=os.environ.get("OPENAI_API_KEY")
    )
    return Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )


def query_vector_db(query: str, vectordb, k: int = 3):

    results = vectordb.similarity_search(query, k=k)
    return results


if __name__ == "__main__":
    csv_file = "dataset/secure_coding_guidelines.csv"
    persist_dir = "chroma_db"

    try:
        # Try to load existing database first
        db = load_vector_db(persist_dir)
    except FileNotFoundError:
        # Create new database if none exists
        db = create_vector_db(csv_file, persist_dir)

    # Example query
    results = query_vector_db("The code is a simple login page that takes a username and password and checks if the username and password are in the database. If they are; it redirects to success. If they are not it redirects to cant_login. If there is an error it redirects to internal_server_error.", db)
    for doc in results:
        print(doc.page_content)
