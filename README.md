# Object Detection Using Radar Data Merging and Fusion
This repository contains the code and documentation for a project focused on object detection using radar systems. Developed during my internship at the Defence Research and Development Organisation (DRDO), this project leverages radar data simulation, data merging, and fusion techniques to dynamically detect and track objects on a geographical map.

# Project Overview
The primary goal of this project is to enhance the accuracy and reliability of object detection by integrating data from multiple radars. The system simulates radar signals, processes the data, and visualizes the real-time movements of radars and objects on a map. Key features include radar data generation, dynamic visualization, and data fusion algorithms.

# Features
Radar Data Simulation:
Generates dynamic radar data for multiple radars and moving objects.
Simulates radar signals and detects objects based on distance and movement patterns.
# Data Merging and Fusion:
Integrates radar data from multiple sources to improve detection accuracy.
Implements algorithms for data merging and fusion to generate a comprehensive view of tracked objects.
# Dynamic Visualization:
Displays real-time movements of radars and objects on a geographical map.
Highlights detected objects and their characteristics, including latitude, longitude, and specific attributes.

# Technologies and Tools
# Python Libraries:
NumPy: For numerical operations and data processing.
Folium: For creating dynamic maps and visualizing radar and object movements.
Plotly: For additional data visualization and plotting.

# Project Structure
src/generate_radar_data.py:
Generates radar data by simulating the positions and movements of radars and objects.
Saves the generated radar data to a JSON file.
src/fuse_and_detect.py:
Reads the generated radar data from the JSON file.
Performs data merging and fusion to integrate detections from multiple radars.
Updates a dynamic map with the latest positions of radars and objects.
Visualizes the fused data and highlights detected objects.

# Usage
Generate Radar Data:
Run generate_radar_data.py to simulate and generate radar data.
The generated data will be saved in radar_data.json.
Fuse and Detect:
Run fuse_and_detect.py to read the generated radar data, perform data fusion, and update the map.
The dynamic map will display the movements and detections in real-time.

# Contributions
Contributions to this project are welcome. Feel free to fork the repository and submit pull requests with improvements or new features.
