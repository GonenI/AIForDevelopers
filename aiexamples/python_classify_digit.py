import random

# Generate data
def generate_data():
    data = []
    labels = []
    # Class 1
    for _ in range(33):
        image = [0, 1, 0, 0, 1, 0, 0, 1, 0]  # Label 1
        labels.append(1)
        data.append(flip_bit(image))
    # Class 0
    for _ in range(33):
        image = [1, 1, 1, 1, 0, 1, 1, 1, 1]  # Label 0
        labels.append(0)
        data.append(flip_bit(image))
    # Class X
    for _ in range(33):
        image = [1, 0, 1, 0, 1, 0, 1, 0, 1]  # Label X
        labels.append(2)
        data.append(flip_bit(image))
    return data, labels

def flip_bit(image):
    index = random.randint(0, 8)
    image[index] = 1 - image[index]
    return image

# Create dataset
data, labels = generate_data()

# Network Initialization
import math

# Initialize weights and biases
input_size = 9
hidden_size = 18
output_size = 3

weights1 = [[random.uniform(-1, 1) for _ in range(hidden_size)] for _ in range(input_size)]
biases1 = [random.uniform(-1, 1) for _ in range(hidden_size)]

weights2 = [[random.uniform(-1, 1) for _ in range(hidden_size)] for _ in range(hidden_size)]
biases2 = [random.uniform(-1, 1) for _ in range(hidden_size)]

weights3 = [[random.uniform(-1, 1) for _ in range(output_size)] for _ in range(hidden_size)]
biases3 = [random.uniform(-1, 1) for _ in range(output_size)]

# Activation functions
def relu(x):
    return [max(0, i) for i in x]

def softmax(x):
    exp_x = [math.exp(i) for i in x]
    sum_exp_x = sum(exp_x)
    return [i / sum_exp_x for i in exp_x]

# Feedforward
def feedforward(image):
    # First layer
    hidden1 = relu([sum(image[i] * weights1[i][j] for i in range(input_size)) + biases1[j] for j in range(hidden_size)])
    
    # Second layer
    hidden2 = relu([sum(hidden1[i] * weights2[i][j] for i in range(hidden_size)) + biases2[j] for j in range(hidden_size)])
    
    # Output layer
    output = softmax([sum(hidden2[i] * weights3[i][j] for i in range(hidden_size)) + biases3[j] for j in range(output_size)])
    
    return hidden1, hidden2, output

# backpropagation
def backpropagation(image, label, hidden1, hidden2, output, learning_rate):
    # Output layer gradients
    target = [0, 0, 0]
    target[label] = 1
    
    d_output = [output[i] - target[i] for i in range(output_size)]
    
    # Hidden layer 2 gradients
    d_hidden2 = [sum(d_output[j] * weights3[i][j] for j in range(output_size)) * (1 if hidden2[i] > 0 else 0) for i in range(hidden_size)]
    
    # Hidden layer 1 gradients
    d_hidden1 = [sum(d_hidden2[j] * weights2[i][j] for j in range(hidden_size)) * (1 if hidden1[i] > 0 else 0) for i in range(hidden_size)]
    
    # Update weights and biases for output layer
    for i in range(hidden_size):
        for j in range(output_size):
            weights3[i][j] -= learning_rate * d_output[j] * hidden2[i]
        biases3[j] -= learning_rate * d_output[j]
    
    # Update weights and biases for hidden layer 2
    for i in range(hidden_size):
        for j in range(hidden_size):
            weights2[i][j] -= learning_rate * d_hidden2[j] * hidden1[i]
        biases2[j] -= learning_rate * d_hidden2[j]
    
    # Update weights and biases for hidden layer 1
    for i in range(input_size):
        for j in range(hidden_size):
            weights1[i][j] -= learning_rate * d_hidden1[j] * image[i]
        biases1[j] -= learning_rate * d_hidden1[j]

# Training loop
# Training parameters
learning_rate = 0.01
epochs = 1000

# Training loop
for epoch in range(epochs):
    total_loss = 0
    for image, label in zip(data, labels):
        # Feedforward
        hidden1, hidden2, output = feedforward(image)
        
        # Calculate loss (cross-entropy)
        target = [0, 0, 0]
        target[label] = 1
        loss = -sum(target[i] * math.log(output[i]) for i in range(output_size))
        total_loss += loss
        
        # Backpropagation
        backpropagation(image, label, hidden1, hidden2, output, learning_rate)
    
    if epoch % 100 == 0:
        print(f'Epoch [{epoch}/{epochs}], Loss: {total_loss / len(data):.4f}')


# Evaluation
def flip_bit(image):
    index = random.randint(0, 8)
    image[index] = 1 - image[index]
    return image

# Evaluation loop
while True:
    user_input = input("Enter 0, 1, or X (or 'quit' to exit): ")
    if user_input.lower() == 'quit':
        break
    
    if user_input == '0':
        image = [1, 1, 1, 1, 0, 1, 1, 1, 1]
    elif user_input == '1':
        image = [0, 1, 0, 0, 1, 0, 0, 1, 0]
    elif user_input == 'X':
        image = [1, 0, 1, 0, 1, 0, 1, 0, 1]
    else:
        print("Invalid input, try again.")
        continue
    
    image = flip_bit(image)
    image = flip_bit(image)
    image = flip_bit(image)
    image = flip_bit(image)
    
    _, _, output = feedforward(image)
    predicted_label = output.index(max(output))
    
    label_map = {0: '0', 1: '1', 2: 'X'}
    print(f'Predicted label: {label_map[predicted_label]}')

