from math import radians, cos, sin, asin, sqrt
import random

# float -> float
def get_distance_m(lat1, lon1, lat2, lon2):
    # Radius of Earth in meters
    R = 6371000 
    
    # Convert degrees to radians
    phi1 = radians(lat1)
    phi2 = radians(lat2)
    delta_phi = radians(lat2 - lat1)
    delta_lambda = radians(lon2 - lon1)
    
    # Haversine formula
    a = sin(delta_phi / 2)**2 + cos(phi1) * cos(phi2) * sin(delta_lambda / 2)**2
    c = 2 * asin(sqrt(a))
    
    # Distance in meters
    return R * c

def random_x( x : float ):
    rx = -x + ( 150 * random.random() )
    if rx > 179:
        rx = rx - 5

    if rx < -179:
        rx = rx + 5

    return rx

def random_y( y : float ):
    ry = -y + ( 58 * random.random() )
    if ry > 89:
        ry = ry - 5

    if ry < -89:
        ry = ry + 5

    return ry