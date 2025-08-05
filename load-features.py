from datetime import date, datetime
import requests
import os

def time_format(timestamp:int) -> date:
    timestamp = timestamp / 1000
    return datetime.fromtimestamp(timestamp).date()

def get_data(url: str) -> list[dict]:
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get('features')
    except requests.HTTPError:
        return "something went wrong"
    
def main(url: str = 'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson') -> None:
    features: list[dict] 
    data: list[dict] = get_date(url)



if __name__ == '__main__':
    endtime: date = date.today().date()
    URL: str = f'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&endtime={endtime}'
    main()


#response.json().get('features')[0]['id']