import json
import numpy as np
import matplotlib.pyplot as plt
from radar_functions import generate_radar_data, initialize_kalman_filters, update_radar_positions, plot_radars_and_objects, read_radar_data, merge_data, fuse_data, update
from matplotlib.animation import FuncAnimation

if __name__ == "__main__":
    radar_filename = "radar_data.json"
    detected_objects_filename = "detected_objects.json"

    # Generate radar data if the file does not exist
    radar_count = 5  # Example number of radars
    map_size = 200  # Example map size
    try:
        radar_data = read_radar_data(radar_filename)
        if not radar_data:
            radar_data = generate_radar_data(radar_count, map_size, radar_filename)
    except FileNotFoundError:
        radar_data = generate_radar_data(radar_count, map_size, radar_filename)

    merged_data = merge_data(radar_data, None)

    # Initialize Kalman filters for radar positions
    kalman_filters = initialize_kalman_filters(merged_data)

    # Generate random objects on the map with varying densities
    object_density = 0.0005  # Adjust density as needed
    num_objects = int(map_size ** 2 * object_density)
    objects = np.random.rand(num_objects, 2) * map_size * 2 - map_size  # Random positions

    detected_objects = []  # List to store detected objects

    # Set up the figure and axis
    fig, ax = plt.subplots(figsize=(8, 8))

    # Create the animation
    ani = FuncAnimation(fig, update, frames=20, fargs=(merged_data, kalman_filters, objects, map_size, ax, detected_objects), interval=500)

    # Show the animation
    plt.show()

    # Save detected objects to a file
    try:
        with open(detected_objects_filename, "w") as file:
            json.dump(detected_objects, file)
        print("Detected objects successfully saved to:", detected_objects_filename)
    except Exception as e:
        print("Error saving detected objects:", e)

    # Print detected objects
    print("Detected objects coordinates:")
    for obj in detected_objects:
        print(obj)
