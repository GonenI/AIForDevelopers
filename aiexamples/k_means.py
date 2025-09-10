import numpy as np

# Define the matrix
matrix = np.array([
    [1, 1, 0, 0, 1, 1],
    [1, 1, 0, 1, 0, 0],
    [0, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0, 0],
    [1, 1, 0, 0, 0, 0]
])

# Extract coordinates of all '1's
one_coords = np.argwhere(matrix == 1)

# Define number of clusters
K = 2

# Initialize centroids randomly from the points
np.random.seed(0)
initial_centroids_indices = np.random.choice(len(one_coords), K, replace=False)
centroids = one_coords[initial_centroids_indices]

# Function to calculate Euclidean distance
def euclidean_distance(coord1, coord2):
    return np.sqrt(np.sum((np.array(coord1) - np.array(coord2))**2))

# K-means algorithm
def k_means_clustering(coords, centroids, max_iters=100):
    for _ in range(max_iters):
        # Assign clusters based on closest centroid
        clusters = [[] for _ in range(K)]
        for coord in coords:
            distances = [euclidean_distance(coord, centroid) for centroid in centroids]
            closest_centroid_index = np.argmin(distances)
            clusters[closest_centroid_index].append(coord)

        # Update centroids
        new_centroids = []
        for cluster in clusters:
            if cluster:  # Avoid division by zero if cluster is empty
                new_centroid = np.mean(cluster, axis=0)
                new_centroids.append(new_centroid)
            else:
                # If a cluster is empty, reinitialize its centroid
                new_centroids.append(coords[np.random.choice(len(coords))])

        new_centroids = np.array(new_centroids)

        # Check for convergence (if centroids do not change)
        if np.allclose(centroids, new_centroids):
            break

        centroids = new_centroids

    return clusters, centroids

# Run K-means clustering
clusters, final_centroids = k_means_clustering(one_coords, centroids)

# Create a new matrix with cluster assignments
clustered_matrix = np.zeros_like(matrix)
for cluster_index, cluster in enumerate(clusters):
    for coord in cluster:
        clustered_matrix[tuple(coord)] = cluster_index + 1  # +1 to differentiate from 0

# Print the clustered matrix
print(clustered_matrix)
