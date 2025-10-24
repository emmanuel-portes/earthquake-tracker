import os
import sys
import logging
from datetime import date, datetime, timedelta

import requests
from dotenv import load_dotenv
from psycopg2 import connect, IntegrityError, DatabaseError, Error

MIN_LATITUDE, MAX_LATITUDE = [-90.0, 90.0]
MIN_MAGNITUDE, MAX_MAGNITUDE = [-1.0, 10.0]
MIN_LONGITUDE, MAX_LONGITUDE = [-180.0, 180.0]
MAG_TYPE: list[str] = ['md', 'ml', 'ms', 'mw', 'me', 'mi', 'mb', 'mlg']
      
def time_format(timestamp:int) -> date:
    timestamp = timestamp / 1000
    return datetime.fromtimestamp(timestamp).date()

def fetch_data(url: str) -> list[dict] | dict:
	try:
		response = requests.get(url)
		response.raise_for_status()
		return response.json().get('features')
	except requests.exceptions.HTTPError:
		message: str = f"Request Error: {response.status_code} - {response.reason}"
		logging.error(message)
		sys.exit(1)
	except (requests.URLRequired, requests.exceptions.InvalidURL) as err :
		message: str = f"URL Error: {err}"
		logging.error(message)
		sys.exit(1)
    
def filter_features(url: str) -> list:
	features: list[list] = []
	data: list[dict] = fetch_data(url)

	for feature in data:
		temp: list = []
		featuretype: str = feature.get('type')
		externalID: str = feature.get('id')
		mag: float = feature.get('properties')['mag']
		place: str = feature.get('properties')['place']
		eventDate: date = time_format(feature.get('properties')['time'])
		url: str = feature.get('properties')['url']
		tsunami: bool = bool(feature.get('properties')['tsunami'])
		magtype: str = feature.get('properties')['magType']
		title: str = feature.get('properties')['title']
		longitude, latitude, magnitude = feature.get('geometry')['coordinates']

		if (longitude is None or latitude is None or magnitude is None or
                title is None or url is None or place is None or magtype is None):
			continue

		if ((MIN_LATITUDE > latitude > MAX_LATITUDE) or 
                (MIN_MAGNITUDE > magnitude > MAX_MAGNITUDE) or 
                    (MIN_LONGITUDE > longitude > MAX_LONGITUDE)):
			continue

		if magtype not in MAG_TYPE: 
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

def connectDB():
	database: str = os.getenv('DB_NAME') 
	user: str = os.getenv('DB_USER')
	password: str = os.getenv('DB_PASSWORD')
	host: str = os.getenv('DB_HOST')
	port: str = os.getenv('DB_PORT')

	try:
		connection = connect(
			dbname=database, user=user, password=password, host=host, port=port
			)
		logging.info(f"Database connection established. {connection.server_version}")
		return connection
	except Error as err:
		message: str = f'Database connection error: {err}'
		logging.error(message)
		sys.exit(1)

def insert_features(connection, features: list) -> None:
	try:
		with connection.cursor() as cursor:
			for feature in features:
				try:
					cursor.callproc('fn_insert_features', feature)
					message: str = f"Inserting feature: {feature}"
					logging.info(message)
				except IntegrityError as err:
					message: str = f"Integrity Error: {err}"
					logging.warning(message)
					continue
	except DatabaseError as err:
		message: str = f"Integrity Error: {err}"
		logging.error(message)
	finally:
		connection.commit()
		connection.close()

def main(
		url: str = 'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson'
	) -> None:

	logging.basicConfig(
		filename='app.log', 
		level=logging.INFO,
		format="%(levelname)s: %(asctime)s - %(message)s",
		datefmt="%Y-%m-%d"
		)

	features: list = filter_features(url)
	connection = connectDB()    
	insert_features(connection, features)

if __name__ == '__main__':
	load_dotenv()
	starttime: date = (datetime.now() - timedelta(days=10)).date()
	endtime: date = datetime.now().date()
	url: str = f'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={starttime}&endtime={endtime}'
	
	main(url)

