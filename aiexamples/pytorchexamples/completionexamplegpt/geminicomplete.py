# --- Imports and Setup ---
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import ReduceLROnPlateau
from torch.utils.data import Dataset, DataLoader
from nltk.tokenize import word_tokenize
import random
import nltk
import os
import math
import numpy as np

# --- Configuration ---
FILE_PATH = 'sentences.txt'
MODEL_PATH = 'gpt_decoder_model_v2.pth'
BEST_MODEL_PATH = 'gpt_decoder_model_best_v2.pth'
SEQ_LEN = 32
BATCH_SIZE = 64
EMBED_SIZE = 64
NUM_HEADS = 4
NUM_LAYERS = 2
FF_DIM = 256
DROPOUT = 0.15
EPOCHS = 500
LEARNING_RATE = 3e-4
WEIGHT_DECAY = 0.01
MIN_FREQ = 2
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
EARLY_STOPPING_PATIENCE = 3

# Ensure necessary nltk packages are downloaded
try:
    nltk.data.find('tokenizers/punkt')
except nltk.downloader.DownloadError:
    nltk.download('punkt')

# --- Load Text Data ---
def load_text_data(file_path, seq_len, vocab, pad_token, unk_token, bos_token, eos_token):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None

    # Tokenize the text
    try:
        tokens = word_tokenize(text.lower())
    except Exception as e:
        print(f"Error during tokenization: {e}")
        return None

    # Convert tokens to indices using the vocabulary
    token_indices = [vocab.get(token, vocab[unk_token]) for token in tokens]

    # Add BOS and EOS tokens to the sequence
    token_indices = [vocab[bos_token]] + token_indices + [vocab[eos_token]]

    # Split the sequence into chunks of length SEQ_LEN + 1
    chunks = []
    for i in range(0, len(token_indices) - seq_len, seq_len):
        chunk = token_indices[i:i + seq_len + 1]
        chunks.append(chunk)

    print(f"Loaded {len(chunks)} chunks from the text.")
    return chunks

# --- Vocabulary Handling ---
def build_vocab(text, min_freq=2):
    word_counts = {}
    tokens = word_tokenize(text.lower())
    for word in tokens:
        word_counts[word] = word_counts.get(word, 0) + 1

    PAD_TOKEN = '<PAD>'
    UNK_TOKEN = '<UNK>'
    BOS_TOKEN = '<BOS>'
    EOS_TOKEN = '<EOS>'

    vocab = {PAD_TOKEN: 0, UNK_TOKEN: 1, BOS_TOKEN: 2, EOS_TOKEN: 3}
    index = 4
    for word, count in word_counts.items():
        if count >= min_freq:
            vocab[word] = index
            index += 1

    print(f"Vocabulary size: {len(vocab)}")
    return vocab, PAD_TOKEN, UNK_TOKEN, BOS_TOKEN, EOS_TOKEN

# --- Dataset Class ---
class SentenceDataset(Dataset):
    def __init__(self, chunks, seq_len, pad_idx):
        self.chunks = chunks
        self.seq_len = seq_len
        self.pad_idx = pad_idx

    def __len__(self):
        return len(self.chunks)

    def __getitem__(self, idx):
        chunk = self.chunks[idx]

        # Split the chunk into input and target sequences
        input_indices = chunk[:-1]
        target_indices = chunk[1:]

        # Ensure the lengths match the sequence length
        assert len(input_indices) == self.seq_len, f"Input length mismatch: {len(input_indices)} vs {self.seq_len}"
        assert len(target_indices) == self.seq_len, f"Target length mismatch: {len(target_indices)} vs {self.seq_len}"

        return torch.tensor(input_indices), torch.tensor(target_indices)

# --- GPTDecoderModel ---
class GPTDecoderModel(nn.Module):
    def __init__(self, vocab_size, embed_size, num_heads, num_layers, ff_dim, seq_len, dropout=0.1, pad_idx=0):
        super(GPTDecoderModel, self).__init__()
        self.seq_len = seq_len
        self.embed_size = embed_size
        self.embedding = nn.Embedding(vocab_size, embed_size)
        self.pos_encoder = PositionalEncoding(embed_size, dropout, max_len=seq_len + 10)
        decoder_layer = nn.TransformerDecoderLayer(
            d_model=embed_size,
            nhead=num_heads,
            dim_feedforward=ff_dim,
            dropout=dropout,
            batch_first=True
        )
        self.transformer_decoder = nn.TransformerDecoder(
            decoder_layer,
            num_layers=num_layers
        )
        self.fc = nn.Linear(embed_size, vocab_size)
        self.pad_idx = pad_idx

    def _generate_square_subsequent_mask(self, sz, device):
        mask = (torch.triu(torch.ones(sz, sz, device=device)) == 1).transpose(0, 1)
        mask = mask.float().masked_fill(mask == 0, float('-inf')).masked_fill(mask == 1, float(0.0))
        return mask

    def _create_padding_mask(self, sequence, device):
        return (sequence == self.pad_idx).to(device)

    def forward(self, src):
        device = src.device
        src_mask = self._generate_square_subsequent_mask(src.size(1), device)
        src_padding_mask = self._create_padding_mask(src, device)
        src_embedded = self.embedding(src) * math.sqrt(self.embed_size)
        src_embedded = self.pos_encoder(src_embedded)
        output = self.transformer_decoder(
            tgt=src_embedded,
            memory=src_embedded,
            tgt_mask=src_mask,
            memory_mask=None,
            tgt_key_padding_mask=src_padding_mask,
            memory_key_padding_mask=src_padding_mask
        )
        out = self.fc(output)
        return out

