# Principles of this script:
# Send a request to https://dataset.api.hub.zamg.ac.at/v1/station/current/tawes-v1-10min/metadata to get all availible stations and parameters
# Send a request to https://dataset.api.hub.zamg.ac.at/v1/station/current/tawes-v1-10min to get some data
# Data example: Station Wien Hohe Warte = 11035 + Temperatur = TL + Luftdruck = P + Windspeed = FFAM 
# Example Data Url = https://dataset.api.hub.zamg.ac.at/v1/station/current/tawes-v1-10min?parameters=TL,P,FFAM&station_ids=11035

import requests
import json
import time

selected_station = ""
selected_parametersinput = ""

def enter_station():

    print("Enter Zamg Station ID to get data from (For a list of availible ones type list):")

    globals()["selected_station"] = input() # To test try 11035

    if globals()["selected_station"] == "list":
        availiblestations = json.loads(requests.get('https://dataset.api.hub.zamg.ac.at/v1/station/current/tawes-v1-10min/metadata').content)["stations"]

        for item in availiblestations:
            time.sleep(0.1)
            print(item["id"] + ": " + item["name"])
        enter_station()

def enter_parameters():
    print("Enter Parameters to get (For a list of availible ones type list, for all parameters type all):")
    selected_parameters_input = ""
    selected_parameters_input = input() # To test try TL,P,FFAM

    # if selected_parameters_input == "list":
    #     availibleparameters = json.loads(requests.get('https://dataset.api.hub.zamg.ac.at/v1/station/current/tawes-v1-10min/metadata').content)["parameters"]
    #     for item in availibleparameters:
    #         print(item["name"] + ": " + item["long_name"])
    #     enter_parameters()

    # if selected_parameters_input == "all":
    #     availibleparameters = json.loads(requests.get('https://dataset.api.hub.zamg.ac.at/v1/station/current/tawes-v1-10min/metadata').content)["parameters"]

    #     selected_parameters_input = ""
    #     for item in availibleparameters:
    #         selected_parameters_input += item["name"] + ","
    #     selected_parameters_input = selected_parameters_input.rstrip(selected_parameters_input[-1])
    #     globals()["selected_parametersinput"] = selected_parameters_input


    if selected_parameters_input == "list":
        availibleparameters = json.loads(requests.get('https://dataset.api.hub.zamg.ac.at/v1/station/current/tawes-v1-10min/metadata').content)["parameters"]
        for item in availibleparameters:
            time.sleep(0.1)
            print(item["name"] + ": " + item["long_name"])
        enter_parameters()
            
    elif selected_parameters_input == "all":
        availibleparameters = json.loads(requests.get('https://dataset.api.hub.zamg.ac.at/v1/station/current/tawes-v1-10min/metadata').content)["parameters"]

        selected_parameters_input = ""
        for item in availibleparameters:
            selected_parameters_input += item["name"] + ","
        selected_parameters_input = selected_parameters_input.rstrip(selected_parameters_input[-1])
        globals()["selected_parametersinput"] = selected_parameters_input
            
    else:
        globals()["selected_parametersinput"] = selected_parameters_input
            

enter_station()

enter_parameters()

selected_parameters = selected_parametersinput.split(",")

tawes_stations = json.loads(requests.get('https://dataset.api.hub.zamg.ac.at/v1/station/current/tawes-v1-10min/metadata').content)["stations"]

stationids = []

for item in tawes_stations:
    stationids.append(str(item["id"]))

if selected_station in stationids:
    print("Found Station " + selected_station)

    requesturl = "https://dataset.api.hub.zamg.ac.at/v1/station/current/tawes-v1-10min?parameters=" + selected_parametersinput +"&station_ids=" + selected_station

    stationweather = json.loads(requests.get(requesturl).content)["features"][0]["properties"]["parameters"]

    for item in selected_parameters:
        time.sleep(0.1)
        print(str(stationweather[item]["name"]) + ": " + str(stationweather[item]["data"][0]) + str(stationweather[item]["unit"]))

else:
    
    print("Can't find Station " + selected_station)