import json
import requests
from grocery_api_client.services.helpers.constants import KROGER_LOCATIONS_URI, KROGER_CHAINS_URI


class LocationsService:

    def __init__(self,
                 access_token: str,
                 search_radius_miles: int = 10,):
        self.access_token = access_token
        self.search_radius_miles = search_radius_miles

    def get_locations(self,
                      zip_code: int) -> [dict]:
        location_url = f"{KROGER_LOCATIONS_URI}?filter.zipCode.near={zip_code}" \
                       f"&filter.radiusInMiles={self.search_radius_miles}"
        resp = requests.get(location_url, headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        })
        locations_data = json.loads(resp.content)
        if not locations_data:
            raise Exception(f'No locations were found for your area. Please select a wider '
                            f'search radius than {self.search_radius_miles} miles')
        return locations_data['data']

    def get_location_details(self,
                             location_id: str) -> dict:
        location_url = f"{KROGER_LOCATIONS_URI}/{location_id}"

        resp = requests.get(location_url, headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        })
        location_details_data = json.loads(resp.content)

        return location_details_data['data']

    def does_location_exist(self,
                            location_id: str):
        location_url = f"{KROGER_LOCATIONS_URI}/{location_id}"

        resp = requests.head(location_url, headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        })

        return resp.status_code == 204

    def get_chains(self) -> [dict]:
        resp = requests.get(KROGER_CHAINS_URI, headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        })

        chains_data = json.loads(resp.content)

        return chains_data['data']
