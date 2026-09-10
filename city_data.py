from dataclasses import dataclass


@dataclass
class City:
    id: int
    name: str
    district: str
    latitude: float
    longitude: float
    x: int
    y: int


CITIES = [
    City(1, "Ben Thanh Market", "District 1", 10.7720, 106.6980, 350, 390),
    City(2, "Independence Palace", "District 1", 10.7771, 106.6953, 390, 320),
    City(3, "Notre Dame Cathedral", "District 1", 10.7798, 106.6992, 430, 270),
    City(4, "Central Post Office", "District 1", 10.7803, 106.6997, 450, 250),
    City(5, "Nguyen Hue Walking Street", "District 1", 10.7741, 106.7034, 520, 360),
    City(6, "Bitexco Financial Tower", "District 1", 10.7718, 106.7042, 560, 410),
    City(7, "Bach Dang Wharf", "District 1", 10.7738, 106.7065, 610, 350),
    City(8, "Saigon Opera House", "District 1", 10.7764, 106.7028, 530, 310),
    City(9, "War Remnants Museum", "District 3", 10.7795, 106.6920, 330, 260),
    City(10, "Tao Dan Park", "District 1", 10.7750, 106.6935, 310, 340),
    City(11, "Museum of Fine Arts", "District 1", 10.7695, 106.6993, 390, 450),
    City(12, "Landmark 81", "Binh Thanh", 10.7949, 106.7218, 760, 120),
]


def get_all_cities():
    return CITIES


def get_city_names():
    return [city.name for city in CITIES]


def get_city_by_name(name):
    for city in CITIES:
        if city.name == name:
            return city
    return None


def get_city_by_id(city_id):
    for city in CITIES:
        if city.id == city_id:
            return city
    return None