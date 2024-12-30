from kivy.app import App
from kivy.uix.screenmanager import Screen

from backend.countries_project.rest_countries import CountriesApi
from utils import wait_implicitly


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

    def on_pre_enter(self):
        if len(self.data) == 0:
            self.fetch_country_names()

    @wait_implicitly(callback=lambda self, countries: self.update_countries_ui_after_fetch(countries))
    def fetch_country_names(self):
        """ Fetch data for all countries names"""
        return CountriesApi().get_country_names()

    def update_countries_ui_after_fetch(self, countries):
        self.data = [{'text': country, 'on_release': lambda b=country: self.go_to_country_screen(b)} for country in countries]
        self.ids.countries_recycle.data = self.data

    def go_to_country_screen(self, country):
        """ Navigate to CountryScreen and fetch data """
        self.manager.transition.direction = 'left'
        self.manager.current = 'CountryScreen'

        # Once the transition starts, fetch the country data
        country_screen = self.manager.get_screen('CountryScreen')
        country_screen.fetch_country_data(country)


class CountryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.top_bar = None
        self.country_data = None

    def on_kv_post(self, base_widget):
        self.top_bar = self.ids.top_bar
        self.top_bar.add_left_button(icon=self.app.get_icon('arrow-left-bold-circle-outline'), on_release=self.go_back)

    def on_pre_enter(self, *args):
        self.ids.title.text = 'Loading...'
        self.top_bar.project_name = 'Loading...'

    @wait_implicitly(callback=lambda self, country_data: self.set_country_data(country_data))
    def fetch_country_data(self, country):
        """ Fetch data for a specific country """
        return CountriesApi().get_country_data(country)

    def set_country_data(self, country_data):
        """Set the country data and update the ui."""
        self.country_data = country_data
        self.ids.title.text = self.country_data['name']['common']
        self.top_bar.project_name = self.ids.title.text

    def go_back(self, *args):
        """Transition back to AllCountriesScreen."""
        self.manager.transition.direction = 'right'
        self.manager.current = 'AllCountriesScreen'
