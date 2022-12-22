import json
import requests
from typing import List, Union
from grocery_api_client.models import Location
from grocery_api_client.services.helpers.constants import KROGER_LOCATIONS_URI, KROGER_CHAINS_URI
from grocery_api_client.services.helpers.helpers import create_location_objects_from_api_response
from grocery_api_client.utils.exc import LocationNotFoundException, SearchRadiusException


class LocationsService:
    """
    Service for getting locations from Kroger API
    """
    DRUG_AND_GENERAL_MERCHANDISE_ID = '23'

    def __init__(self,
                 access_token: str,
                 search_radius_miles: int = 10,):
        self.access_token = access_token
        self.search_radius_miles = self.validate_search_radius_miles(search_radius_miles)

    @staticmethod
    def validate_search_radius_miles(value: int):
        if isinstance(value, int) and value <= 100:
            return value
        else:
            raise SearchRadiusException()

    def get_locations(self,
                      zip_code: int) -> List[Location]:
        locations = self.get_locations_data(zip_code=zip_code)
        if locations:
            return create_location_objects_from_api_response(locations)
        return []

    def get_location(self,
                     zip_code: int) -> Union[Location, None]:
        locations = self.get_locations(zip_code=zip_code)
        return locations[0] if locations else None

    def expand_locations_search(self,
                                zip_code: int,
                                expand_in_miles: int = 10):
        try_count = 0
        locations = []
        while try_count <= 10 and len(locations) == 0 and self.search_radius_miles <= 100:
            locations = self.get_locations(zip_code)
            if not locations:
                self.search_radius_miles += expand_in_miles
                try_count += 1
            else:
                return locations
        if not locations:
            raise LocationNotFoundException(f'No locations were found for your area '
                                            f'with a search radius of {self.search_radius_miles} miles')

    def get_grocery_store_locations(self,
                                    zip_code: int,
                                    expand_locations_search: bool = False,
                                    expand_in_miles: int = 10) -> List[Location]:
        if expand_locations_search:
            locations = self.expand_locations_search(zip_code, expand_in_miles)
        else:
            locations = self.get_locations(zip_code)
        locations_with_grocery_stores = []
        for location in locations:
            if len(location.departments) > 1:
                for department in location.departments:
                    if location.departments and department['departmentId'] == self.DRUG_AND_GENERAL_MERCHANDISE_ID:
                        locations_with_grocery_stores.append(location)
            elif location.departments == 1:
                if location.departments[0]['departmentId'] == self.DRUG_AND_GENERAL_MERCHANDISE_ID:
                    locations_with_grocery_stores.append(location)
        return locations_with_grocery_stores

    def get_grocery_store_location(self,
                                   zip_code: int,
                                   expand_location_search: bool = False,
                                   expand_in_miles: int = 10) -> Union[Location, None]:
        locations = self.get_grocery_store_locations(zip_code=zip_code,
                                                     expand_locations_search=expand_location_search,
                                                     expand_in_miles=expand_in_miles)
        return locations[0] if locations else None

    def get_locations_data(self,
                           zip_code: int) -> [dict]:
        location_url = f"{KROGER_LOCATIONS_URI}?filter.zipCode.near={zip_code}" \
                       f"&filter.radiusInMiles={self.search_radius_miles}"
        resp = requests.get(location_url, headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        })
        locations_data = json.loads(resp.content)
        if not locations_data:
            raise LocationNotFoundException(f'No locations were found for your area. Please select a wider '
                                            f'search radius than {self.search_radius_miles} miles')
        return locations_data['data']

    def get_location_details_data(self,
                                  location_id: str) -> dict:
        location_url = f"{KROGER_LOCATIONS_URI}/{location_id}"

        resp = requests.get(location_url, headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        })
        location_details_data = json.loads(resp.content)

        return location_details_data['data']

    def does_location_exist(self,
                            location_id: str) -> bool:
        location_url = f"{KROGER_LOCATIONS_URI}/{location_id}"

        resp = requests.head(location_url, headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        })

        return resp.status_code == 204

    def get_chains_data(self) -> [dict]:
        resp = requests.get(KROGER_CHAINS_URI, headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        })

        chains_data = json.loads(resp.content)

        return chains_data['data']
