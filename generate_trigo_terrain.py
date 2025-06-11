import math
import numpy as np
import random
import csv

def save_points_to_csv(points, filename="terrain.csv"):
    """
    Saves a list of 3D points to a CSV file.

    Args:
        points (list): A list of tuples, where each tuple represents a 3D point (x, y, z).
        filename (str): The name of the CSV file to create.
    """
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['x', 'y', 'z'])  # Write header row
        writer.writerows(points)
    print(f"Points saved to {filename}")


def generate_random_points(x_length, y_length, num_size):
    """
    Generate random points within specified x and y boundaries.
    
    Args:
        x_length (float): Maximum x coordinate (from 0 to x_length)
        y_length (float): Maximum y coordinate (from 0 to y_length)
        num_size (int): Number of random points to generate
    
    Returns:
        list: List of tuples containing (x, y) coordinates
    """
    points = []
    
    for _ in range(num_size):
        x = random.uniform(0, x_length)
        y = random.uniform(0, y_length)
        points.append((x, y))
    
    return points


def terrain_height(x, y):
    """
    Generate terrain-like height values using trigonometric functions.
    
    Args:
        x (float): X coordinate
        y (float): Y coordinate
    
    Returns:
        float: Height value z representing terrain elevation
    """
    # Base terrain with large-scale hills
    base_terrain = 10 * math.sin(x * 0.1) * math.cos(y * 0.1)
    
    # Medium-scale rolling hills
    rolling_hills = 5 * math.sin(x * 0.3) * math.sin(y * 0.2)
    
    # Small-scale details and ridges
    fine_details = 2 * math.cos(x * 0.8) * math.sin(y * 0.7)
    
    # Additional complexity with crossed sine waves
    cross_waves = 1.5 * math.sin(x * 0.15 + y * 0.1) * math.cos(x * 0.1 - y * 0.2)
    
    # Combine all components
    z = base_terrain + rolling_hills + fine_details + cross_waves
    
    return z



if __name__ == "__main__":
    # Configuration parameters
    terrain_width        = 10
    terrain_length       = 10
    num_size             = 2000

    # Convert the heightmap to a list of 3D points
    rpoints = generate_random_points(terrain_width, terrain_length, num_size)
    points  = []
    for rpoint in rpoints:
        x = rpoint[0]
        y = rpoint[1]
        z = terrain_height(x, y)
        points.append((x, y, z))

    # Save the points to a CSV file
    save_points_to_csv(points, filename="terrain.csv")

    print("Terrain generation complete!")