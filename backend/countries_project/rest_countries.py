import requests


class CountriesApi:
    BASE_URL = 'https://restcountries.com/v3.1'

    def get_country_names(self):
        url = f'{self.BASE_URL}/all?fields=name'
        try:
            response = requests.get(url, timeout=30, verify=False)
            response.raise_for_status()
            countries = response.json()

            return [country['name']['common'] for country in countries]
        except requests.RequestException as e:
            print(f"Error fetching countries: {e}")
            return []

    def get_country_data(self, country_name):
        url = f'{self.BASE_URL}/name/{country_name}'
        try:
            response = requests.get(url, timeout=30, verify=False)
            response.raise_for_status()
            data = response.json()

            if not data or not isinstance(data, list):
                print(f"No data found for {country_name}.")
                return None

            country_data = data[0]
            result = {
                "name": {
                    "common": country_data.get("name", {}).get("common"),
                    "official": country_data.get("name", {}).get("official"),
                    "native_names": country_data.get("name", {}).get("nativeName"),
                },
                "codes": {
                    "cca2": country_data.get("cca2"),
                    "cca3": country_data.get("cca3"),
                    "cioc": country_data.get("cioc"),
                },
                "tld": country_data.get("tld"),
                "capital": country_data.get("capital"),
                "region": country_data.get("region"),
                "subregion": country_data.get("subregion"),
                "population": country_data.get("population"),
                "languages": country_data.get("languages"),
                "currencies": country_data.get("currencies"),
                "timezones": country_data.get("timezones"),
                "latlng": country_data.get("latlng"),
                "borders": country_data.get("borders"),
                "flag": country_data.get("flags", {}).get("png"),
                "coat_of_arms": country_data.get("coatOfArms", {}).get("png"),
                "maps": country_data.get("maps"),
                "gini": country_data.get("gini"),
                "postal_code_format": country_data.get("postalCode", {}).get("format"),
                "postal_code_regex": country_data.get("postalCode", {}).get("regex"),
            }

            return result
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None
