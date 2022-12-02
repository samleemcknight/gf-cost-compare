import json
import requests
from grocery_api_client.services.helpers.constants import KROGER_LOCATIONS_URI


class LocationsService:

    def __init__(self,
                 access_token: str,
                 search_radius_miles: int = 10,):
        self.location_uri = KROGER_LOCATIONS_URI
        self.access_token = access_token
        self.search_radius_miles = search_radius_miles

    def get_locations(self,
                      zip_code: int):
        location_url = f"{self.location_uri}?filter.zipCode.near={zip_code}" \
                       f"&filter.radiusInMiles={self.search_radius_miles}"
        resp = requests.get(location_url, headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        })
        locations = json.loads(resp.content)
        if not locations:
            raise Exception(f'No locations were found for your area. Please select a wider '
                            f'search radius than {self.search_radius_miles} miles')
        return locations['data']
