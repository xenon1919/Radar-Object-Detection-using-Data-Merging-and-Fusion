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