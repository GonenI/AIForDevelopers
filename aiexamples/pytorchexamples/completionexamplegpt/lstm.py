import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from nltk.tokenize import word_tokenize
import random
import nltk
import os

# Download the NLTK tokenizer data if not already available
nltk.download('punkt')
nltk.download('punkt_tab')

# Function to load sentences from a text file
def load_sentences(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]  # Read non-empty lines

# Function to build a vocabulary from the sentences
def build_vocab(sentences, min_freq=1):
    word_counts = {}
    for sentence in sentences:
        for word in word_tokenize(sentence):  # Tokenize each sentence into words
            word_counts[word] = word_counts.get(word, 0) + 1  # Count word frequencies
    # Create a vocabulary with special tokens for padding, unknown words, start, and end
    vocab = {'<PAD>': 0, '<UNK>': 1, '<BOS>': 2, '<EOS>': 3}
    index = 4
    for word, count in word_counts.items():
        if count >= min_freq:  # Only include words that appear frequently enough
            vocab[word] = index
            index += 1
    return vocab

# Custom dataset class for handling sentences
class SentenceDataset(Dataset):
    def __init__(self, sentences, vocab, seq_len=20):
        self.sentences = sentences  # List of sentences
        self.vocab = vocab  # Vocabulary dictionary
        self.seq_len = seq_len  # Maximum sequence length

    def __len__(self):
        return len(self.sentences)  # Number of sentences in the dataset

    def __getitem__(self, idx):
        sentence = self.sentences[idx]
        # Add special tokens for start and end of the sentence
        tokens = ['<BOS>'] + word_tokenize(sentence) + ['<EOS>']
        # Convert tokens to their corresponding indices in the vocabulary
        token_indices = [self.vocab.get(token, self.vocab['<UNK>']) for token in tokens]
        # Truncate or pad the sequence to the fixed length
        token_indices = token_indices[:self.seq_len]
        token_indices += [self.vocab['<PAD>']] * (self.seq_len - len(token_indices))
        # Input is the sequence without the last token, target is the sequence without the first token
        input_indices = token_indices[:-1]
        target_indices = token_indices[1:]
        return torch.tensor(input_indices), torch.tensor(target_indices)

# LSTM-based neural network model for text generation
class LSTMModel(nn.Module):
    def __init__(self, vocab_size, embed_size=128, hidden_size=256, num_layers=2, seq_len=20):
        super(LSTMModel, self).__init__()
        # Embedding layer to convert word indices into dense vectors
        self.embedding = nn.Embedding(vocab_size, embed_size)
        # LSTM layer to process sequences
        self.lstm = nn.LSTM(embed_size, hidden_size, num_layers, batch_first=True)
        # Fully connected layer to predict the next word
        self.fc = nn.Linear(hidden_size, vocab_size)
        self.seq_len = seq_len

    def forward(self, src):
        embedded = self.embedding(src)  # Convert input indices to embeddings
        lstm_out, _ = self.lstm(embedded)  # Pass embeddings through the LSTM
        out = self.fc(lstm_out)  # Predict the next word for each position
        return out

# Function to generate predictions from the model
def predict(input_text, model, vocab, seq_len=20, max_words=5):
    reverse_vocab = {v: k for k, v in vocab.items()}  # Reverse the vocabulary for decoding
    input_tokens = ['<BOS>'] + word_tokenize(input_text)  # Add start token to input
    input_indices = [vocab.get(token, vocab['<UNK>']) for token in input_tokens]
    # Pad the input to match the sequence length
    input_indices = [vocab['<PAD>']] * (seq_len - len(input_indices)) + input_indices
    predicted_output = input_text
    model.eval()  # Set the model to evaluation mode
    with torch.no_grad():  # Disable gradient computation
        for _ in range(max_words):  # Generate up to max_words
            tgt_tensor = torch.tensor([input_indices]).to(next(model.parameters()).device)
            output = model(tgt_tensor)  # Get model predictions
            logits = output[0, -1]  # Take the last word's predictions
            probabilities = torch.softmax(logits, dim=-1)  # Convert logits to probabilities
            predicted_index = torch.multinomial(probabilities, 1).item()  # Sample a word
            predicted_word = reverse_vocab.get(predicted_index, '<UNK>')  # Decode the word
            if predicted_word in ['<EOS>', '<PAD>']:  # Stop if end token is reached
                break
            predicted_output += ' ' + predicted_word  # Append the word to the output
            input_indices.append(predicted_index)  # Update the input sequence
            input_indices = input_indices[-seq_len:]  # Keep the sequence length fixed
    return predicted_output

# Function to train the model
def train_model(model, data_loader, epochs=10):
    optimizer = optim.Adam(model.parameters(), lr=0.001)  # Optimizer for updating weights
    criterion = nn.CrossEntropyLoss(ignore_index=0)  # Loss function, ignoring padding
    for epoch in range(epochs):
        model.train()  # Set the model to training mode
        total_loss = 0
        for src, tgt in data_loader:  # Iterate over batches of data
            src, tgt = src.to(next(model.parameters()).device), tgt.to(next(model.parameters()).device)
            optimizer.zero_grad()  # Reset gradients
            output = model(src).reshape(-1, len(vocab))  # Get model predictions
            loss = criterion(output, tgt.reshape(-1))  # Compute the loss
            loss.backward()  # Backpropagate the loss
            optimizer.step()  # Update the model weights
            total_loss += loss.item()  # Accumulate the loss
        print(f'Epoch [{epoch+1}/{epochs}], Loss: {total_loss / len(data_loader):.4f}')  # Print progress

# Load sentences from a file
sentences = load_sentences('sentences.txt')
# Build the vocabulary from the sentences
vocab = build_vocab(sentences)
seq_len = 20  # Fixed sequence length
# Create a dataset and data loader for training
dataset = SentenceDataset(sentences, vocab, seq_len)
data_loader = DataLoader(dataset, batch_size=32, shuffle=True)

# Check if a GPU is available, otherwise use the CPU
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {DEVICE}")

# Initialize the LSTM model
model = LSTMModel(vocab_size=len(vocab), seq_len=seq_len).to(DEVICE)
if os.path.exists('lstm_model.pth'):  # Check if a saved model exists
    print("Loading existing model...")
    model.load_state_dict(torch.load('lstm_model.pth', map_location=DEVICE))  # Load the model
else:
    # Train the model if no saved model exists
    train_model(model, data_loader, epochs=10)
    torch.save(model.state_dict(), 'lstm_model.pth')  # Save the trained model

# Interactive loop for generating predictions
while True:
    input_text = input("Enter a sentence (or type 'exit' to quit): ")
    if input_text.lower() == 'exit':  # Exit the loop if the user types 'exit'
        break
    # Generate and print the predicted output
    print(f"Predicted Output: {predict(input_text, model, vocab, seq_len=20, max_words=5)}")
