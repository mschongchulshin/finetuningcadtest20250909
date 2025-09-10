# ���� ������ generator.py
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import re
import json

class CADGenerator:
    def __init__(self, model_repo_id=None):
        """
        Hugging Face Hub���� �𵨰� ��ũ�������� �ʱ�ȭ�ϰ� �ε��մϴ�.
        """
        if model_repo_id is None:
            # ? ����ڴ��� ��Ȯ�� �������丮 �ּҷ� �����߽��ϴ�.
            model_repo_id = "HongchulShin/finetuning-cad-model" 

        print("Initializing CAD Generator...")
        print(f"Loading model from Hugging Face Hub: {model_repo_id}")
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_repo_id)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_repo_id,
            torch_dtype=torch.bfloat16,
            device_map="auto"
        )
        print("Model loaded successfully.")

    def _format_prompt(self, instruction):
        """�߷��� ���� ������Ʈ ������ ����ϴ�."""
        system_message = (
            "����� ����� �κ� �۾������� ���� ���� �������Դϴ�. "
            "����ڰ� �����ϴ� �ڿ��� ������ �������� ��Ȯ�� JSON ������ ���� �����͸� �������ּ���."
        )
        prompt = (
            f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
            f"{system_message}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n"
            f"{instruction}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
        )
        return prompt

    def generate(self, prompt, max_new_tokens=2048):
        """
        ����ڷκ��� ������Ʈ�� �޾� JSON�� �����ϰ� ��ȯ�մϴ�.
        """
        formatted_prompt = self._format_prompt(prompt)
        inputs = self.tokenizer(formatted_prompt, return_tensors="pt").to(self.model.device)
        self.model.eval()
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=0.1,
                do_sample=True,
                top_p=0.9,
                pad_token_id=self.tokenizer.eos_token_id,
            )
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        assistant_start = response.find("<|start_header_id|>assistant<|end_header_id|>")
        if assistant_start != -1:
            json_part = response[assistant_start + len("<|start_header_id|>assistant<|end_header_id|>"):].strip()
            json_match = re.search(r'\{.*\}', json_part, re.DOTALL)
            if json_match:
                try:
                    parsed_json = json.loads(json_match.group(0))
                    return json.dumps(parsed_json, indent=2, ensure_ascii=False)
                except json.JSONDecodeError:
                    return json_match.group(0)
        return '{"error": "Failed to generate valid JSON."}'