class Location:
    def __init__(self,
                 location_id: int,
                 name: str,
                 chain: str,
                 departments: [],
                 address: dict):
        self.location_id = location_id
        self.name = name
        self.chain = chain
        self.departments = departments
        self.address = address


