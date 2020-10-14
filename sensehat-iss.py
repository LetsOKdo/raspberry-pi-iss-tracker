from sense_hat import SenseHat
import time
import threading
import requests
from math import sin, cos, atan2, degrees, radians
from haversine import haversine

home = (51.7836, -1.4854)  # Set home co-ordinates as degrees N, degrees E
out_of_sight = 2000  # Trigger distances in km
getting_closer = 800

red = (255, 0, 0)  # RGB colours
orange = (255, 165, 0)
b = (0, 0, 0)  # Off
f = green = (0, 255, 0)
url = "http://api.open-notify.org/iss-now.json"  # IIS Json location service
earths_radius = 6371.0088  # Earths radius in Kilometres

two_by_two = [
    b, b, b, b, b, b, b, b,
    b, b, b, b, b, b, b, b,
    b, b, b, b, b, b, b, b,
    b, b, b, f, f, b, b, b,
    b, b, b, f, f, b, b, b,
    b, b, b, b, b, b, b, b,
    b, b, b, b, b, b, b, b,
    b, b, b, b, b, b, b, b
]

six_by_six = [
    b, b, b, b, b, b, b, b,
    b, f, f, f, f, f, f, b,
    b, f, b, b, b, b, f, b,
    b, f, b, b, b, b, f, b,
    b, f, b, b, b, b, f, b,
    b, f, b, b, b, b, f, b,
    b, f, f, f, f, f, f, b,
    b, b, b, b, b, b, b, b
]


def get_iss_coords():
    """Get latest IIS latitude and longitude as tuple
       Don't query server more than every 5 seconds"""
    global iss
    while True:
        try:
            coords = requests.get(url).json()  # Json response
            iss = (float(coords['iss_position']['latitude']),
                   float(coords['iss_position']['longitude']))
        except:
            pass
        time.sleep(5)


def compass_bearing(coordA, coordB):
    """Return bearing between two co-ordinates (Degrees)"""
    latA, latB, long_diff = (radians(coordA[0]),
                            radians(coordB[0]),
                            radians(coordB[1] - coordA[1]))
    x, y = (sin(long_diff) * cos(latB),
            cos(latA) * sin(latB) - (sin(latA) * cos(latB) * cos(long_diff)))
    return round((degrees(atan2(x, y)) + 360) % 360)


def compass_quadrant(bearing):
    """Return a compass quadrant from bearing"""
    if bearing < 90:
        quad = 'NE'
    elif bearing < 180:
        quad = 'SE'
    elif bearing < 270:
        quad = 'SW'
    else:
        quad = 'NW'
    return quad


def pulse_matrix(colour, delay=1):
    for matrix in two_by_two, six_by_six:
        sense.set_pixels(matrix)
        time.sleep(delay)


def update_display():
    distance = haversine(home, iss)  # Haversine dist between two points (km)
    bearing = compass_bearing(home, iss)
    quadrant = compass_quadrant(bearing)
    print(f'Distance from home: {round(distance)} km')
    print('Co-ordinates:', iss)
    print(f'Bearing: {bearing} degrees')
    print('Quadrant:', quadrant)
    if distance > out_of_sight:
        pulse_matrix(green)
    elif distance > getting_closer:
        sense.show_message(quadrant, text_colour=orange, scroll_speed=0.2)
    else:  # Red alert - in view!!
        sense.show_message(quadrant, text_colour=red, scroll_speed=0.2)

iss = (0, 0)  # ISS co-ordinates
t = threading.Thread(target=get_iss_coords)  # Get ISS position concurrently
t.daemon = True
t.start()
sense = SenseHat()
sense.set_rotation(180)  # Rotate display
try:
    while True:
        update_display()
finally:
    sense.clear()  # Turn lights off when leaving!
