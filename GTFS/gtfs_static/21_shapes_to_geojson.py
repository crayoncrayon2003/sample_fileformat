import csv
import json
import os

def convert_shapes_to_geojson(shapes_csv_path, output_geojson_path):
    shape_points = {}

    with open(shapes_csv_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        print("Columns in shapes.csv:", reader.fieldnames)

        shape_id_key = None
        for candidate in ['shape_id', 'shapeid', 'shape-id']:
            if candidate in reader.fieldnames:
                shape_id_key = candidate
                break
        if shape_id_key is None:
            raise ValueError("No 'shape_id' column found in shapes.csv")

        lat_key = None
        for candidate in ['shape_pt_lat', 'shape_pt_latitude']:
            if candidate in reader.fieldnames:
                lat_key = candidate
                break
        if lat_key is None:
            raise ValueError("No 'shape_pt_lat' column found in shapes.csv")

        lon_key = None
        for candidate in ['shape_pt_lon', 'shape_pt_longitude']:
            if candidate in reader.fieldnames:
                lon_key = candidate
                break
        if lon_key is None:
            raise ValueError("No 'shape_pt_lon' column found in shapes.csv")

        seq_key = None
        for candidate in ['shape_pt_sequence', 'shape_pt_seq']:
            if candidate in reader.fieldnames:
                seq_key = candidate
                break
        if seq_key is None:
            raise ValueError("No 'shape_pt_sequence' column found in shapes.csv")

        for row in reader:
            shape_id = row[shape_id_key]
            lat = float(row[lat_key])
            lon = float(row[lon_key])
            seq = int(row[seq_key])

            if shape_id not in shape_points:
                shape_points[shape_id] = []
            shape_points[shape_id].append((seq, lon, lat))

    features = []
    for shape_id, points in shape_points.items():
        points.sort(key=lambda x: x[0])
        coords = [[lon, lat] for _, lon, lat in points]

        feature = {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": coords
            },
            "properties": {
                "shape_id": shape_id
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
    path_shape_in = os.path.join(directory, "shapes.txt")
    path_shape_out = os.path.join(directory, "shapes.geojson")
    convert_shapes_to_geojson(path_shape_in, path_shape_out)

if __name__ == "__main__":
    main()
