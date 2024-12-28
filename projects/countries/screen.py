from threading import Thread

from kivy.app import App
from kivy.uix.screenmanager import Screen

from backend.countries_project.rest_countries import CountriesApi
from utils import explicit_wait


class CountriesMainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_leave(self, *args):
        self.ids.screen_manager.current = 'AllCountriesScreen'


class AllCountriesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.data = []

    def on_pre_enter(self, *args):
        if len(self.data) == 0:
            Thread(target=self.fetch_country_names).start()

    @explicit_wait(wait=0.75, callback=lambda self, countries: self.update_countries_ui_after_fetch(countries))
    def fetch_country_names(self):
        return CountriesApi().get_country_names()

    @explicit_wait(wait=0.75, callback=lambda self, country_data: self.set_country_data(country_data))
    def fetch_country_data(self, country):
        return CountriesApi().get_country_data(country)

    def update_countries_ui_after_fetch(self, countries):
        self.data = [{'text': country, 'on_release': lambda b=country: self.fetch_country_data(b)} for country in countries]
        self.ids.countries_recycle.data = self.data

    def set_country_data(self, country_data):
        self.manager.current = 'CountryScreen'
        self.manager.get_screen('CountryScreen').country_data = country_data


class CountryScreen(Screen):
    def on_enter(self, *args):
        self.ids.title.text = self.country_data['name']['common']
