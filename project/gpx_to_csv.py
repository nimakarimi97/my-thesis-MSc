import gpxpy
import gpxpy.gpx
import numpy as np
import haversine as hs
import pandas as pd
import os
import gpxpy
import pandas as pd


def gpx_to_csv(gpx_file_path, csv_file_path):
    with open(gpx_file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    route_info = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                route_info.append({
                    'time': point.time,
                    'latitude': point.latitude,
                    'longitude': point.longitude,
                    'elevation': point.elevation
                })

    route_df = pd.DataFrame(route_info)
    route_df.to_csv(csv_file_path, index=False)


def convert_all_gpx_to_csv(gpx_dir, csv_dir):
    for filename in os.listdir(gpx_dir):
        if filename.endswith('.gpx'):
            gpx_file_path = os.path.join(gpx_dir, filename)
            csv_file_path = os.path.join(
                csv_dir, filename.replace('.gpx', '.csv'))
            gpx_to_csv(gpx_file_path, csv_file_path)


# Usage
gpx_dir = './data/gpx/'
csv_dir = './data/csv/'
# convert_all_gpx_to_csv(gpx_dir, csv_dir)
