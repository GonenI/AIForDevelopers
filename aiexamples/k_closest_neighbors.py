class Point:
  """Represents a point with x and y coordinates and distance from target."""

  def __init__(self, xcoord, ycoord, distance_from_target=None):
    self.xcoord = xcoord
    self.ycoord = ycoord
    self.distance_from_target = distance_from_target

def get_neighbors_and_points(data):
  """Gets a list of neighbors and the point to classify.

  Args:
      data: A list of lists representing training data points (matrices).

  Returns:
      A tuple containing:
          - neighbors: A list of Point objects for neighbors (1 or 2).
          - point_coord: A Point object for the point to classify (marked by 3).
  """
  neighbors = []
  point_coord = None
  for i, row in enumerate(data):
    for j, val in enumerate(row):
      if val in (1, 2):  # Neighbor (class 1 or 2)
        neighbors.append(Point(i, j))
      elif val == 'X':  # Point to classify (marked by 3)
        point_coord = Point(i, j)

  return neighbors, point_coord

def euclidean_distance(p1, p2):
  """Calculates the Euclidean distance between two points and updates the distance_from_target member."""
  distance = ((p1.xcoord - p2.xcoord)**2 + (p1.ycoord - p2.ycoord)**2)**0.5
  return distance

def classify_knn(neighbors, point_coord, k):
  """Classifies a point using K Nearest Neighbors algorithm based on neighbors.

  Args:
      neighbors: A list of Point objects for neighbors (1 or 2).
      point_coord: A Point object for the point to classify.
      k: The number of neighbors to consider.

  Returns:
      The most frequent class among the k nearest neighbors.
  """
  class1_count = 0
  class2_count = 0

  # Calculate distances and update neighbor objects (error was here)
  for neighbor in neighbors:
    if neighbor != point_coord:  # Avoid calculating distance to itself (fixed)
      neighbor.distance_from_target = euclidean_distance(point_coord, neighbor)

  # Sort neighbors by distance (using the member variable)
  neighbors.sort(key=lambda x: x.distance_from_target)

  # Get k nearest neighbors
  k_nearest_neighbors = neighbors[:k]

  # Count class occurrences only among k nearest neighbors
  for neighbor in k_nearest_neighbors:
    neighbor_x = neighbor.xcoord
    neighbor_y = neighbor.ycoord
    if data[neighbor_x][neighbor_y] == 1:
      class1_count += 1
    elif data[neighbor_x][neighbor_y] == 2:
      class2_count += 1

  # Find most frequent class based on counts
  predicted_class = 1 if class1_count > class2_count else 2

  return predicted_class

# Sample data (replace with your actual data)
data = [
    [1, 2, 1, 0, 1, 2],
    [1, 2, 1, 1, 0, 0],
    [0, 2, 2, 2, 0, 0],
    [2,2, 2, 2, 0, 0],
    [0, 1, 2, 0, 0, 0],
    ['X', 1, 2, 0, 0, 0]  # Point to classify (marked by 3)
]

# Get neighbors and point coordinates
neighbors, point_coord = get_neighbors_and_points(data)

# Number of neighbors
k = 4

# Classify the point (assuming class 1 for neighbors)
predicted_class = classify_knn(neighbors, point_coord, k)

print("Predicted class for the point:", predicted_class)
