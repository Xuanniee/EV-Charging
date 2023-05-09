import requests
import csv
import json

url = "https://api.plugshare.com/api/v3/locations/"

querystring = {
    # define a bounding box around Singapore
    "bounds": "1.14,103.55,1.42,104.05",
    # include operator information
    "show_networks": "true", 
    # include power rating information
    "show_evse_power": "true",
    # include charge point count information 
    "show_evse_count": "true" 
}

response = requests.request("GET", url, params=querystring)

data = json.loads(response.text)

# create a new CSV file and write the headers
with open("ev_chargers.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Location", "Operator", "Power (kW)", "Charge Points", "Latitude", "Longitude"])

    # iterate through the locations and extract the relevant information
    for location in data["locations"]:
        latitude = location["latitude"]
        longitude = location["longitude"]
        name = location["name"]
        operator = location["network_name"]
        power = location["evse"][0]["power"]
        charge_points = location["evse_count"]
        
        # filter for fast chargers with a power rating of 22 kW or higher
        if power >= 22:
            # write the data to the CSV file
            writer.writerow([name, operator, power, charge_points, latitude, longitude])
            
            # print the data to the console
            print(f"Location: {name}")
            print(f"Operator: {operator}")
            print(f"Power: {power} kW")
            print(f"Charge Points: {charge_points}")
            print(f"Latitude: {latitude}")
            print(f"Longitude: {longitude}")
            print("\n")
