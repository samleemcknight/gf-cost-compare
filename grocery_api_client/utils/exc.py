class LocationNotFoundException(Exception):
    def __init__(self,
                 message: 'no locations found with given zip code' = None):
        super().__init__(message)
        self.message = message
    pass
