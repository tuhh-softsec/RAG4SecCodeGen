
from code_generation.gpt4 import CodeGenerator
from config import config
import json


response = CodeGenerator()


def read_SecurityEval_tasks(file_path: str):
    security_eval_tasks = []
    with open(file_path, 'r') as file:
        for line in file:
            data = json.loads(line)
            security_eval_tasks.append(data.get('Prompt', '').strip())
    return security_eval_tasks


def read_Sallms_tasks(file_path: str):
    security_eval_tasks = []
    with open(file_path, 'r') as file:
        for line in file:
            data = json.loads(line)
            security_eval_tasks.append(data.get('prompt', '').strip())
    return security_eval_tasks


def read_LLMSecEval_Py(file_path: str):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        return lines


if __name__ == "__main__":
    # Read tasks from a file
    tasks = read_Sallms_tasks(config.prompt_dataset_file)

    count = 1
    # Process each task
    for task in tasks:
        task_id = f"{config.prompt_id_prefix}{count}"
        task_prompt = f"Generate secure Python code for the following: {task}"
        print(task_prompt)
        final_answer = response.generate_response(task_prompt, task_id)
        response.write_code_to_file(task_id, final_answer)
        count += 1
