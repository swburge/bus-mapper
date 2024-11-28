import requests
import json
from datetime import datetime
import re
from collections import OrderedDict
from itertools import islice
import xml.etree.ElementTree as ET
import pprint
import xmltodict


def xml_to_dict(element):
    if len(element) == 0:
        return element.text
    
    result = {}
    
    for child in element:
        child_result = xml_to_dict(child)
        if child.tag in result:
            if not isinstance(result[child.tag], list):
                result[child.tag] = [result[child.tag]]
            result[child.tag].append(child_result)
        else:
            result[child.tag] = child_result
    
    return result


def replace_string_in_element(element, old_string, new_string):
    # If the element has text, replace the old string with the new string
    if element.text and old_string in element.text:
        element.text = element.text.replace(old_string, new_string)
    
    # Recursively call for each child element
    for child in element:
        replace_string_in_element(child, old_string, new_string)

def remove_prefix(element, prefix):

    if element.tag.startswith(prefix):
        element.tag = element.tag[len(prefix):]
    for child in element:
        remove_prefix(child, prefix)

def print_latitudes(element):
    for vehicle_location in element.findall(".//VehicleLocation"):
        latitude = vehicle_location.find("Latitude")
        if latitude is not None:
            print(f"Latitude: {latitude.text}")



def get_vehicle_info(element):
    locations = []
    for vehicle_activity in element.findall(".//VehicleActivity"):
        recorded_at_time = vehicle_activity.find("RecordedAtTime").text
        line_ref = vehicle_activity.find(".//LineRef").text
        longitude = float(vehicle_activity.find(".//VehicleLocation/Longitude").text)
        latitude = float(vehicle_activity.find(".//VehicleLocation/Latitude").text)
        vehicle_ref = vehicle_activity.find(".//VehicleRef").text
        locations.append({
            'service_number': line_ref,
            'recorded_at_time': recorded_at_time,
            'latitude': latitude,
            'longitude': longitude,
            'vehicle_ref': vehicle_ref
        })

        #print(f"Service Number: {line_ref}")
        #print(f"Recorded At: {recorded_at_time}")
        #print(f"Longitude: {longitude}")
        #print(f"Latitude: {latitude}")
        #print("")

    return locations

class getBusLocation:
    def __init__(self,operatorRef): #,operatorRef):
        #self.lineRef = lineRef
        self.operatorRef = operatorRef
    


    def getBusLocation(self):
        api_key = #ADD API KEY HERE
        #lineRef = self.lineRef
        operatorRef = self.operatorRef

        

        base_url = 'https://data.bus-data.dft.gov.uk/api/v1/datafeed/?'
        #request_url = f"{base_url}lineRef={lineRef}&operatorRef={operatorRef}&api_key={api_key}"
        request_url = f"{base_url}operatorRef={operatorRef}&api_key={api_key}"
        print(request_url)
        response = requests.get(request_url)
        
        if response.status_code == 200:

            root = ET.fromstring(response.content)
            prefix =  "{http://www.siri.org.uk/siri}"
            remove_prefix(root, prefix)
            
            locations = get_vehicle_info(root)
           #ßprint(locations)
            


            modified_xml = ET.tostring(root, encoding='unicode')
            #print(modified_xml)
            #print(root.keys())
            #print_element_names(root)
            return locations
 
