from grocery_api_client.models import Location


def test_get_location_data(mock_data,
                       locations_service):
    locations = locations_service.get_locations_data(zip_code=12121)
    assert len(locations)
    assert locations[0]['chain'] == 'KROGER'


def test_get_location_details(mock_data,
                              locations_service):
    locations = locations_service.get_locations_data(zip_code=12121)
    location_id = locations[0]['locationId']
    location_details = locations_service.get_location_details_data(location_id=location_id)
    assert location_details['locationId'] == location_id


def test_does_location_exists_returns_true_for_valid_location_id(mock_data,
                                                                locations_service):
    locations = locations_service.get_locations_data(zip_code=12121)
    location_id = locations[0]['locationId']
    assert locations_service.does_location_exist(location_id)


def test_does_location_exists_returns_true_for_invalid_location_id(mock_data,
                                                                   locations_service):
    location_id = 'bogus'
    assert not locations_service.does_location_exist(location_id)


def test_get_chains(mock_data,
                    locations_service):
    chains = locations_service.get_chains_data()
    assert len(chains) == 43
    assert chains[0].get('name')
    assert chains[0].get('divisionNumbers')


def test_get_locations(mock_data,
                       locations_service):
    locations = locations_service.get_locations(zip_code=11111)
    assert len(locations)
    assert all(isinstance(location, Location) for location in locations)


def test_get_location(mock_data,
                      locations_service):
    location = locations_service.get_location(zip_code=11111)
    assert isinstance(location, Location)


def test_get_grocery_store_locations(mock_data,
                                     locations_service):
    locations = locations_service.get_grocery_store_locations(zip_code=11111)
    assert len(locations) == 1
    assert locations[0].departments[0]['departmentId'] == locations_service.DRUG_AND_GENERAL_MERCHANDISE_ID


def test_get_grocery_store_location(mock_data,
                                    locations_service):
    location = locations_service.get_grocery_store_location(zip_code=11111)
    assert location.departments[0]['departmentId'] == locations_service.DRUG_AND_GENERAL_MERCHANDISE_ID