class PositionalEncoding(nn.Module):
    def __init__(self, d_model, dropout=0.1, max_len=5000):
        super(PositionalEncoding, self).__init__()
        self.dropout = nn.Dropout(p=dropout)
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0)
        self.register_buffer('pe', pe)

    def forward(self, x):
        x = x + self.pe[:, :x.size(1)]
        return self.dropout(x)

# --- Predict Function ---
def predict(input_text, model, vocab, seq_len, max_words, temperature, top_k, device, pad_token, unk_token, bos_token, eos_token):
    model.eval()
    reverse_vocab = {v: k for k, v in vocab.items()}
    pad_idx = vocab[pad_token]
    unk_idx = vocab[unk_token]
    bos_idx = vocab[bos_token]
    eos_idx = vocab[eos_token]

    try:
        input_tokens = [bos_token] + word_tokenize(input_text.lower())
    except Exception as e:
        print(f"Warning: Tokenization error during prediction for '{input_text}': {e}")
        return "[Tokenization Error]"

    input_indices = [vocab.get(token, unk_idx) for token in input_tokens]
    generated_indices = input_indices[:]
    generated_text = ""

    with torch.no_grad():
        for _ in range(max_words):
            current_input_indices = generated_indices[-seq_len:]
            if len(current_input_indices) < seq_len:
                current_input_indices = [pad_idx] * (seq_len - len(current_input_indices)) + current_input_indices
            else:
                current_input_indices = current_input_indices[:seq_len]

            src_tensor = torch.tensor([current_input_indices], dtype=torch.long).to(device)
            output_logits = model(src_tensor)
            next_token_logits = output_logits[0, -1, :]

            if temperature > 0:
                next_token_logits = next_token_logits / temperature
            else:
                predicted_index = torch.argmax(next_token_logits).item()

            if temperature > 0:
                probabilities = torch.softmax(next_token_logits, dim=-1)
                top_k_probs, top_k_indices = torch.topk(probabilities, k=min(top_k, probabilities.size(-1)))
                top_k_probs_np = top_k_probs.cpu().numpy()
                top_k_indices_np = top_k_indices.cpu().numpy()
                prob_sum = top_k_probs_np.sum()
                if prob_sum > 1e-6:
                    normalized_probs = top_k_probs_np / prob_sum
                else:
                    normalized_probs = np.ones_like(top_k_probs_np) / len(top_k_probs_np)
                if len(top_k_indices_np) > 0 and len(normalized_probs) > 0:
                    predicted_index = np.random.choice(top_k_indices_np, p=normalized_probs)
                else:
                    predicted_index = torch.argmax(next_token_logits).item()

            if predicted_index == eos_idx or predicted_index == pad_idx:
                break

            generated_indices.append(predicted_index)
            predicted_word = reverse_vocab.get(predicted_index, unk_token)
            generated_text += " " + predicted_word

    return input_text + generated_text

