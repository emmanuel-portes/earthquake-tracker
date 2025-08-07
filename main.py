import os
from datetime import date, datetime

from load_features import filter_features

from dotenv import load_dotenv
from oracledb import connect, Connection


def main(
		url: str = 'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson',
		connection: Connection
	) -> None:

	features: list = filter_features(url)

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
	
	connection = connect(
		user=user, password=password, dsn=dsn, 
		config_dir=config, wallet_location=wlt_loc, wallet_password=wlt_pass 
		)
	
    main(url, connection)

