from code_generation.gpt4 import CodeGenerator
from vector_db_gen import load_vector_db, create_vector_db, query_vector_db
from config import config


def read_LLMSecEval_Py(file_path: str):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        return lines


def prompt_template(task: str, preconditions_guidelines: list[str]):
    task_prompt = f"Generate secure code for the following task: {task}"
    additional_info = f"Here are some additional security guidelines to follow if the coding task satisfies the specific preconditions:\n"
    count = 1
    for pair in preconditions_guidelines:
        info = f"#{count}\n{pair}\n"
        count += 1
    return task_prompt + additional_info + info


def generate_code(full_prompt: str, prompt_id: str):
    code_generator = CodeGenerator()
    code = code_generator.generate_response(full_prompt, prompt_id)
    output_path = f"{config.code_output_dir}/{prompt_id}.py"
    code_generator.write_code_to_file(code, output_path)
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
        prompt_id = f"{config.prompt_id_prefix}{count}"
        preconditions_guidelines = query_vector_db(task, db)
        full_prompt = prompt_template(task, preconditions_guidelines)
        generate_code(full_prompt, prompt_id)
        count += 1
