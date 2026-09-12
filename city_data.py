from dataclasses import dataclass


@dataclass
class City:
    id: int
    latitude: float
    longitude: float
    name: str = ""


class CityManager:
    def __init__(self):
        self.cities = []
        self.start_city_id = None

    def add_city(self, latitude, longitude, name=""):
        city = City(
            id=len(self.cities),
            latitude=latitude,
            longitude=longitude,
            name=name
        )

        self.cities.append(city)

        if self.start_city_id is None:
            self.start_city_id = city.id

        return city

    def remove_city(self, city_id):
        if city_id < 0 or city_id >= len(self.cities):
            return False

        self.cities.pop(city_id)

        for index, city in enumerate(self.cities):
            city.id = index

        if not self.cities:
            self.start_city_id = None
        elif self.start_city_id == city_id:
            self.start_city_id = 0
        elif self.start_city_id > city_id:
            self.start_city_id -= 1

        return True

    def clear(self):
        self.cities = []
        self.start_city_id = None

    def get_cities(self):
        return self.cities.copy()

    def get_city(self, city_id):
        if 0 <= city_id < len(self.cities):
            return self.cities[city_id]

        return None

    def set_start_city(self, city_id):
        if self.get_city(city_id) is None:
            return False

        self.start_city_id = city_id
        return True

    def get_start_city(self):
        if self.start_city_id is None:
            return None

        return self.get_city(
            self.start_city_id
        )

    def get_city_count(self):
        return len(self.cities)