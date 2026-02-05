from celery import shared_task

from ingestion.ingest_features import insert_features, fetch_data, filter_features

@shared_task(ignore_result=True)
def ingest_into_database(url: str) -> dict:
	usgs_features: list[dict] = fetch_data(url)
	processed_features: list[dict] = filter_features(usgs_features)
	result = insert_features(processed_features)
	return result
	
