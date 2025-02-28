from langchain_community.document_loaders import CSVLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from config import config
import pandas as pd
import os
import json


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
        # text = f"Guidelines: {row['Secure Coding Guidelines']}"
        text = f"Preconditions: {row['Preconditions']}"
        #    row['Secure Coding Guidelines']}"
        doc = Document(
            page_content=text,
            metadata={
                "id": row["ID"],
                "guidelines": row["Secure Coding Guidelines"],
                "cwe_id": row["CWE-ID"]
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


def query_vector_db(query: str, db, k: int = 10):

    results = db.similarity_search(query, k=k)
    for doc in results:
        # print(doc)
        doc.page_content += f"\nGuidelines: {doc.metadata["guidelines"]}"
    return results


def read_Sallms_tasks(file_path: str):
    security_eval_tasks = []
    with open(file_path, 'r') as file:
        for line in file:
            data = json.loads(line)
            security_eval_tasks.append(data.get('prompt', '').strip())
    return security_eval_tasks


def read_SecurityEval_tasks(file_path: str):
    security_eval_tasks = []
    with open(file_path, 'r') as file:
        for line in file:
            data = json.loads(line)
            security_eval_tasks.append(data.get('Prompt', '').strip())
    return security_eval_tasks


def prompt_template(task: str, preconditions_guidelines: list[str]):
    # task_prompt = f"Generate secure Python code for the following:\n {task}"
    task_prompt = f"{task}\n"
    # additional_info = "\nHere are some additional security guidelines to follow if the coding task satisfies the specific preconditions:\n"
    guideline_num = 1
    info = ""
    for pair in preconditions_guidelines:
        # Access the page_content attribute of the Document object
        content = pair.page_content
        info += f"#{guideline_num}\n{content}\n"
        guideline_num += 1
    return task_prompt + info
