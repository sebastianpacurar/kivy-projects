import requests


class CountriesApi:
    BASE_URL = 'https://restcountries.com/v3.1'

    def get_countries_data(self, fields=None):
        if fields is None:
            fields = ['name', 'capital', 'capitalInfo', 'region', 'subregion', 'flags', 'population', 'latlng']

        fields_param = ",".join(fields)
        url = f"{self.BASE_URL}/all"
        params = {"fields": fields_param}

        return get_multiple_countries_data(url, params)

    def get_countries_data_based_on_region(self, region):
        url = f"{self.BASE_URL}/region/{region}"
        return get_multiple_countries_data(url)

    def get_country_data(self, country_name):
        url = f'{self.BASE_URL}/name/{country_name}'
        try:
            response = requests.get(url, timeout=30, verify=False)
            response.raise_for_status()
            data = response.json()

            if not data or not isinstance(data, list):
                print(f'No data found for {country_name}.')
                return None

            country_data = data[0]
            result = {
                'name': {
                    'common': country_data.get('name', {}).get('common'),
                    'official': country_data.get('name', {}).get('official'),
                    'native_names': country_data.get('name', {}).get('nativeName'),
                },
                'codes': {
                    'cca2': country_data.get('cca2'),
                    'cca3': country_data.get('cca3'),
                    'ccn3': country_data.get('ccn3'),
                    'cioc': country_data.get('cioc'),
                },
                'tld': country_data.get('tld'),
                'capital': country_data.get('capital'),
                'region': country_data.get('region'),
                'subregion': country_data.get('subregion'),
                'population': country_data.get('population'),
                'languages': country_data.get('languages'),
                'currencies': country_data.get('currencies'),
                'timezones': country_data.get('timezones'),
                'latlng': country_data.get('latlng'),
                'borders': country_data.get('borders'),
                'flag': country_data.get('flags', {}).get('png', 'svg'),
                'coat_of_arms': country_data.get('coatOfArms', {}).get('png', 'svg'),
                'maps': country_data.get('maps'),
                'gini': country_data.get('gini'),
                'postal_code_format': country_data.get('postalCode', {}).get('format'),
                'postal_code_regex': country_data.get('postalCode', {}).get('regex'),
            }

            return result
        except requests.exceptions.RequestException as e:
            print(f'An error occurred: {e}')
            return None


def get_multiple_countries_data(url, params=None):
    try:
        response = requests.get(url, params=params, timeout=30, verify=False)
        response.raise_for_status()
        countries = response.json()

        countries_data = {}

        for country in countries:
            capital = country.get('capital')

            countries_data[country.get('name').get('common')] = {
                'common_name': country.get('name').get('common'),
                'capitalInfo': country.get('latlng'),
                'flag': country.get('flags').get('png', 'svg'),
                'capital': ', '.join(capital) if isinstance(capital, list) and len(capital) > 0 else 'N/A',
                'population': country.get('population'),
                'region': country.get('region'),
                'subregion': country.get('subregion'),
                'latlng': country.get('latlng'),
            }

        return countries_data
    except requests.RequestException as e:
        print(f'Error fetching countries: {e}')
        return {}
