import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from nltk.tokenize import word_tokenize
import random
import nltk
import os

# Ensure necessary nltk packages are downloaded
nltk.download('punkt')

# Load pairs from sentence_pairs.txt
def load_pairs(file_path):
    pairs = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            input_text, output_text = line.strip().split('\t')
            pairs.append((input_text, output_text))
    return pairs

# Vocabulary Handling
def build_vocab(pairs, min_freq=2):
    word_counts = {}
    for input_text, output_text in pairs:
        for word in word_tokenize(input_text) + word_tokenize(output_text):
            word_counts[word] = word_counts.get(word, 0) + 1

    vocab = {'<PAD>': 0, '<UNK>': 1, '<BOS>': 2, '<EOS>': 3, '<SEP>': 4}
    index = 5
    for word, count in word_counts.items():
        if count >= min_freq:  # Only include words that appear at least `min_freq` times
            vocab[word] = index
            index += 1
    return vocab

# Dataset class
class SentenceDataset(Dataset):
    def __init__(self, pairs, vocab, seq_len=10):
        self.pairs = pairs
        self.vocab = vocab
        self.seq_len = seq_len

    def __len__(self):
        return len(self.pairs)

    def __getitem__(self, idx):
        input_text, output_text = self.pairs[idx]
        combined_text = f"<BOS> {input_text} <SEP> {output_text} <EOS>"
        tokens = word_tokenize(combined_text)

        # Convert tokens to their respective indices
        token_indices = [self.vocab.get(token, self.vocab['<UNK>']) for token in tokens]

        # Padding or truncating to uniform length
        token_indices = token_indices[:self.seq_len]  # Truncate if longer than seq_len
        token_indices += [self.vocab['<PAD>']] * (self.seq_len - len(token_indices))  # Pad if shorter

        # Input and target are the same for GPT (causal language modeling)
        input_indices = token_indices[:-1]  # All tokens except the last
        target_indices = token_indices[1:]  # All tokens except the first

        return torch.tensor(input_indices), torch.tensor(target_indices)

# GPT Model
class GPTModel(nn.Module):
    def __init__(self, vocab_size, embed_size=128, num_heads=8, num_layers=4, seq_len=10, dropout=0.1):
        super(GPTModel, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_size)
        self.positional_encoding = nn.Parameter(torch.zeros(1, seq_len, embed_size))
        self.transformer = nn.Transformer(
            d_model=embed_size,
            nhead=num_heads,
            num_encoder_layers=num_layers,
            num_decoder_layers=num_layers,
            dim_feedforward=512,
            dropout=dropout,
        )
        self.fc = nn.Linear(embed_size, vocab_size)

    def forward(self, src, tgt):
        # Get the actual sequence lengths
        src_len = src.size(1)
        tgt_len = tgt.size(1)

        # Dynamically slice positional encoding to match the sequence lengths
        src_positional_encoding = self.positional_encoding[:, :src_len, :]
        tgt_positional_encoding = self.positional_encoding[:, :tgt_len, :]

        # Add positional encoding to embeddings
        src_embedded = self.embedding(src) + src_positional_encoding
        tgt_embedded = self.embedding(tgt) + tgt_positional_encoding

        # Pass through the transformer
        transformer_out = self.transformer(src_embedded.permute(1, 0, 2), tgt_embedded.permute(1, 0, 2))

        # Final linear layer
        out = self.fc(transformer_out.permute(1, 0, 2))
        return out

