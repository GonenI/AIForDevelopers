import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt

# Generate random training data
X_train = torch.FloatTensor(np.random.randint(1, 1001, size=(100, 1)))
y_train = torch.where(X_train > 500, torch.FloatTensor([1.0]), torch.FloatTensor([0.0]))  # Fixed shape issue

# Define a simple neural network
class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.fc1 = nn.Linear(1, 10)
        self.fc2 = nn.Linear(10, 1)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.sigmoid(self.fc2(x))
        return x

# Instantiate the model
model = Model()

# Define loss function and optimizer
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.003)

# Training loop
for epoch in range(1000):
    # Forward pass
    outputs = model(X_train)
    loss = criterion(outputs, y_train)
    
    # Backward pass and optimization
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    if (epoch+1) % 100 == 0:
        print(f'Epoch [{epoch+1}/1000], Loss: {loss.item():.4f}')

# Generate random test data
X_test = torch.FloatTensor(np.random.randint(1, 1001, size=(100, 1)))

# Predict labels for test data
with torch.no_grad():
    predictions = model(X_test)
    predicted_labels = torch.where(predictions > 0.5, torch.FloatTensor([1.0]), torch.FloatTensor([0.0]))  # Fixed shape issue

print("Predicted labels for test data:")
print(predicted_labels.numpy().flatten())

# Plot the test data
plt.scatter(X_test.numpy(), predicted_labels.numpy(), c=predicted_labels.numpy().flatten(), cmap='bwr')
plt.xlabel('Input')
plt.ylabel('Predicted Class')
plt.title('Predicted Classes for Test Data')
plt.axhline(y=0.5, color='black', linestyle='--')
plt.show()
