import requests
 
 
def reverse_geocode(latitude, longitude):
    sensor = 'true'
    base = "http://maps.googleapis.com/maps/api/geocode/json?"
    params = "latlng={lat},{lon}&sensor={sen}".format(
        lat=latitude,
        lon=longitude,
        sen=sensor)
    url = "{base}{params}".format(base=base, params=params)
    response = requests.get(url)
    return response.json()['results']


def get_address(latitude, longitude):
    return reverse_geocode(latitude, longitude)[0]['formatted_address']
