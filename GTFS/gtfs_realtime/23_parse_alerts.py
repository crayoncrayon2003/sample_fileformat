import os
import json
from google.transit import gtfs_realtime_pb2

def parse_alerts(bin_path, out_path):
    feed = gtfs_realtime_pb2.FeedMessage()
    with open(bin_path, 'rb') as f:
        feed.ParseFromString(f.read())

    alerts = []
    for entity in feed.entity:
        if entity.HasField("alert"):
            a = entity.alert
            alert_info = {
                "cause": gtfs_realtime_pb2.Alert.Cause.Name(a.cause),
                "effect": gtfs_realtime_pb2.Alert.Effect.Name(a.effect),
                "header_text": a.header_text.translation[0].text if a.header_text.translation else "",
                "description_text": a.description_text.translation[0].text if a.description_text.translation else ""
            }
            alerts.append(alert_info)

    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(alerts, f, ensure_ascii=False, indent=2)

def main():
    directory = os.path.dirname(os.path.abspath(__file__))
    path_alerts_in = os.path.join(directory, "alerts.bin")
    path_alerts_out = os.path.join(directory, "alerts.json")

    parse_alerts(path_alerts_in, path_alerts_out)

if __name__ == "__main__":
    main()
