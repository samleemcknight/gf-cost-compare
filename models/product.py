
class Product:
    def __init__(self,
                 product_id: int = None,
                 price: float = None,
                 description: str = None,
                 size_string: str = None):
        self.product_id = product_id
        self.price = price
        self.description = description
        self.size_string = size_string

    def count(self):
        if self.size_string.find('ct') != -1:
            return int(self.size_string.split('ct')[0].replace(' ', ''))
        else:
            return None

    def size(self):
        if self.size_string.find('ct') != -1:
            return float(self.__determine_size(self.size_string.split('ct')[1].split('/ ')[-1]))
        else:
            return float(self.__determine_size(self.size_string))

    def unit(self):
        if self.size_string.find('ct') != -1:
            return self.__determine_unit(self.size_string)
        else:
            return self.__determine_unit(self.size_string)

    def price_per_unit(self):
        size = self.size()
        if self.count():
            price_per_unit = self.price / (self.count() * size)
        else:
            price_per_unit = self.price / size
        return dict(price_per_unit=price_per_unit,
                    unit=self.unit(),
                    total_price=self.price)

    @staticmethod
    def __determine_unit(value):
        if 'fl oz' in value:
            return 'fl oz'
        elif 'oz' in value:
            return 'oz'
        elif 'lb' in value:
            return 'lb'
        return None

    @staticmethod
    def __determine_size(value):
        if 'fl oz' in value:
            return value.split('fl oz')[0]
        elif 'oz' in value:
            return value.split('oz')[0]
        elif 'lb' in value:
            return value.split('oz')[0]
