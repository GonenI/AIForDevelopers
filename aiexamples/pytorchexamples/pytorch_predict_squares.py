import torch
import torch.nn as nn
import torch.optim as optim

# Input data: squares of numbers from 1 to 100
X_train = torch.FloatTensor([[i ** 2] for i in range(1, 101)])  # Reshape to (100, 1)
y_train = torch.FloatTensor([[i ** 2] for i in range(2, 102)])  # Next 10 numbers

# Define a simple neural network with 2 hidden layers
class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.fc1 = nn.Linear(1, 10)
        self.fc2 = nn.Linear(10, 10)
        self.fc3 = nn.Linear(10, 1)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

# Instantiate the model
model = Model()

# Define loss function and optimizer
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.0001)

# Training loop
for epoch in range(5000):
    # Forward pass
    outputs = model(X_train)
    loss = criterion(outputs, y_train)
    
    # Backward pass and optimization
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    if (epoch+1) % 500 == 0:
        print(f'Epoch [{epoch+1}/5000], Loss: {loss.item():.4f}')

# Predict the next 10 numbers
with torch.no_grad():
    next_numbers = model(torch.FloatTensor([[i ** 2] for i in range(101, 201)]))

print("Predicted next 10 numbers:")
print(next_numbers.numpy().flatten())

# plot the actual values as y coordinates and their position as x coordinates
import matplotlib.pyplot as plt
plt.plot(range(1, 101), X_train.numpy(), 'ro', label='Actual')
# plot the predicted values as y coordinates and their position as x coordinates
plt.plot(range(101, 201), next_numbers.numpy(), 'bo', label='Predicted')

plt.show()
