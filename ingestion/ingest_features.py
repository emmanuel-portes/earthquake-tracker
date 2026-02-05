
import requests

import logging

from app import database
from app.schemas.feature_schema import USGSFeatureSchema
from app.models.features_model import Feature

from sqlalchemy.dialects.postgresql import insert

from marshmallow import ValidationError

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
	statement = insert(Feature).values(features)
	statement = statement.on_conflict_do_nothing(index_elements=['usgs_code'])
	result = database.session.execute(statement)
	database.session.commit()

	return {
		"inserted": result.rowcount,
		"total": len(features),
		"skipped": len(features) - result.rowcount
	}


