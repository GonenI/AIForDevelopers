import os
import random
import re

# Load and clean sentences
def load_and_clean_sentences(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Remove empty lines and strip whitespace
    cleaned_lines = [line.strip() for line in lines if line.strip()]
    
    # Remove all punctuation
    cleaned_lines = [re.sub(r'[^\w\s]', '', line) for line in cleaned_lines]
    
    return cleaned_lines

# Generate sentence pairs
def create_sentence_pairs(sentences):
    pairs = []
    
    for sentence in sentences:
        words = sentence.split()  # Split the sentence into words
        if len(words) > 5:  # Ensure minimum sentence length
            split_idx = random.randint(2, len(words) - 3)  # Random split point
            input_text = ' '.join(words[:split_idx]).strip()
            output_text = ' '.join(words[split_idx:]).strip()
            pairs.append((input_text, output_text))
    
    return pairs

# Main processing function
def process_sentences(input_file, output_file):
    # Load and clean sentences
    sentences = load_and_clean_sentences(input_file)
    
    # Generate sentence pairs
    pairs = create_sentence_pairs(sentences)
    
    # Shuffle the pairs for randomness
    random.shuffle(pairs)
    
    # Save the sentence pairs to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        for inp, out in pairs:
            if inp.strip() and out.strip():  # Ensure no empty lines in the output
                f.write(f"{inp}\t{out}\n")
    
    print(f"Processed {len(pairs)} sentence pairs saved to {output_file}")

# File paths
input_file = "sentences.txt"
output_file = "sentence_pairs.txt"

# Run the processing
process_sentences(input_file, output_file)