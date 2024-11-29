
from code_generation.gpt4 import CodeGenerator
from config import config


response = CodeGenerator()


def rci_task_iterative(task, task_id, iterations):
    model_response = task

    # 1. Get initial answer
    initial_prompt = model_response
    model_response = response.generate_response(initial_prompt, task_id)
    # print("Initial response")
    # print(model_response)

    for _ in range(iterations):

        # print(f"!!!!!!!Iteration {_}!!!!!!")
        # 2. Critique the response
        if model_response:
            critique_prompt = f"Review the following answer and find security problems with it: '{
                model_response}'"
            critique = response.generate_response(critique_prompt, task_id)
            # print(critique)

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
        # print(model_response)

    return model_response


if __name__ == "__main__":
    iterations = 2  # Set the number of iterative improvements
    # Read tasks from a file
    with open(config.prompt_dataset_file, 'r') as f:
        tasks = f.readlines()

    count = 1
    # Process each task
    for task in tasks:
        if count <= 82:
            count += 1
            continue
        task_id = f"{config.prompt_id_prefix}{count}"
        task_prompt = f"Generate secure Python code for the following: {task}"
        final_answer = rci_task_iterative(task_prompt, task_id, iterations)
        response.write_code_to_file(task_id, final_answer)
        count += 1
