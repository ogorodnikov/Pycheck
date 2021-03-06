class Capital:
    _instance = None
    _city_name = None

    def __new__(cls, city_name):
        if cls._instance:
            return cls._instance
        cls._instance = super().__new__(cls)
        cls._city_name = city_name
        return cls._instance

    def name(self):
        return type(self)._city_name


if __name__ == '__main__':
    ukraine_capital_1 = Capital("Kyiv")
    ukraine_capital_2 = Capital("London")
    ukraine_capital_3 = Capital("Marocco")

    assert ukraine_capital_2.name() == "Kyiv"
    assert ukraine_capital_3.name() == "Kyiv"

    assert ukraine_capital_2 is ukraine_capital_1
    assert ukraine_capital_3 is ukraine_capital_1
