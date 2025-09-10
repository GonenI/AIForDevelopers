from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load a pretrained GPT-2 model and tokenizer
model = GPT2LMHeadModel.from_pretrained("gpt2")  # Downloads weights if not already cached
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Set the padding token to the EOS token (since GPT-2 does not have a padding token by default)
tokenizer.pad_token = tokenizer.eos_token

# Encode text input
while True:
    input_text = input("Enter a prompt (or type 'exit' to quit): ")
    if input_text.lower() == 'exit':
        break
    input_ids = tokenizer.encode(input_text, return_tensors="pt", padding=True)  # Convert to tensor with padding
    attention_mask = input_ids.ne(tokenizer.pad_token_id).long()  # Create attention mask
    # Generate text
    output = model.generate(input_ids, attention_mask=attention_mask, max_length=40, pad_token_id=tokenizer.eos_token_id)
    # Decode output
    print(tokenizer.decode(output[0], skip_special_tokens=True))
