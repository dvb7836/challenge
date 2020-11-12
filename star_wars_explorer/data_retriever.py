import requests
from loguru import logger
from dateutil import parser
import urllib.parse
import posixpath


from star_wars_explorer.models import Person
from star_wars_explorer.data_writer import save_collection, save_to_disk
from challenge.settings import SWAPI_URL


class DataRetriever:
    def __init__(self):
        self.PLANETS_CACHE = dict()
        self._data = list()

    def run(self):
        self.fetch_data()

        filename = save_to_disk(self.data)
        save_collection(filename)

    @property
    def data(self):
        return self._data

    def fetch_data(self, url=urllib.parse.urljoin(SWAPI_URL, "people")):
        response = requests.get(url)

        if response.status_code != requests.codes.ok:
            logger.error("can't get data from API: {}".format(SWAPI_URL))
            raise BaseException()

        response_json = response.json()

        results = self._preprocess_results(response_json.get("results"))

        self._data.extend(results)

        next_page = response_json.get("next")
        if next_page:
            self.fetch_data(next_page)

    def _preprocess_results(self, results):
        persons = list()
        person = Person()
        for result in results:
            result["homeworld"] = self.__get_planet_name(result)
            result["date"] = parser.parse(result.get("edited")).date()

            persons.append(person.dump(result))

        return persons

    def __get_planet_name(self, result):
        homeworld = result.get("homeworld", "")
        planet_id = homeworld.split("/")[-2]

        if planet_id not in self.PLANETS_CACHE:
            homeworld_name = self.__fetch_planet_name_by_id(planet_id)
            self.PLANETS_CACHE[planet_id] = homeworld_name
        else:
            homeworld_name = self.PLANETS_CACHE.get(planet_id)

        return homeworld_name

    @staticmethod
    def __fetch_planet_name_by_id(planet_id):
        url = urllib.parse.urljoin(
            SWAPI_URL, posixpath.join("planets", planet_id))
        response = requests.get(url)

        if response.status_code != requests.codes.ok:
            logger.error("can't get planet name from API: {}".format(url))
            raise BaseException()

        response_json = response.json()

        return response_json.get("name")
