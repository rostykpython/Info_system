import math


def get_geometry_location(json_obj):
    geometry = json_obj['results'][0]['geometry']['location']
    lat = geometry['lat']
    lng = geometry['lng']
    return lat, lng


def to_rad(deg):
    return deg * (math.pi / 180)


def calculate_distance(lt1, lon1, lt2, lon2):
    R = 6371.0
    dlat = to_rad(lt2 - lt1)
    dlon = to_rad(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.sin(dlon / 2) * math.sin(dlon / 2) \
        * math.cos(lt1) * math.cos(lt2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def distance_between_cities(json_obj_shipping, json_obj_delivery):
    lat1, lng1 = get_geometry_location(json_obj_shipping)
    lat2, lng2 = get_geometry_location(json_obj_delivery)

    return calculate_distance(lat1, lng1, lat2, lng2)
