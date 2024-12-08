from kivy.uix.screenmanager import Screen

from backend.countries_project.rest_countries import CountriesApi


class CountriesMainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api = CountriesApi()
        self.selected_country = None

    def on_leave(self, *args):
        self.ids.screen_manager.current = 'AllCountriesScreen'


class AllCountriesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api = CountriesApi()
        self.data = []

    def on_enter(self, *args):
        for country in self.api.get_country_names():
            self.data.append({'text': country, 'on_release': lambda b=country: self.go_to_country_screen(b)})

    def on_kv_post(self, base_widget):
        self.ids.countries_recycle.data = self.data

    def go_to_country_screen(self, country_name):
        country = self.api.get_country_data(country_name)
        country_screen = self.manager.get_screen('CountryScreen')
        country_screen.country_name = country
        self.manager.current = 'CountryScreen'


class CountryScreen(Screen):
    def on_pre_enter(self, *args):
        self.ids.title.text = self.manager.get_screen('CountryScreen').country_name['name']['common']
