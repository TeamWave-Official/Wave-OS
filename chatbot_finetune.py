from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# Load GPT-2 small (fastest and lightest)
model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# Make sure it runs on CPU
device = torch.device("cpu")
model.to(device)

# Function to generate clean text
def generate_text(prompt):
    inputs = tokenizer.encode(prompt, return_tensors="pt").to(device)

    outputs = model.generate(
        inputs,
        max_length=100,         # limit text length
        temperature=0.7,        # lower = less random
        top_p=0.9,              # nucleus sampling for quality
        repetition_penalty=1.2, # discourages repeated words
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id
    )

    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return text

# Example usage
print(generate_text("Once upon a time in India,"))
