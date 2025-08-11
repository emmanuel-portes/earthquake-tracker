import os
from datetime import date, datetime

import requests

from dotenv import load_dotenv
from oracledb import connect, Connection

MIN_LATITUDE, MAX_LATITUDE = [-90.0, 90.0]
MIN_MAGNITUDE, MAX_MAGNITUDE = [-1.0, 10.0]
MIN_LONGITUDE, MAX_LONGITUDE = [-180.0, 180.0]

def time_format(timestamp:int) -> date:
    timestamp = timestamp / 1000
    return datetime.fromtimestamp(timestamp).date()

def fetch_data(url: str) -> list[dict] | dict:
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get('features')
    except requests.exceptions.HTTPError:
        return {"message": f"something went wrong: {response.status} - {response.reason}"}
    except (requests.URLRequired, requests.exceptions.InvalidURL) as err :
        return {"message": f"something went wrong: {err}"}
    
def filter_features(url: str) -> list:

    features: list[list] = []
    data: list[dict] | dict = fetch_data(url)

    if data.get('message') is not None:
        return list()

    for feature in data:
        temp: list = []
        featuretype: str = feature.get('type')
        externalID: str = feature.get('id')
        mag: float = feature.get('properties')['mag']
        place: str = feature.get('properties')['place']
        eventDate: date = time_format(feature.get('properties')['time'])
        url: str = feature.get('properties')['url']
        tsunami: bool = feature.get('properties')['tsunami']
        magtype: str = feature.get('properties')['magType']
        title: str = feature.get('properties')['title']
        longitude, latitude, magnitude = feature.get('coordinates') 

        if (longitude is None or latitude is None or magnitude is None or
                title is None or url is None or place is None or magtype is None):
            continue

        if ((MIN_LATITUDE > latitude > MAX_LATITUDE) or 
                (MIN_MAGNITUDE > magnitude > MAX_MAGNITUDE) or 
                    (MIN_LONGITUDE > longitude > MAX_LONGITUDE)):
            continue

        temp.append(featuretype)
        temp.append(externalID)
        temp.append(mag)
        temp.append(place)
        temp.append(eventDate)
        temp.append(url)
        temp.append(tsunami)
        temp.append(magtype)
        temp.append(title)
        temp.append(longitude)
        temp.append(latitude)

        features.append(temp)

    return features	

def main(
		url: str = 'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson',
        connection: Connection = None
	) -> None:

	features: list = filter_features(url)

	if not features:
		SystemExit()

	with connection.cursor() as cursor:
		for feature in features:
			cursor.callproc('insert_features', feature)

if __name__ == '__main__':
	load_dotenv()
	dsn: str = os.getenv('DSN') 
	user: str = os.getenv('DB_USER')
	password: str = os.getenv('DB_PASSWORD')
	wlt_loc: str = os.getenv('DB_WALLET')
	wlt_pass: str = os.getenv('DB_WALLET_PASSWORD')
	config: str = os.getenv('DB_CONFIG')

	endtime: date = datetime.now().date()
	url: str = f'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&endtime={endtime}'
	
	connection: Connection = connect(
		user=user, password=password, dsn=dsn, 
		config_dir=config, wallet_location=wlt_loc, wallet_password=wlt_pass 
		)
	
	main(url, connection)

