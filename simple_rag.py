from code_generation.gpt4 import CodeGenerator
from vector_db_gen import load_vector_db, create_vector_db, query_vector_db
from config import config


def read_LLMSecEval_Py(file_path: str):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        return lines


def prompt_template(task: str, preconditions_guidelines: list[str]):
    task_prompt = f"Generate secure Python code for the following task: {task}"
    additional_info = "Here are some additional security guidelines to follow if the coding task satisfies the specific preconditions:\n"
    guideline_num = 1
    info = ""
    for pair in preconditions_guidelines:
        # Access the page_content attribute of the Document object
        content = pair.page_content
        info += f"#{guideline_num}\n{content}\n"
        guideline_num += 1
    return task_prompt + additional_info + info


def generate_code(full_prompt: str, prompt_id: str):
    code_generator = CodeGenerator()
    code = code_generator.generate_response(full_prompt, prompt_id)
    code_generator.write_code_to_file(prompt_id, code)
    prompt_file = f"output/rag_prompts/{prompt_id}.txt"
    with open(prompt_file, "w") as file:
        file.write(full_prompt)
    return


if __name__ == "__main__":
    coding_tasks = read_LLMSecEval_Py(config.prompt_dataset_file)

    try:
        # Try to load existing database first
        db = load_vector_db()
    except FileNotFoundError:
        # Create new database if none exists
        db = create_vector_db()

    count = 1
    for task in coding_tasks:

        print(f"Generating code for task {count}")
        prompt_id = f"{config.prompt_id_prefix}{count}"
        preconditions_guidelines = query_vector_db(task, db)
        full_prompt = prompt_template(task, preconditions_guidelines)
        generate_code(full_prompt, prompt_id)
        count += 1
