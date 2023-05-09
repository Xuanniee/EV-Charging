import requests
import csv

# Define the API endpoint URL and parameters
# url = "https://api.openchargemap.io/v3/poi/?output=json&countrycode=SG&maxresults=100000"
url = "https://api.openchargemap.io/v3/poi/?output=json&countrycode=SG&maxresults=100000&key=477bed05-ec92-476a-8e9c-81db18f7176e"
headers = {'Accept': 'application/json'}
params = {'compact': 'true', 'verbose': 'false'}
# params = {'compact': 'true', 'verbose': 'false', 'key': '477bed05-ec92-476a-8e9c-81db18f7176e'}

# Send a GET request to the API endpoint
response = requests.get(url, headers=headers, params=params)

# Parse the response data as JSON
data = response.json()

header = ['Latitude', 'Longitude', 'Address', 'Operator', 'Number of Charging Points', 'Power Rating (kW)']
rows = []

for location in data:
    # x = location['AddressInfo'].get('Longitude')
    # y = location['AddressInfo'].get('Latitude')
    latitude = location['AddressInfo'].get('Latitude')
    longitude = location['AddressInfo'].get('Longitude')
    address = location['AddressInfo'].get('AddressLine1')
    operator = location.get('OperatorInfo', {}).get('Title', 'Unknown')
    charging_points = len(location.get('Connections', []))
    power_rating = max([c.get('PowerKW', 0) for c in location.get('Connections', [])])
    rows.append([latitude, longitude, address, operator, charging_points, power_rating])

with open('ev_chargers_sg.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(rows)
