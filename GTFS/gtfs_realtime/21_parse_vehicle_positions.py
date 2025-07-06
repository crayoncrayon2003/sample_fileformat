import os
import json
from google.transit import gtfs_realtime_pb2

def parse_vehicle_positions(bin_path, out_path):
    feed = gtfs_realtime_pb2.FeedMessage()
    with open(bin_path, 'rb') as f:
        feed.ParseFromString(f.read())

    features = []
    for entity in feed.entity:
        if not entity.HasField("vehicle"):
            continue
        v = entity.vehicle
        if not v.HasField("position"):
            continue

        lat = v.position.latitude
        lon = v.position.longitude

        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [lon, lat]
            },
            "properties": {
                "vehicle_id": v.vehicle.id if v.vehicle.HasField("id") else None,
                "trip_id": v.trip.trip_id if v.trip.HasField("trip_id") else None,
                "route_id": v.trip.route_id if v.trip.HasField("route_id") else None,
                "bearing": getattr(v.position, "bearing", None),
                "speed": getattr(v.position, "speed", None),
                "timestamp": v.timestamp if v.HasField("timestamp") else None
            }
        }
        features.append(feature)

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)

def main():
    directory = os.path.dirname(os.path.abspath(__file__))
    path_vehicle_position_in = os.path.join(directory, "vehicle_position.bin")
    path_vehicle_position_out = os.path.join(directory, "vehicle_positions.geojson")

    parse_vehicle_positions(path_vehicle_position_in, path_vehicle_position_out)

if __name__ == "__main__":
    main()
