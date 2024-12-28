from threading import Thread

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen

from backend.countries_project.rest_countries import CountriesApi


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

    def fetch_country_names(self):
        countries = CountriesApi().get_country_names()
        Clock.schedule_once(lambda dt: self.app.show_spinner(.5), 0)
        Clock.schedule_once(lambda dt: self.update_countries_ui_after_fetch(countries), .5)

    def fetch_country_data(self, country):
        self.manager.current = 'CountryScreen'
        country_data = CountriesApi().get_country_data(country)
        Clock.schedule_once(lambda dt: self.app.show_spinner(.5), 0)
        Clock.schedule_once(lambda dt: self.set_country_data(country_data), .5)

    def update_countries_ui_after_fetch(self, countries):
        self.data = [{'text': country, 'on_release': lambda b=country: self.fetch_country_data(b)} for country in countries]
        self.ids.countries_recycle.data = self.data

    def set_country_data(self, country_data):
        self.manager.get_screen('CountryScreen').country_data = country_data


class CountryScreen(Screen):
    def on_enter(self, *args):
        self.ids.title.text = self.country_data['name']['common']
