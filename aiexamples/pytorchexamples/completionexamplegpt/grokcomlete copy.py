import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from nltk.tokenize import word_tokenize
import random
import nltk
import os

nltk.download('punkt')

def load_pairs(file_path):
    pairs = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                input_text, output_text = line.strip().split('\t')
                pairs.append((input_text, output_text))
            except ValueError:
                print(f"Skipping malformed line: {line.strip()}")
    return pairs

def build_vocab(pairs, min_freq=1):
    word_counts = {}
    for input_text, output_text in pairs:
        for word in word_tokenize(input_text) + word_tokenize(output_text):
            word_counts[word] = word_counts.get(word, 0) + 1
    vocab = {'<PAD>': 0, '<UNK>': 1, '<BOS>': 2, '<EOS>': 3, '<SEP>': 4}
    index = 5
    for word, count in word_counts.items():
        if count >= min_freq:
            vocab[word] = index
            index += 1
    print(f"Vocabulary size: {len(vocab)}")
    print(f"Sample vocab: {dict(list(vocab.items())[:10])}")
    return vocab

class SentenceDataset(Dataset):
    def __init__(self, pairs, vocab, seq_len=20):
        self.pairs = pairs
        self.vocab = vocab
        self.seq_len = seq_len
        self.unk_count = 0
        self.total_tokens = 0

    def __len__(self):
        return len(self.pairs)

    def __getitem__(self, idx):
        input_text, output_text = self.pairs[idx]
        combined_text = f"<BOS> {input_text} <SEP> {output_text} <EOS>"
        tokens = word_tokenize(combined_text)
        token_indices = [self.vocab.get(token, self.vocab['<UNK>']) for token in tokens]
        self.unk_count += token_indices.count(1)
        self.total_tokens += len(token_indices)
        token_indices = token_indices[:self.seq_len]
        token_indices += [self.vocab['<PAD>']] * (self.seq_len - len(token_indices))
        input_indices = token_indices[:-1]
        target_indices = token_indices[1:]
        return torch.tensor(input_indices), torch.tensor(target_indices)

    def print_unk_stats(self):
        if self.total_tokens == 0:
            print("No tokens processed.")
            return
        print(f"<UNK> frequency: {self.unk_count}/{self.total_tokens} ({self.unk_count/self.total_tokens*100:.2f}%)")

class GPTModel(nn.Module):
    def __init__(self, vocab_size, embed_size=256, num_heads=8, num_layers=6, seq_len=20, dropout=0.1):
        super(GPTModel, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_size)
        self.positional_encoding = nn.Parameter(torch.zeros(1, seq_len, embed_size))
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=embed_size,
            nhead=num_heads,
            dim_feedforward=1024,
            dropout=dropout,
            batch_first=False
        )
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.fc = nn.Linear(embed_size, vocab_size)
        self.seq_len = seq_len

    def forward(self, src):
        src_len = src.size(1)
        src_embedded = self.embedding(src) + self.positional_encoding[:, :src_len, :]
        src_embedded = src_embedded.permute(1, 0, 2)
        src_mask = self.generate_square_subsequent_mask(src_len).to(src.device)
        transformer_out = self.transformer_encoder(src_embedded, mask=src_mask)
        out = self.fc(transformer_out.permute(1, 0, 2))
        return out

    def generate_square_subsequent_mask(self, sz):
        mask = (torch.triu(torch.ones(sz, sz)) == 1).transpose(0, 1)
        mask = mask.float().masked_fill(mask == 0, float('-inf')).masked_fill(mask == 1, float(0.0))
        return mask

