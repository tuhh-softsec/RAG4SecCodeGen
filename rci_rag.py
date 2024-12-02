from code_generation.gpt4 import CodeGenerator
from config import config
from vector_db_gen import load_vector_db, create_vector_db, query_vector_db

response = CodeGenerator()


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


def rci_task_iterative(task_prompt, task_id, iterations):
    model_response = task_prompt

    # 1. Get initial answer
    initial_prompt = model_response
    model_response = response.generate_response(initial_prompt, task_id)

    for _ in range(iterations):
        # 2. Critique the response
        if model_response:
            critique_prompt = f"Review the following answer and find security problems with it: '{
                model_response}'"
            critique = response.generate_response(critique_prompt, task_id)

            if critique:
                # 3. Improve the answer
                improve_prompt = f"Based on the critique: '{
                    critique}', improve the following answer: '{model_response}'"
                model_response = response.generate_response(
                    improve_prompt, task_id)
            else:
                return f"improved output was None in iteration {_} for task {task_id}"
        else:
            return f"Critique was None in iteration {_} for task {task_id}"

    return model_response


if __name__ == "__main__":
    iterations = 2  # Set the number of iterative improvements
    # Read tasks from a file
    coding_tasks = read_LLMSecEval_Py(config.prompt_dataset_file)

    try:
        # Try to load existing database first
        db = load_vector_db()
    except FileNotFoundError:
        # Create new database if none exists
        db = create_vector_db()

    count = 1
    # Process each task
    for task in coding_tasks:
        prompt_id = f"{config.prompt_id_prefix}{count}"
        preconditions_guidelines = query_vector_db(task, db)
        full_prompt = prompt_template(task, preconditions_guidelines)
        final_answer = rci_task_iterative(full_prompt, prompt_id, iterations)
        response.write_code_to_file(prompt_id, final_answer)
        prompt_file = f"{config.prompt_file_dir}/{prompt_id}.txt"
        with open(prompt_file, "w") as file:
            file.write(full_prompt)
        count += 1
