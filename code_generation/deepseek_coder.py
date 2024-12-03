from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os
from time import sleep
from config import config
import re

os.environ["TOKENIZERS_PARALLELISM"] = "false"


class DeepseekCodeGenerator:
    def __init__(self, model_name="deepseek-ai/deepseek-coder-6.7b-base") -> None:
        self.model_name = model_name
        # Initialize tokenizer and model
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name, trust_remote_code=True)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16,
                device_map="auto",
                trust_remote_code=True
            )
        except Exception as e:
            print(f"Error initializing model: {e}")
            raise

    def generate_response(self, task_prompt, task_prompt_id):
        success = False
        while not success:
            try:
                # Prepare the input
                messages = [
                    {"role": "user", "content": task_prompt}
                ]
                input_text = self.tokenizer.apply_chat_template(
                    messages,
                    tokenize=False,
                    add_generation_prompt=True
                )

                # Tokenize input
                inputs = self.tokenizer(
                    input_text, return_tensors="pt").to(self.model.device)

                # Generate response
                outputs = self.model.generate(
                    inputs["input_ids"],
                    max_new_tokens=2048,
                    temperature=0.0,
                    top_p=0.1,
                    pad_token_id=self.tokenizer.eos_token_id,
                )

                # Decode response
                response = self.tokenizer.decode(
                    outputs[0], skip_special_tokens=True)
                # Remove the input prompt from response
                response = response[len(input_text):].strip()

                success = True
                return response

            except torch.cuda.OutOfMemoryError:
                print(f"GPU OOM for prompt {
                      task_prompt_id}... Clearing cache...")
                torch.cuda.empty_cache()
                sleep(5)
            except Exception as e:
                print(f"Error for prompt {task_prompt_id}: {e}... Waiting...")
                sleep(65)
                print("...continue")

        return None

    def wrap_request(self, type, msg):
        return {"role": type, "content": msg}

    def write_code_to_file(self, prompt_task_id, code):
        """ Writes a given code snippet and its associated prompt to a Python file. """
        print(f"Writing code for {prompt_task_id} to file")
        output_dir = config.code_output_dir
        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Extract code blocks
        code_blocks = []
        code_blocks = re.findall(r'```python(.*?)```', code, re.DOTALL)
        # If no code blocks found, use the entire response
        if all(not block.strip() for block in code_blocks):
            code_blocks.append(code)

        filename = f"{prompt_task_id}"
        filepath = os.path.join(output_dir, f"{filename}.py")
        print(filepath)

        try:
            with open(filepath, "w+", encoding='utf-8') as f:
                for block in code_blocks:
                    f.write(block.strip() + '\n\n')
            return filepath
        except Exception as e:
            print(f"Failed to write to file: {e}")
