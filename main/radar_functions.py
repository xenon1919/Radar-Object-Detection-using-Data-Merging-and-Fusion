import matplotlib.pyplot as plt
import numpy as np
import json
from kalman_filter import KalmanFilter

# Function to generate radar data randomly
def generate_radar_data(radar_count, map_size, filename):
    radar_data_all = []
    for radar_id in range(radar_count):
        position = (np.random.rand(2) * 2 - 1) * map_size
        radar_data = {
            "radar_id": radar_id,
            "position": position.tolist(),  # Convert position to list
            "range": np.random.uniform(10, 30)  # Reduced range
        }
        radar_data_all.append(radar_data)
    
    try:
        with open(filename, "w") as file:
            json.dump(radar_data_all, file)
        print("Radar data successfully saved to:", filename)
    except Exception as e:
        print("Error:", e)
    
    return radar_data_all

# Function to initialize Kalman Filters for radar positions
def initialize_kalman_filters(radar_data):
    kalman_filters = {}
    for radar in radar_data:
        kf = KalmanFilter(dim_x=4, dim_z=2)
        kf.x[:2, 0] = radar["position"]  # Initial position
        kf.F = np.array([[1, 0, 1, 0],
                         [0, 1, 0, 1],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]])  # State transition matrix
        kf.H = np.array([[1, 0, 0, 0],
                         [0, 1, 0, 0]])  # Measurement function
        kf.P *= 10  # Initial uncertainty
        kf.R *= 5  # Measurement uncertainty
        kf.Q = np.eye(4)  # Process uncertainty
        kalman_filters[radar["radar_id"]] = kf
    return kalman_filters

# Function to update radar positions using Kalman Filters
def update_radar_positions(radar_data, kalman_filters, map_size):
    for radar in radar_data:
        radar_id = radar["radar_id"]
        kf = kalman_filters[radar_id]
        kf.predict()
        
        # Simulate a noisy measurement
        measurement = radar["position"] + np.random.randn(2) * 5
        kf.update(measurement)
        
        radar["position"] = kf.x[:2, 0]
        radar["position"] = np.clip(radar["position"], -map_size, map_size)  # Ensure radar stays within map bounds

def plot_radars_and_objects(ax, radar_data, objects, map_size):
    ax.clear()  # Clear the axis before plotting
    ax.plot(objects[:, 0], objects[:, 1], 'bo', markersize=5, label='Undetected Objects')  # Plot all objects initially as undetected
    for radar in radar_data:
        position = radar["position"]
        max_range = radar["range"]
        circle = plt.Circle(position, max_range, color='r', fill=False, alpha=0.3)  # Plot radar coverage area
        ax.add_artist(circle)
        ax.plot(position[0], position[1], 'ro', markersize=8, label=f'Radar {radar["radar_id"]}')  # Plot radar position

        detected_objects = objects[np.linalg.norm(objects - np.array(position), axis=1) <= max_range]
        for obj in detected_objects:
            ax.plot(obj[0], obj[1], 'go', markersize=5)  # Change color of detected objects to green

    ax.set_xlim(-map_size, map_size)
    ax.set_ylim(-map_size, map_size)
    ax.set_aspect('equal')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Radar Object Detection Map')
    ax.legend()

def read_radar_data(filename):
    try:
        with open(filename, "r") as file:
            radar_data = json.load(file)
        print("Radar data successfully loaded from:", filename)
        return radar_data
    except Exception as e:
        print("Error:", e)
        return []

def merge_data(radar_data, sensor_data):
    return radar_data

def fuse_data(merged_data):
    fused_data = {}
    for radar in merged_data:
        radar_id = radar["radar_id"]
        if radar_id not in fused_data:
            fused_data[radar_id] = {"position": radar["position"], "range": radar["range"]}
        else:
            prev_position = fused_data[radar_id]["position"]
            prev_range = fused_data[radar_id]["range"]
            count = fused_data[radar_id].get("count", 1)
            fused_data[radar_id]["position"] = (prev_position * count + radar["position"]) / (count + 1)
            fused_data[radar_id]["range"] = max(prev_range, radar["range"])
            fused_data[radar_id]["count"] = count + 1
    return list(fused_data.values())

def update(frame, radar_data, kalman_filters, objects, map_size, ax, detected_objects):
    update_radar_positions(radar_data, kalman_filters, map_size)
    ax.clear()
    
    # Print predicted positions
    print("Predicted Radar Positions:")
    for radar_id, kf in kalman_filters.items():
        print(f"Radar {radar_id}: {kf.x[:2, 0]}")

    plot_radars_and_objects(ax, radar_data, objects, map_size)
    for radar in radar_data:
        position = radar["position"]
        max_range = radar["range"]
        detected = objects[np.linalg.norm(objects - np.array(position), axis=1) <= max_range]
        detected_objects.extend(detected.tolist())