# --- Train Model Function ---
def train_model(model, train_loader, eval_loader, epochs, learning_rate, weight_decay, vocab_size, pad_idx, device, model_path, best_model_path, patience):
    optimizer = optim.Adam(model.parameters(), lr=learning_rate, weight_decay=weight_decay)
    criterion = nn.CrossEntropyLoss(ignore_index=pad_idx)
    scheduler = ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=patience // 2, verbose=True)

    print(f"Starting training on {device} for up to {epochs} epochs...")
    print(f"Early stopping patience: {patience} epochs.")
    print(f"Saving best model to: {best_model_path}")

    best_val_loss = float('inf')
    epochs_no_improve = 0

    for epoch in range(epochs):
        model.train()
        total_train_loss = 0
        for i, (src, tgt) in enumerate(train_loader):
            src, tgt = src.to(device), tgt.to(device)
            optimizer.zero_grad()
            output = model(src)
            output_flat = output.view(-1, vocab_size)
            tgt_flat = tgt.view(-1)
            loss = criterion(output_flat, tgt_flat)
            loss.backward()
            optimizer.step()
            total_train_loss += loss.item()
            if (i + 1) % 100 == 0:
                print(f"  Epoch {epoch+1}, Batch {i+1}/{len(train_loader)}, Current Loss: {loss.item():.4f}")

        avg_train_loss = total_train_loss / len(train_loader)

        model.eval()
        total_val_loss = 0
        with torch.no_grad():
            for src, tgt in eval_loader:
                src, tgt = src.to(device), tgt.to(device)
                output = model(src)
                output_flat = output.view(-1, vocab_size)
                tgt_flat = tgt.view(-1)
                loss = criterion(output_flat, tgt_flat)
                total_val_loss += loss.item()

        avg_val_loss = total_val_loss / len(eval_loader)
        print(f'Epoch [{epoch+1}/{epochs}] finished.')
        print(f'--> Avg Train Loss: {avg_train_loss:.4f}')
        print(f'--> Avg Val Loss:   {avg_val_loss:.4f}')

        scheduler.step(avg_val_loss)

        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            epochs_no_improve = 0
            try:
                #torch.save(model.state_dict(), best_model_path)
                #print(f"Validation loss improved. Saved best model to {best_model_path}")
                print(f"Validation loss improved. Best model not saved ")
            except Exception as e:
                print(f"Error saving best model: {e}")
        else:
            epochs_no_improve += 1
            print(f"Validation loss did not improve for {epochs_no_improve} epoch(s).")

        if epochs_no_improve >= patience:
            print(f"Early stopping triggered after {epoch+1} epochs.")
            break

    try:
        torch.save(model.state_dict(), model_path)
        print(f"Final model state saved to {model_path}")
    except Exception as e:
        print(f"Error saving final model: {e}")

    print(f"Loading best model from {best_model_path} for prediction.")
    try:
        model.load_state_dict(torch.load(best_model_path, map_location=DEVICE))
    except Exception as e:
        print(f"Error loading best model weights: {e}. Using final model state.")

# --- Main Script ---
if __name__ == "__main__":
    print("Loading text data...")
    try:
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: File not found at {FILE_PATH}")
        exit()

    print("Building vocabulary...")
    vocab, PAD_TOKEN, UNK_TOKEN, BOS_TOKEN, EOS_TOKEN = build_vocab(text, MIN_FREQ)
    pad_idx = vocab[PAD_TOKEN]
    vocab_size = len(vocab)

    print("Processing text into chunks...")
    chunks = load_text_data(FILE_PATH, SEQ_LEN, vocab, PAD_TOKEN, UNK_TOKEN, BOS_TOKEN, EOS_TOKEN)
    if chunks is None or not chunks:
        print("Failed to load data or file is empty. Exiting.")
        exit()

    print("Creating dataset...")
    dataset = SentenceDataset(chunks, SEQ_LEN, pad_idx)

    val_fraction = 0.1
    val_size = int(val_fraction * len(dataset))
    train_size = len(dataset) - val_size
    print(f"Splitting data: Train={train_size}, Validation={val_size}")
    if train_size <= 0 or val_size <= 0:
        print("Error: Dataset too small for splitting with current validation fraction.")
        exit()
    train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])

    print("Creating data loaders...")
    num_workers = 2 if os.name == 'posix' else 0
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=num_workers)
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=num_workers)

    print(f"Using device: {DEVICE}")
    print("Initializing GPT model...")
    model = GPTDecoderModel(
        vocab_size=vocab_size,
        embed_size=EMBED_SIZE,
        num_heads=NUM_HEADS,
        num_layers=NUM_LAYERS,
        ff_dim=FF_DIM,
        seq_len=SEQ_LEN,
        dropout=DROPOUT,
        pad_idx=pad_idx
    ).to(DEVICE)

    print("Starting model training...")
    train_model(model, train_loader, val_loader, EPOCHS, LEARNING_RATE, WEIGHT_DECAY,
                vocab_size, pad_idx, DEVICE, MODEL_PATH, BEST_MODEL_PATH, EARLY_STOPPING_PATIENCE)

    print("\nEnter a sentence start (e.g., 'Sam picks') or type 'exit' to quit.")
    while True:
        input_text = input("> ")
        if input_text.lower() == 'exit':
            break
        if not input_text.strip():
            continue

        predicted_output = predict(
            input_text=input_text,
            model=model,
            vocab=vocab,
            seq_len=SEQ_LEN,
            max_words=25,
            temperature=0.75,
            top_k=40,
            device=DEVICE,
            pad_token=PAD_TOKEN, unk_token=UNK_TOKEN, bos_token=BOS_TOKEN, eos_token=EOS_TOKEN
        )
        print(f"Completed: {predicted_output}")