def predict(input_text, model, vocab, seq_len=20, max_words=5, temperature=0.9, top_k=15):  # Adjusted for diversity
    reverse_vocab = {v: k for k, v in vocab.items()}
    input_tokens = ['<BOS>'] + word_tokenize(input_text) + ['<SEP>']
    input_indices = [vocab.get(token, vocab['<UNK>']) for token in input_tokens]
    if len(input_indices) > seq_len:
        input_indices = input_indices[-seq_len:]
    else:
        input_indices = [vocab['<PAD>']] * (seq_len - len(input_indices)) + input_indices
    predicted_output = input_text
    tgt_indices = input_indices.copy()
    recent_indices = set()
    model.eval()
    with torch.no_grad():
        for i in range(max_words):
            tgt_tensor = torch.tensor([tgt_indices]).to(next(model.parameters()).device)
            output = model(tgt_tensor)
            logits = output[0, -1] / temperature
            for idx in recent_indices:
                logits[idx] -= 2.0  # Repetition penalty
            probabilities = torch.softmax(logits, dim=-1)
            top_k_probs, top_k_indices = torch.topk(probabilities, k=top_k + 1)
            top_k_probs = top_k_probs.cpu().numpy()
            top_k_indices = top_k_indices.cpu().numpy()
            print(f"Step {i+1} - Top {top_k+1} indices: {top_k_indices.tolist()}")
            print(f"Step {i+1} - Top {top_k+1} probs: {top_k_probs.tolist()}")
            valid_mask = top_k_indices != 1
            valid_indices = top_k_indices[valid_mask]
            valid_probs = top_k_probs[valid_mask]
            if len(valid_indices) == 0:
                valid_indices = [vocab['<EOS>']]
                valid_probs = [1.0]
            predicted_index = random.choices(valid_indices, weights=valid_probs, k=1)[0]
            print(f"Step {i+1} - Predicted index: {predicted_index}")
            predicted_word = reverse_vocab.get(predicted_index, "<UNK>")
            if predicted_word in ['<EOS>', '<PAD>']:
                break
            predicted_output += " " + predicted_word
            tgt_indices.append(predicted_index)
            recent_indices.add(predicted_index)
            if len(recent_indices) > 3:
                recent_indices = set(tgt_indices[-3:])
            if len(tgt_indices) > seq_len:
                tgt_indices = tgt_indices[-seq_len:]
    return predicted_output

def train_model(model, data_loader, epochs=50, eval_loader=None):
    optimizer = optim.Adam(model.parameters(), lr=0.0001)
    criterion = nn.CrossEntropyLoss(ignore_index=vocab['<PAD>'], label_smoothing=0.1)  # Add label smoothing
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=5)
    best_val_loss = float('inf')
    patience = 10
    counter = 0
    for epoch in range(epochs):
        model.train()
        total_loss = 0
        for src, tgt in data_loader:
            src, tgt = src.to(next(model.parameters()).device), tgt.to(next(model.parameters()).device)
            optimizer.zero_grad()
            output = model(src)
            output = output.reshape(-1, len(vocab))
            tgt = tgt.reshape(-1)
            loss = criterion(output, tgt)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        avg_loss = total_loss / len(data_loader)
        print(f'Epoch [{epoch+1}/{epochs}], Loss: {avg_loss:.4f}')
        if eval_loader:
            model.eval()
            val_loss = 0
            with torch.no_grad():
                for src, tgt in eval_loader:
                    src, tgt = src.to(next(model.parameters()).device), tgt.to(next(model.parameters()).device)
                    output = model(src)
                    output = output.reshape(-1, len(vocab))
                    tgt = tgt.reshape(-1)
                    val_loss += criterion(output, tgt).item()
            avg_val_loss = val_loss / len(eval_loader)
            print(f"Validation Loss after Epoch {epoch+1}: {avg_val_loss:.4f}")
            scheduler.step(avg_val_loss)
            if avg_val_loss < best_val_loss:
                best_val_loss = avg_val_loss
                counter = 0
                torch.save(model.state_dict(), 'best_model.pth')
            else:
                counter += 1
            if counter >= patience:
                print("Early stopping triggered.")
                break
    return best_val_loss

pairs = load_pairs('sentence_pairs.txt')
vocab = build_vocab(pairs)
seq_len = 20
dataset = SentenceDataset(pairs, vocab, seq_len)
val_size = int(0.2 * len(dataset))
train_size = len(dataset) - val_size
train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=64)
dataset.print_unk_stats()
model = GPTModel(vocab_size=len(vocab), seq_len=seq_len).to('cuda' if torch.cuda.is_available() else 'cpu')
model_path = 'gpt_model.pth'
if os.path.exists(model_path):
    print("Loading saved model...")
    model.load_state_dict(torch.load(model_path))
    print("Model loaded successfully.")
    while True:
        input_text = input("Enter a sentence (or type 'exit' to quit): ")
        if input_text.lower() == 'exit':
            break
        predicted_output = predict(input_text, model, vocab, seq_len=20, max_words=5, temperature=0.9, top_k=15)
        print(f"Predicted Output: {predicted_output}")
else:
    print("No saved model found. Training a new model...")
    train_model(model, train_loader, epochs=50, eval_loader=val_loader)
    torch.save(model.state_dict(), model_path)
    print("Model training complete and saved.")
    while True:
        input_text = input("Enter a sentence (or type 'exit' to quit): ")
        if input_text.lower() == 'exit':
            break
        predicted_output = predict(input_text, model, vocab, seq_len=20, max_words=5, temperature=0.9, top_k=15)
        print(f"Predicted Output: {predicted_output}")