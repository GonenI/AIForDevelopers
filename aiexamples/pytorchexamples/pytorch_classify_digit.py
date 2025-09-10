import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random

# Define the dataset
def create_dataset():
    data = []
    labels = []

    # Create images of 1
    for _ in range(33):
        image = [0, 1, 0, 0, 1, 0, 0, 1, 0]
        data.append(image)
        labels.append(0)

    # Create images of 0
    for _ in range(33):
        image = [1, 1, 1, 1, 0, 1, 1, 1, 1]
        data.append(image)
        labels.append(1)

    # Create images of X
    for _ in range(33):
        image = [1, 0, 1, 0, 1, 0, 1, 0, 1]
        data.append(image)
        labels.append(2)

    return data, labels

def flip_random_bit(image):
    index_to_flip = random.randint(0, len(image) - 1)
    image[index_to_flip] = 1 - image[index_to_flip]  # Flip the bit
    return image

# Create training dataset
train_data, train_labels = create_dataset()
train_data = [flip_random_bit(image) for image in train_data]

# Convert to tensors
train_data = torch.FloatTensor(train_data)
train_labels = torch.LongTensor(train_labels)

# Define the neural network model
class Classifier(nn.Module):
    def __init__(self):
        super(Classifier, self).__init__()
        self.fc1 = nn.Linear(9, 18)
        self.fc2 = nn.Linear(18, 9)
        self.fc3 = nn.Linear(9, 3)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

# Instantiate the model, define the loss function and the optimizer
model = Classifier()
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
num_epochs = 1000
for epoch in range(num_epochs):
    # Forward pass
    outputs = model(train_data)
    loss = criterion(outputs, train_labels)
    
    # Backward pass and optimization
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    if (epoch+1) % 100 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

# User interaction for evaluation
label_dict = {0: "1", 1: "0", 2: "X"}
while True:
    user_input = input("Enter 1, 0, or X to create the image, or 'q' to quit: ").strip()
    if user_input.lower() == 'q':
        break
    
    if user_input == '1':
        image = [0, 1, 0, 0, 1, 0, 0, 1, 0]
    elif user_input == '0':
        image = [1, 1, 1, 1, 0, 1, 1, 1, 1]
    elif user_input.lower() == 'x':
        image = [1, 0, 1, 0, 1, 0, 1, 0, 1]
    else:
        print("Invalid input. Please enter 1, 0, or X.")
        continue

    # ask user how many bits to flip
    num_bits_to_flip = input("Enter the number of bits to flip (0-9): ").strip()
    if not num_bits_to_flip.isdigit():
        print("Invalid input. Please enter a number.")
        continue
    # flip the bits the specified number of times
    for _ in range(int(num_bits_to_flip)):
     image = flip_random_bit(image)
     print("image with noise",image)
    image_tensor = torch.FloatTensor([image])
    
    with torch.no_grad():
        prediction = model(image_tensor)
        _, predicted_label = torch.max(prediction, 1)
        print(f"Predicted label for the image: {label_dict[predicted_label.item()]}")

print("Exiting program.")
