import gpxpy
import gpxpy.gpx
import numpy as np
import haversine as hs
import pandas as pd
import os
import gpxpy
import pandas as pd
from tqdm import tqdm

report = []


def haversine_distance(lat1, lon1, lat2, lon2) -> float:
    distance = hs.haversine(
        point1=(lat1, lon1),
        point2=(lat2, lon2),
        unit=hs.Unit.METERS
    )
    return np.round(distance, 2)


def lift_checker(df):
    number_of_lifts = 0
    df['lift?'] = 0  # ? set the "lift?" column to zero
    df['lift_path'] = 0

    for i in range(len(df)):
        if df['altitude_diff'][i] > 100:
            number_of_lifts += 1
            df.loc[i, 'lift?'] = 1
            df.loc[i-1:i, 'lift_path'] = 1

    return number_of_lifts


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
                    'altitude': point.elevation
                })

    route_df = pd.DataFrame(route_info)

    route_df['altitude_diff'] = route_df['altitude'].diff()
    route_df['relative_elevation'] = route_df['altitude_diff'].cumsum()

    distances = [np.nan]
    speed = [np.nan]

    for i in range(1, len(route_df)):
        distances.append(haversine_distance(
            lat1=route_df.iloc[i - 1]['latitude'],
            lon1=route_df.iloc[i - 1]['longitude'],
            lat2=route_df.iloc[i]['latitude'],
            lon2=route_df.iloc[i]['longitude']
        ))

        # #* speed
        time_diff = (route_df.iloc[i].time - route_df.iloc[i - 1].time).seconds
        distances_i = distances[i]

        # Handling division by zero
        if time_diff == 0:
            speed_i = 10  # Assign an appropriate default value
        else:
            speed_i = distances_i / time_diff

        speed.append(speed_i)

    route_df['distance'] = distances
    route_df['cum_distance'] = route_df['distance'].cumsum()/1e3
    route_df['speed'] = speed

    number_of_lifts = lift_checker(route_df)
    if number_of_lifts > 0:
        report.append({
            'file': csv_file_path[11:],
            'n': number_of_lifts,
            'sum_of_n': route_df['lift_path'].sum()/2
        })
        # print('------------------------------------------------------------------')
        # print(
        #     f"The number of lifts detected on {csv_file_path[11:]} is {number_of_lifts} ")
        # print('------------------------------------------------------------------')

    route_df = route_df.fillna(0)  # replace NANs with zero
    ######
    route_df.to_csv(csv_file_path, index=False)
    return route_df


def convert_all_gpx_to_csv(gpx_dir, csv_dir):
    gpx_files = [filename for filename in os.listdir(
        gpx_dir) if filename.endswith('.gpx')]
    progress_bar = tqdm(total=len(gpx_files), desc="Converting GPX files")
    for filename in gpx_files:
        gpx_file_path = os.path.join(gpx_dir, filename)
        csv_file_path = os.path.join(csv_dir, filename.replace('.gpx', '.csv'))
        gpx_to_csv(gpx_file_path, csv_file_path)
        progress_bar.update(1)
    progress_bar.close()


# Usage
gpx_dir = './data/gpx_train/'
csv_dir = './data/csv_train/'
convert_all_gpx_to_csv(gpx_dir, csv_dir)
print('Converting is finished.')


report_df = pd.DataFrame(report)
report_df.to_csv('./data/report.csv', index=True)
