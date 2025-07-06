# 1. get sample data
https://www.bus-kyo.or.jp/gtfs-open-data

## 1.1. get gtfs static
```
cd gtfs_static
python 11_download_zip.py
python 12_extract_zip.py
python 21_shapes_to_geojson.py
```

## 1.2. get gtfs realtime
```
cd gtfs_realtime
python 11_download_bin.py
python 21_parse_vehicle_positions.py
python 22_parse_trip_updates.py
python 23_parse_alerts.py
```

# 2. Exec
index.html

