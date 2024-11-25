from langchain_community.document_loaders import CSVLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from config import config
import pandas as pd
import os


def create_vector_db():
    # Check if database already exists
    if os.path.exists(os.path.join(config.persist_dir, "chroma.sqlite3")):
        print("Database already exists. Loading existing database...")
        return load_vector_db()

    print("Creating new database...")
    embeddings = OpenAIEmbeddings(
        model=config.embedding_model,
        openai_api_key=os.environ.get("OPENAI_API_KEY")
    )

    # Read CSV and create documents
    df = pd.read_csv(config.guidelinescsv_file)
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
        persist_directory=config.persist_dir
    )
    vectordb.persist()
    return vectordb


def load_vector_db():
    if not os.path.exists(os.path.join(config.persist_dir, "chroma.sqlite3")):
        raise FileNotFoundError(
            f"No existing database found in {config.persist_dir}")

    print("Loading existing database...")
    embeddings = OpenAIEmbeddings(
        model=config.embedding_model,
        openai_api_key=os.environ.get("OPENAI_API_KEY")
    )
    return Chroma(
        persist_directory=config.persist_dir,
        embedding_function=embeddings
    )


def query_vector_db(query: str, db, k: int = 4):

    results = db.similarity_search(query, k=k)
    return results


if __name__ == "__main__":
    try:
        # Try to load existing database first
        db = load_vector_db()
    except FileNotFoundError:
        # Create new database if none exists
        db = create_vector_db()

    # Example query
    results = query_vector_db("The code is a simple login page that takes a username and password and checks if the username and password are in the database. If they are; it redirects to success. If they are not it redirects to cant_login. If there is an error it redirects to internal_server_error.", db)
    for doc in results:
        print(doc.page_content)
