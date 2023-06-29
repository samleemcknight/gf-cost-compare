class LocationNotFoundException(Exception):
    def __init__(self,
                 message: str = 'no locations found with given zip code'):
        super().__init__(message)
        self.message = message
    pass


class SearchRadiusException(Exception):
    def __init__(self,
                 message: str = 'search radius cannot be over 100'):
        super().__init__(message)
        self.message = message
    pass
