
import logging
from datetime import date, datetime, timedelta

import requests

from marshmallow import ValidationError

from earthquake_tracker import app

from app import database

from app.schemas.feature_schema import USGSFeatureSchema

from app.models.features_model import Feature
from sqlalchemy.exc import IntegrityError

def fetch_data(url: str) -> list[dict] | dict:
	try:
		response = requests.get(url)
		response.raise_for_status()
		return response.json().get('features')
	except requests.exceptions.HTTPError:
		message: str = f"Request Error: {response.status_code} - {response.reason}"
		logging.error(message)
	except (requests.URLRequired, requests.exceptions.InvalidURL) as err :
		message: str = f"URL Error: {err}"
		logging.error(message)

def filter_features(data: list[dict]) -> list[dict]:
	features: list[dict] = list()
	for usgs in data:
		try:
			feature = USGSFeatureSchema().load(usgs)
			logging.info(f"feature: {feature["usgs_code"]} - {feature["magnitude"]} - {feature["event_date"]}. processed.")
			features.append(feature)
		except ValidationError as err:
			logging.warning(f"While processing feature: {err.messages}")
			continue
	return features	

def insert_features(features: list[dict]) -> None:
	for feature in features:
		try:
			usgs = Feature(**feature)
			database.session.add(usgs)
		except IntegrityError as err:
			database.session.rollback()
			logging.error(f"Something went wrong while inserting feature. {err}")
			continue
		finally:
			database.session.commit()
		
def main(
		url: str = 'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson'
	) -> None:

	logging.basicConfig(
			filename='app.log', 
			level=logging.INFO,
			format="%(levelname)s: %(asctime)s - %(message)s",
			datefmt="%Y-%m-%d"
		)
	usgs_features: list[dict] = fetch_data(url)
	processed_features: list[dict] = filter_features(usgs_features)
	with app.app_context():
		insert_features(processed_features)

if __name__ == '__main__':
	starttime: date = (datetime.now() - timedelta(days=1)).date()
	endtime: date = datetime.now().date()
	url: str = f'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={starttime}&endtime={endtime}'
	main(url)

