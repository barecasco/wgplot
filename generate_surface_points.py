import numpy as np
import csv
import random





def generate_terrain_data(size=512, roughness=0.5, height_scale=100):
    """
    Generates a heightmap representing terrain using the midpoint displacement algorithm.

    Args:
        size (int): The size of the square heightmap (size x size). Must be a power of 2 plus 1.
        roughness (float):  A value between 0 and 1 controlling the terrain roughness.
                           Higher values result in more jagged terrain.
        height_scale (float):  Scales the generated height values.  Higher values lead to more dramatic elevation changes.

    Returns:
        numpy.ndarray: A 2D numpy array representing the heightmap.
    """

    # if not (size & (size - 1) == 0):
    #     raise ValueError("Size must be a power of 2 plus 1.")

    heightmap = np.zeros((size, size))

    def displace(x1, y1, x2, y2, random_seed):
        """Recursive function to apply midpoint displacement."""

        if x2 - x1 <= 1:  # Base case: interval is small enough
            return

        mid_x = (x1 + x2) // 2
        mid_y = (y1 + y2) // 2

        # Calculate midpoint values
        if heightmap[mid_x, y1] == 0: # check is the points are initialzed before assigning value
            heightmap[mid_x, y1] = (heightmap[x1, y1] + heightmap[x2, y1]) / 2 + np.random.normal(0, roughness * height_scale,1)[0]
        if heightmap[mid_x, y2] == 0:
            heightmap[mid_x, y2] = (heightmap[x1, y2] + heightmap[x2, y2]) / 2 + np.random.normal(0, roughness * height_scale,1)[0]
        if heightmap[x1, mid_y] == 0:
            heightmap[x1, mid_y] = (heightmap[x1, y1] + heightmap[x1, y2]) / 2 + np.random.normal(0, roughness * height_scale,1)[0]
        if heightmap[x2, mid_y] == 0:
            heightmap[x2, mid_y] = (heightmap[x2, y1] + heightmap[x2, y2]) / 2 + np.random.normal(0, roughness * height_scale,1)[0]

        heightmap[mid_x, mid_y] = (heightmap[x1, y1] + heightmap[x2, y1] + heightmap[x1, y2] + heightmap[x2, y2]) / 4 + np.random.normal(0, roughness * height_scale,1)[0]



        # Recursive calls for the four sub-squares
        displace(x1, y1, mid_x, mid_y,random_seed)
        displace(mid_x, y1, x2, mid_y,random_seed)
        displace(x1, mid_y, mid_x, y2,random_seed)
        displace(mid_x, mid_y, x2, y2,random_seed)


    # Initialize corner values (can be any arbitrary values)
    np.random.seed(42) #set random seed for reproducability

    random_seed = np.random.randint(1,1000)
    heightmap[0, 0] = np.random.uniform(0, height_scale/2)
    heightmap[size - 1, 0] = np.random.uniform(0, height_scale/2)
    heightmap[0, size - 1] = np.random.uniform(0, height_scale/2)
    heightmap[size - 1, size - 1] = np.random.uniform(0, height_scale/2)

    displace(0, 0, size - 1, size - 1, random_seed)


    return heightmap


def heightmap_to_points(heightmap, x_scale=1.0, y_scale=1.0, z_scale=1.0):
    """
    Converts a heightmap (2D numpy array) into a list of 3D points.

    Args:
        heightmap (numpy.ndarray): The heightmap data.
        x_scale (float): Scaling factor for the X coordinate.
        y_scale (float): Scaling factor for the Y coordinate.
        z_scale (float): Scaling factor for the Z coordinate (height).

    Returns:
        list: A list of tuples, where each tuple represents a 3D point (x, y, z).
    """
    size = heightmap.shape[0]
    points = []
    for x in range(size):
        for y in range(size):
            z = heightmap[x, y]
            points.append((x * x_scale, y * y_scale, z * z_scale))
    return points


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


if __name__ == "__main__":
    # Configuration parameters
    terrain_size         = 2**10 + 1  # Size of the terrain (must be 2^n + 1)
    terrain_roughness    = 0.35 # Adjust this value for smoother or more rugged terrain
    terrain_height_scale = 150.0 # Adjust for overall terrain height
    x_scale = 5.0       # Adjust these scales to change the dimensions of the terrain
    y_scale = 5.0
    z_scale = 1.0

    # Generate the terrain heightmap
    heightmap = generate_terrain_data(size=terrain_size, roughness=terrain_roughness, height_scale=terrain_height_scale)

    # Convert the heightmap to a list of 3D points
    points = heightmap_to_points(heightmap, x_scale=x_scale, y_scale=y_scale, z_scale=z_scale)

    # Save the points to a CSV file
    save_points_to_csv(points, filename="terrain.csv")

    print("Terrain generation complete!")