# Prediction function with top-k sampling
def predict(input_text, model, vocab, seq_len=10, max_words=5, temperature=1.0, top_k=5):
    reverse_vocab = {v: k for k, v in vocab.items()}
    input_tokens = ['<BOS>'] + word_tokenize(input_text) + ['<SEP>']
    input_indices = [vocab.get(token, vocab['<UNK>']) for token in input_tokens]

    # Ensure the input sequence length matches seq_len
    if len(input_indices) > seq_len:
        input_indices = input_indices[-seq_len:]  # Truncate to the last `seq_len` tokens
    else:
        input_indices = [vocab['<PAD>']] * (seq_len - len(input_indices)) + input_indices  # Pad to `seq_len`

    predicted_output = input_text
    tgt_indices = input_indices

    for _ in range(max_words):
        src_tensor = torch.tensor([tgt_indices]).to(next(model.parameters()).device)

        with torch.no_grad():
            model.eval()
            output = model(src_tensor, src_tensor)

        logits = output[0, -1] / temperature
        probabilities = torch.softmax(logits, dim=-1)

        # Top-k sampling
        top_k_probs, top_k_indices = torch.topk(probabilities, k=top_k)
        top_k_probs = top_k_probs.cpu().numpy()
        top_k_indices = top_k_indices.cpu().numpy()
        predicted_index = random.choices(top_k_indices, weights=top_k_probs, k=1)[0]

        predicted_word = reverse_vocab.get(predicted_index, "<UNK>")
        if predicted_word == '<EOS>' or predicted_word == '<PAD>':
            break
        predicted_output += " " + predicted_word
        tgt_indices.append(predicted_index)

        # Ensure tgt_indices does not exceed seq_len
        if len(tgt_indices) > seq_len:
            tgt_indices = tgt_indices[-seq_len:]

    return predicted_output

# Training loop with validation loss monitoring
def train_model(model, data_loader, epochs=10, eval_loader=None):
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.CrossEntropyLoss(ignore_index=vocab['<PAD>'])

    for epoch in range(epochs):
        model.train()
        total_loss = 0
        for src, tgt in data_loader:
            src, tgt = src.to(next(model.parameters()).device), tgt.to(next(model.parameters()).device)

            optimizer.zero_grad()
            output = model(src, src)  # GPT uses the same input for src and tgt
            output = output.reshape(-1, len(vocab))
            tgt = tgt.reshape(-1)
            loss = criterion(output, tgt)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        avg_loss = total_loss / len(data_loader)
        print(f'Epoch [{epoch+1}/{epochs}], Loss: {avg_loss:.4f}')

        # Validation step
        if eval_loader:
            model.eval()
            val_loss = 0
            with torch.no_grad():
                for src, tgt in eval_loader:
                    src, tgt = src.to(next(model.parameters()).device), tgt.to(next(model.parameters()).device)
                    output = model(src, src)
                    output = output.reshape(-1, len(vocab))
                    tgt = tgt.reshape(-1)
                    val_loss += criterion(output, tgt).item()
            avg_val_loss = val_loss / len(eval_loader)
            print(f"Validation Loss after Epoch {epoch+1}: {avg_val_loss:.4f}")

# Main script
pairs = load_pairs('sentence_pairs.txt')
vocab = build_vocab(pairs)
seq_len = 10
dataset = SentenceDataset(pairs, vocab, seq_len)

# Split dataset into training and validation
val_size = int(0.2 * len(dataset))
train_size = len(dataset) - val_size
train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=64)

# Initialize GPT model
model = GPTModel(vocab_size=len(vocab), seq_len=seq_len).to('cuda' if torch.cuda.is_available() else 'cpu')

# Check for saved model
model_path = 'gpt_model.pth'
if os.path.exists(model_path):
    print("Loading saved model...")
    model.load_state_dict(torch.load(model_path))
    print("Model loaded successfully.")
else:
    print("No saved model found. Training a new model...")
    train_model(model, train_loader, epochs=10, eval_loader=val_loader)
    torch.save(model.state_dict(), model_path)
    print("Model training complete and saved.")

# Interactive prediction loop
while True:
    input_text = input("Enter a sentence (or type 'exit' to quit): ")
    if input_text.lower() == 'exit':
        break
    predicted_output = predict(input_text, model, vocab, seq_len=10, max_words=5, temperature=1.0, top_k=5)
    print(f"Predicted Output: {predicted_output}")
