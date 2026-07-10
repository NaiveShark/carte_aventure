import math
import random

# float -> float
def dist( x1, y1, x2, y2 ):
    return math.sqrt( abs(x2-x1)**2 + abs( y2-y1 )**2 )

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