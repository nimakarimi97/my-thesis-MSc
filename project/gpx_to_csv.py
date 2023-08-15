import gpxpy
import gpxpy.gpx
import numpy as np
import haversine as hs
import pandas as pd
import os
import gpxpy
import pandas as pd

report = []


def haversine_distance(lat1, lon1, lat2, lon2) -> float:
    distance = hs.haversine(
        point1=(lat1, lon1),
        point2=(lat2, lon2),
        unit=hs.Unit.METERS
    )
    return np.round(distance, 2)


def add_lift_counter(df):
    counter = 0
    df['counter'] = 0  # ? set the counter column to zero
    for i in range(len(df)):
        # if df['elevation_diff'][i] < 1:
        #     continue
        if df['elevation_diff'][i] > 100:
            counter += 1
            # print(i)
        df.loc[i, 'counter'] = counter

    # print(df['elevation'][i])
    return counter


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

    route_df['elevation_diff'] = route_df['elevation'].diff()

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
        speed.append(distances[i]/time_diff)

    route_df['distance'] = distances
    route_df['speed'] = speed

    route_df['cum_elevation'] = route_df['elevation_diff'].cumsum()
    route_df['cum_distance'] = route_df['distance'].cumsum()/1e3

    counter = add_lift_counter(route_df)
    if counter > 0:
        report.append({
            'file': csv_file_path[11:],
            'n': counter,
        })
        print('------------------------------------------------------------------')
        print(
            f"The number of lifts detected on {csv_file_path[11:]} is {counter} ")
        print('------------------------------------------------------------------')

    route_df = route_df.fillna(0)  # replace NANs with zero
    ######
    route_df.to_csv(csv_file_path, index=False)
    return route_df


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
convert_all_gpx_to_csv(gpx_dir, csv_dir)


# report_df = pd.DataFrame(report)
# report_df.to_csv('./data/report.csv', index=True)
