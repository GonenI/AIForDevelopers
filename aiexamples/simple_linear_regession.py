import numpy as np
import matplotlib.pyplot as plt

# Generate some random data
np.random.seed(0)
X = 2 * np.random.rand(100, 1)  # Generate 100 random values between 0 and 2
y = 4 + 3 * X + np.random.randn(100, 1)  # y = 4 + 3*X + noise

# Manually calculate slope and intercept using least squares
X_mean = np.mean(X)
y_mean = np.mean(y)

numerator = 0
denominator = 0
for i in range(len(X)):
    numerator += (X[i] - X_mean) * (y[i] - y_mean)
    denominator += (X[i] - X_mean) ** 2

coefficient = numerator / denominator
intercept = y_mean - (coefficient * X_mean)

# Print the calculated intercept and coefficient
print("Intercept (β0):", intercept)
print("Coefficient (β1):", coefficient)

# Plot the data points
plt.plot(X, y, "b.")

# Plot the fitted line
X_new = np.array([[0], [2]])  # Generate X values for the line (from 0 to 2)
y_predict = intercept + coefficient * X_new
plt.plot(X_new, y_predict, "r-")

# Add labels and title
plt.xlabel("X")
plt.ylabel("y")
plt.title("Simple Linear Regression")

# Show the plot
plt.show()
