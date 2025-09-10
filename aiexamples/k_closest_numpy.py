import numpy as np

# Custom Euclidean distance function
def euclidean_distance(coord1, coord2):
    return np.sqrt(np.sum((np.array(coord1) - np.array(coord2))**2))

# Define the matrix
matrix = np.array([
    [1, 2, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 2, 0, 0, 0, 0],
    [3, 0, 0, 0, 0, 0]
])

# Get the coordinates of non-zero values
non_zero_coords = np.argwhere(matrix > 0)

# Get the coordinates and value of the point to classify
target_coord = np.argwhere(matrix == 3)[0]

# Define the value K
K = 3

# Calculate distances from the target point to all other points
distances = []
for coord in non_zero_coords:
    if not np.array_equal(coord, target_coord):
        dist = euclidean_distance(target_coord, coord)
        distances.append((dist, tuple(coord)))

# Sort distances and select the K closest neighbors
distances.sort(key=lambda x: x[0])
closest_neighbors = distances[:K]

# Determine the classes of the K closest neighbors
neighbor_classes = [matrix[coord] for _, coord in closest_neighbors]

# Classify the target point based on the majority class of the neighbors
classification = max(set(neighbor_classes), key=neighbor_classes.count)

# Print the classification result
print(f"The value '3' is classified as: {classification}")

# Print the closest neighbors for verification
print(f"The K closest neighbors are: {closest_neighbors}")
print(f"The classes of the K closest neighbors are: {neighbor_classes}")
