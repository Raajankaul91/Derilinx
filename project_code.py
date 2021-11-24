import csv
import json
import time
from pprint import pprint
from pyproj import Transformer
import requests


def get_coordinates():
    per_county_addresses = {}
    result = {}

    for address in all_addresses:

        address_list = address['Address'].split(',')
        address_list = [each_element.strip().lower() for each_element in address_list]

        county = address_list[-1]
        if county.startswith("co."):
            county = county.replace('co.', '').strip()

        if county not in per_county_addresses:
            per_county_addresses = get_per_county_addresses(county)

        closest_address = get_closest_address(per_county_addresses, county, address_list)

        if not closest_address:
            raise Exception("Please check the provided address: {0}".format(address))

        # Getting result directly from .geojson file
        result = get_gps_cordinates_from_geojson(closest_address, result, address)

        # Getting result by conversion using proj
        # result = get_gps_cordinates_using_proj(closest_address, result, address)

    return result


def get_gps_cordinates_using_proj(closest_address, result, address):

    transformer = Transformer.from_crs("EPSG:2157", "EPSG:4326", always_xy=True)
    x, y = transformer.transform(closest_address[0]['properties']['ITM_E'], closest_address[0]['properties']['ITM_N'])
    result[address['Address']] = [y, x]

    return result


def get_gps_cordinates_from_geojson(closest_address, result, address):

    itm_n = closest_address[0]["geometry"]["coordinates"][1]
    itm_w = closest_address[0]["geometry"]["coordinates"][0]
    result[address['Address']] = [itm_n, itm_w]

    return result


def get_per_county_addresses(county):

    per_county_townlands = {county: []}

    for townland in townlands_dataset:
        if townland['properties']['County'].strip().lower() == county:
            per_county_townlands[county].append(townland)

    return per_county_townlands


def get_closest_address(per_county_addresses, county, address_list):

    closest_address = []

    if not per_county_addresses[county]:
        per_county_addresses[county] = townlands_dataset

    for address in per_county_addresses[county]:

        english_name = address['properties']['English_Name'] or ''
        irish_name = address['properties']['English_Name'] or ''
        alternative_name = address['properties']['English_Name'] or ''

        for index in range(0, len(address_list)):

            if english_name.lower() == address_list[index] or \
                    irish_name.lower() == address_list[index] or \
                    alternative_name.lower() == address_list[index]:

                closest_address.append(address)
                break
            else:
                continue

        if closest_address:
            break

    if not closest_address:
        [closest_address.append(address) for address in counties_dataset if
         address['properties']['County'].lower() == county]

    return closest_address


if __name__ == '__main__':

    time1 = time.time()

    townlands_dataset = None

    with open('./addresses_for_task.csv', ) as f1, open('./Counties.geojson', ) as f2:
        all_addresses = list(csv.DictReader(f1))
        counties_dataset = json.load(f2)['features']

    param = {'id': 'townlands-osi-national-placenames-gazetteer3'}
    response = requests.get('https://data.gov.ie/api/3/action/package_show', param)
    results = response.json()

    for item in results['result']['resources']:

        if item['format'].lower() == 'geojson' or item['format'].lower() == 'json':
            response = requests.get(item['url'])
            data_json = json.loads(json.dumps(response.json()))
            townlands_dataset = data_json['features']

    result = get_coordinates()
    pprint(result)
