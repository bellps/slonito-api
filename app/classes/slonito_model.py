from transformers import AutoTokenizer
from local_gemma import LocalGemma2ForCausalLM
import os
import torch

from .prompt_formatter import PromptFormatter
from ..types.prompt_request import PromptRequest


class SlonitoModel():
    def __init__(self) -> None:
        torch.cuda.empty_cache()

        self.model = LocalGemma2ForCausalLM.from_pretrained(os.getenv("HF_MODEL"), preset="memory", device="cuda")
        self.tokenizer = AutoTokenizer.from_pretrained(os.getenv("HF_TOKENIZER"))


    def generate_response(self, request: PromptRequest) -> str:
        prompt = [
            {"role": "user", "content": PromptFormatter(request).format()},
        ]

        model_inputs = self.tokenizer.apply_chat_template(prompt, add_generation_prompt=True, return_tensors="pt", return_dict=True).to("cuda")
        generated_ids = self.model.generate(**model_inputs, max_new_tokens=1024, do_sample=True)
        decoded_text = self.tokenizer.batch_decode(generated_ids, clean_up_tokenization_spaces=True)

        torch.cuda.empty_cache()

        return decoded_text[0]
