import re
import nltk
import random
import os
from nltk.tokenize import sent_tokenize

nltk.download('punkt')  # Ensure sentence tokenizer is available

# Load and clean text
def load_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Remove Gutenberg headers/footers and unwanted characters
    text = re.sub(r'\*\*\* START.*?\*\*\*', '', text, flags=re.DOTALL)
    text = re.sub(r'\*\*\* END.*?\*\*\*', '', text, flags=re.DOTALL)
    text = re.sub(r'[^a-zA-Z0-9.,!?;:\'"\s]', '', text)  # Keep only alphanumeric and punctuation
    text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
    # Remove chapter headings
    text = re.sub(r'CHAPTER [IVXLCDM]+', '', text)

    return text.strip()

# Generate sentence pairs
def create_sentence_pairs(text):
    sentences = sent_tokenize(text)
    pairs = []
    
    for sentence in sentences:
        words = sentence.split()
        if len(words) > 5:  # Ensure minimum sentence length
            split_idx = random.randint(2, len(words) - 3)  # Random split point
            input_text = ' '.join(words[:split_idx]).strip()
            output_text = ' '.join(words[split_idx:]).strip()
            pairs.append((input_text, output_text))
    
    return pairs

# Process all .txt files in the current directory
text_files = [file for file in os.listdir('.') if file.endswith('.txt')]

# Create dataset
pairs = []
for file in text_files:
    book_text = load_text(file)
    pairs.extend(create_sentence_pairs(book_text))

random.shuffle(pairs)

# Save processed data
with open("sentence_pairs.txt", "w", encoding="utf-8") as f:
    for inp, out in pairs:
        f.write(f"{inp}\t{out}\n")

print(f"Processed {len(pairs)} sentence pairs from {len(text_files)} files saved to sentence_pairs.txt")
