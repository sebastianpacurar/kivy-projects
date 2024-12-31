from kivy.app import App
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen

from backend.countries_project.rest_countries import CountriesApi
from utils import wait_implicitly


class CountriesMainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_leave(self, *args):
        self.ids.screen_manager.current = 'AllCountriesScreen'


class AllCountriesScreen(Screen):
    data = ListProperty([])
    original_data = ListProperty([])
    counter = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()

    def filter_data(self, text):
        """ Filter data based on query and update RecycleView """
        if text:  # filter only if query is not empty
            words = text.strip().lower().split()

            self.data = [
                # match any combination of the query string
                item for item in self.original_data
                if any(item.get('country_name').lower().startswith(word) for word in words) or
                   any(word in item.get('country_name').lower() for word in words)
            ]
        else:  # reset data if text is empty
            self.data = self.original_data

        self.counter = len(self.data)
        self.refresh_recycle_view()

    def on_pre_enter(self):
        if len(self.data) == 0:
            self.fetch_country_names()

    @wait_implicitly(callback=lambda self, countries: self.update_countries_ui_after_fetch(countries))
    def fetch_country_names(self):
        """ Fetch data for all countries names"""
        return CountriesApi().get_country_names_and_flags()

    def update_countries_ui_after_fetch(self, countries):
        self.original_data = [{'country_name': country, 'country_flag': flag} for country, flag in countries.items()]

        self.data = self.original_data.copy()
        self.counter = len(self.data)
        self.refresh_recycle_view()

    def refresh_recycle_view(self):
        self.ids.responsive_grid.ids.rv.data = self.data

    def go_to_country_screen(self, country):
        """ Navigate to CountryScreen and fetch data """
        self.manager.transition.direction = 'left'
        self.manager.current = 'CountryScreen'

        # once the transition starts, fetch the country data
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
        self.ids.common_name.text = 'Loading...'
        self.top_bar.project_name = 'Loading...'

    @wait_implicitly(callback=lambda self, country_data: self.set_country_data(country_data))
    def fetch_country_data(self, country):
        """ Fetch data for a specific country """
        return CountriesApi().get_country_data(country)

    def set_country_data(self, country_data):
        """Set the country data and update the ui."""
        self.country_data = country_data
        self.ids.common_name.text = self.country_data['name']['common']
        self.ids.official_name.text = self.country_data['name']['official']
        self.ids.capital.text = self.country_data['capital'][0]
        self.top_bar.project_name = self.ids.common_name.text
        self.ids.flag.source = self.country_data['flag']

    def go_back(self, *args):
        """Transition back to AllCountriesScreen."""
        self.manager.transition.direction = 'right'
        self.manager.current = 'AllCountriesScreen'


class CountryItem(FloatLayout):
    country_name = StringProperty('')
    country_flag = StringProperty('')

    def update_size(self, *args):
        """ Resize logic as described above """
        scale_factor = 0.5
        container_width = args[0][0]
        container_height = args[0][1]
        texture_width, texture_height = args[1].texture_size

        image_aspect = texture_width / texture_height
        container_aspect = container_width / container_height

        if container_aspect > image_aspect:
            scaled_height = container_height * scale_factor
            scaled_width = scaled_height * image_aspect
        else:
            scaled_width = container_width * scale_factor
            scaled_height = scaled_width / image_aspect

        args[1].size = (scaled_width, scaled_height)
