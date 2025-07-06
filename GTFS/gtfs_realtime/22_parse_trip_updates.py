import os
import json
from google.transit import gtfs_realtime_pb2

def parse_trip_updates(bin_path, out_path):
    feed = gtfs_realtime_pb2.FeedMessage()
    with open(bin_path, 'rb') as f:
        feed.ParseFromString(f.read())

    updates = []
    for entity in feed.entity:
        if entity.HasField("trip_update"):
            tu = entity.trip_update
            trip_info = {
                "trip_id": tu.trip.trip_id,
                "route_id": tu.trip.route_id,
                "start_time": tu.trip.start_time,
                "stop_time_updates": []
            }
            for stu in tu.stop_time_update:
                stop_update = {
                    "stop_id": stu.stop_id,
                    "arrival": stu.arrival.time if stu.HasField("arrival") else None,
                    "departure": stu.departure.time if stu.HasField("departure") else None
                }
                trip_info["stop_time_updates"].append(stop_update)
            updates.append(trip_info)

    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(updates, f, ensure_ascii=False, indent=2)


def main():
    directory = os.path.dirname(os.path.abspath(__file__))

    path_trip_update_in = os.path.join(directory, "trip_updates.bin")
    path_trip_update_out = os.path.join(directory,"trip_updates.json")

    parse_trip_updates(path_trip_update_in, path_trip_update_out)


if __name__ == "__main__":
    main()
