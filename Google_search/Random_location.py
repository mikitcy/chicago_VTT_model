import random
import math
import geopandas as gpd
from shapely.geometry import MultiPolygon
from shapely.ops import unary_union

def add_random_location_circle(distance: 0, heading: 0):
    earth_radius = 3958.8

    latitude_distance = distance * math.cos(heading * math.pi / 180)
    earth_circle = 2 * math.pi * earth_radius
    latitude_per_mile = 360 / earth_circle

    latitude_delta = latitude_distance * latitude_per_mile

    longitude_distance = distance * math.sin(heading * math.pi / 180)
    earth_circle = 2 * math.pi * earth_radius
    longitude_per_mile = 360 / earth_circle

    longitude_delta = longitude_distance * longitude_per_mile

    return latitude_delta

print(add_random_location_circle(0.5, 0))

def add_random_location(latitude, longitude):
    latitude = float(latitude)
    longitude = float(longitude)

    degree_range = add_random_location_circle(distance= 1, heading= 0)

    latitude_delta = random.uniform(degree_range * -1, degree_range)
    random_latitude = str(latitude + latitude_delta)

    longitude_delta = random.uniform(degree_range * -1, degree_range)
    random_longitude = str(longitude + longitude_delta)

    new_location = str(f"{random_latitude}, {random_longitude}")

    return new_location

def get_random_location_airportfix(df):

    new_origins = []
    new_destinations = []

    for i in range(len(df)):
        if df.iloc[i]['Origin'] == '41.9827750091, -87.8773053996' or df.iloc[i]['Origin'] == '42.0055597639, -87.901885838' or df.iloc[i]['Origin'] == '41.9790708201, -87.9030396611' or df.iloc[i]['Origin'] == '41.9802643146, -87.913624596':
            new_origin = "41.981127, -87.900876"
        else:
            new_origin = add_random_location(df.iloc[i]['OriginLat'], df.iloc[i]['OriginLong'])
        new_origins.append(new_origin)

        if df.iloc[i]['Destination'] == '41.9827750091, -87.8773053996' or df.iloc[i]['Destination'] == '42.0055598, -87.9018858' or df.iloc[i]['Destination'] == '41.9790708201, -87.9030396611' or df.iloc[i]['Destination'] == '41.9802643146, -87.913624596':
            new_destination = "41.981127, -87.900876"
        else:
            new_destination = add_random_location(df.iloc[i]['DestinationLat'], df.iloc[i]['DestinationLong'])
        new_destinations.append(new_destination)

    df['Random_origin'] = new_origins
    df['Random_destination'] = new_destinations

    return df

#########################
## Random location within a community area

def get_unified_polygon(ca_number):
    gdf = gpd.read_file('Boundaries - Community Areas (current).geojson')

    gdf['area_num_1'] = gdf['area_num_1'].astype(int)
    area = gdf[gdf['area_num_1'] == ca_number]

    # Extract the geometry, unifying if it's a MultiPolygon
    polygon = area.geometry.iloc[0]
    if isinstance(polygon, MultiPolygon):
        polygon = unary_union(polygon.geoms)
    #print("print", polygon)
    return polygon

def get_random_point_in_polygon(polygon):

    minx, miny, maxx, maxy = polygon.bounds
    while True:
        random_point = (random.uniform(miny, maxy), random.uniform(minx, maxx))
        point = gpd.points_from_xy([random_point[1]], [random_point[0]])[0]
        if polygon.contains(point):
            return f"{random_point[0]}, {random_point[1]}"

def get_random_coordinate_sameCA(row):
    ca_number = row['Pickup_CA']
    polygon = get_unified_polygon(ca_number)
    coordinates = get_random_point_in_polygon(polygon)
    return coordinates