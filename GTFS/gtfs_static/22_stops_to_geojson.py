import csv
import json
import os

def convert_stops_to_geojson(stops_csv_path, output_geojson_path):
    features = []

    with open(stops_csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        print("Columns in stops.csv:", reader.fieldnames)

        for row in reader:
            try:
                lat = float(row.get('stop_lat') or row.get('stopLat') or 0)
                lon = float(row.get('stop_lon') or row.get('stopLon') or 0)
            except ValueError:
                continue

            stop_id = row.get('stop_id') or row.get('stopId') or row.get('stop-id') or "unknown"
            stop_name = row.get('stop_name') or row.get('stopName') or "unknown"

            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [lon, lat]
                },
                "properties": {
                    "stop_id": stop_id,
                    "stop_name": stop_name
                }
            }
            features.append(feature)

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    with open(output_geojson_path, 'w', encoding='utf-8') as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)

def main():
    directory = os.path.dirname(os.path.abspath(__file__))

    path_stop_in  = os.path.join(directory, "stops.txt")
    path_stop_out = os.path.join(directory, "stops.geojson")
    convert_stops_to_geojson(path_stop_in, path_stop_out)

if __name__ == "__main__":
    main()
