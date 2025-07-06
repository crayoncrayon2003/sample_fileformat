import os
import json
from google.transit import gtfs_realtime_pb2
import requests

def download_gtfs_realtime_bin(url, save_path):
    print(f"📥 Downloading GTFS-RT bin from {url}...")
    response = requests.get(url)
    response.raise_for_status()
    with open(save_path, 'wb') as f:
        f.write(response.content)
    print(f"✅ Saved to {save_path}")


def main():
    gtfs_url = "https://example.com/realtime/"
    vehicle_position_url = gtfs_url+"vehicle_position.bin"
    trip_update_url = gtfs_url+"trip_updates.bin"
    alerts_url = gtfs_url+"alerts.bin"

    directory = os.path.dirname(os.path.abspath(__file__))
    path_vehicle_position_local = os.path.join(directory, "vehicle_position.bin")
    path_trip_update_local = os.path.join(directory, "trip_updates.bin")
    path_alerts_local = os.path.join(directory, "alerts.bin")

    download_gtfs_realtime_bin(vehicle_position_url, path_vehicle_position_local)
    download_gtfs_realtime_bin(trip_update_url, path_trip_update_local)
    download_gtfs_realtime_bin(alerts_url, path_alerts_local)

if __name__ == "__main__":
    main()
