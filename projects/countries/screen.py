from kivy.app import App
from kivy.properties import ListProperty, NumericProperty, StringProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy_garden.mapview import MapMarker

from backend.countries_project.rest_countries import CountriesApi
from utils import wait_implicitly


class CountriesMainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()

    def on_leave(self, *args):
        self.ids.screen_manager.current = 'AllCountriesScreen'

    def on_pre_leave(self, *args):
        self.app.toggle_app_map(False)
        self.ids.screen_manager.get_screen('AllCountriesScreen').close_map()
        self.ids.screen_manager.get_screen('CountryScreen').close_map()


class AllCountriesScreen(Screen):
    data = ListProperty([])
    original_data = ListProperty([])
    pinned_countries = ListProperty([])
    counter = NumericProperty(0)
    is_tabular = BooleanProperty(False)
    is_map_on = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()

    def on_pre_enter(self):
        if len(self.data) == 0:
            self.fetch_country_names()

    def on_kv_post(self, base_widget):
        self.ids.table_view.opacity = 0
        self.ids.table_view.size_hint_y = None
        self.ids.table_view.height = 0

        # toggle buttons
        top_bar = self.ids.top_bar
        top_bar.add_right_button(
            icon=self.app.get_icon('map-search'),
            text='Open Map',
            on_release=self.toggle_map_visibility
        )
        top_bar.add_right_button(
            icon=self.app.get_icon('list-box-outline'),
            text='List',
            on_release=self.toggle_layout
        )

    def add_marker_to_map_and_update_data(self, instance):
        """ Logic to add marker on map, and attach Pill component as pinned """
        container = self.ids.pill_container
        country_name = instance.common_name
        container.add_pill(icon=self.app.get_icon('map-marker-off-outline'), text=country_name, on_press=lambda pill, name=country_name: self.remove_marker_from_map(pill, name))
        self.app.map_ui.add_ui_marker(instance.coords[0], instance.coords[1], instance.common_name)
        self.app.map_ui.center_map(*instance.coords)

        if not self.is_map_on:
            self.is_map_on = True

        for i in self.data:
            for k, v in i.items():
                if k == instance.common_name:
                    v['is_pinned'] = True
        self.refresh_grid_recycle_view()
        self.refresh_table_recycle_view()

    def remove_marker_from_map(self, instance, country_name):
        """ The callback used as on_press event, before executing on_release (deleting pill widget) """
        for i in self.data:
            for k, v in i.items():
                if k == country_name:
                    v['is_pinned'] = False

        self.refresh_grid_recycle_view()
        self.refresh_table_recycle_view()
        self.app.map_ui.remove_ui_marker(country_name)

    def toggle_map_visibility(self, *args):
        self.is_map_on = not self.is_map_on

    def close_map(self):
        self.is_map_on = False
        self.manager.get_screen('CountryScreen').is_map_on = False

    def on_is_map_on(self, instance, value):
        self.app.toggle_app_map(value)
        map_btn = self.ids.top_bar.ids.button_container_right.children[1]
        map_btn.is_red_state = value
        map_btn.icon = self.app.get_icon('map-minus') if value else self.app.get_icon('map-search')
        map_btn.label_text = 'Close Map' if value else 'Open Map'
        self.manager.get_screen('CountryScreen').is_map_on = self.is_map_on

    def toggle_layout(self, *args):
        """ Toggle between table and grid views """
        self.is_tabular = not self.is_tabular

        def update_view(view, show):
            view.opacity = 1 if show else 0
            view.size_hint_y = 1 if show else None
            view.height = self.ids.responsive_grid.height if show else 0

        # update views based on the current layout
        update_view(self.ids.table_view, self.is_tabular)
        update_view(self.ids.responsive_grid, not self.is_tabular)

        # change the toggle button icon
        layout_btn = self.ids.top_bar.ids.button_container_right.children[0]
        layout_btn.icon = self.app.get_icon('grid-large') if self.is_tabular else self.app.get_icon('list-box-outline')
        layout_btn.label_text = 'Grid' if self.is_tabular else 'List'

    def filter_data(self, instance, value):
        """ Filter data based on query and update RecycleView """
        if value:  # filter only if query is not empty
            words = value.strip().lower().split()
            self.data = []
            for i in self.original_data:
                country_name = list(i.keys())[0].lower()
                if ' '.join(words) in country_name:
                    self.data.append(i)

        else:  # reset data if text is empty
            self.data = self.original_data

        # update counter and refresh the RecycleViews
        instance.counter = len(self.data)
        self.refresh_grid_recycle_view()
        self.refresh_table_recycle_view()

    @wait_implicitly(callback=lambda self, countries: self.update_countries_ui_after_fetch(countries))
    def fetch_country_names(self):
        """ Fetch data for all countries names"""
        return CountriesApi().get_countries_data()

    def update_countries_ui_after_fetch(self, countries):
        self.original_data = [{c[0]: {**c[1], 'is_pinned': False}} for c in countries.items()]
        self.data = self.original_data.copy()
        self.counter = len(self.data)
        self.refresh_grid_recycle_view()
        self.refresh_table_recycle_view()

    def refresh_grid_recycle_view(self, *args):
        responsive_grid = self.ids.get('responsive_grid', None)
        country_and_flag_display = [
            {'common_name': k, 'flag': v['flag'], 'coords': v['latlng'], 'is_pinned': v['is_pinned']}
            for i in self.data for (k, v) in i.items()
            if v['is_pinned'] is False  # only include data where is_pinned is False
        ]
        responsive_grid.ids.rv.data = country_and_flag_display

    def refresh_table_recycle_view(self, *args):
        table_view = self.ids.get('table_view', None)
        table_data = [
            {'common_name': k, 'region': v['region'], 'capital': v['capital'],
             'population': v.get('population', 'N/A'), 'coords': v['latlng'], 'is_pinned': v['is_pinned'],
             'row_color': (95, .95, .95, 1) if i % 2 == 0 else (1, 1, 1, 1)}
            for (i, item) in enumerate(self.data) for (k, v) in item.items()
            if v['is_pinned'] is False  # only include data where is_pinned is False
        ]
        table_view.ids.rv.data = table_data

    def go_to_country_screen(self, country):
        """ Navigate to CountryScreen and fetch data """
        self.manager.transition.direction = 'left'
        self.manager.current = 'CountryScreen'

        # once the transition starts, fetch the country data
        country_screen = self.manager.get_screen('CountryScreen')
        country_screen.fetch_country_data(country)


class CountryScreen(Screen):
    is_map_on = BooleanProperty(False)
    map_marker = MapMarker()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.top_bar = None
        self.country_data = None

    def on_kv_post(self, base_widget):
        self.top_bar = self.ids.top_bar
        self.top_bar.add_left_button(icon=self.app.get_icon('arrow-left-bold-circle-outline'), on_release=self.go_back)

        self.top_bar.add_right_button(
            icon=self.app.get_icon('map-minus') if self.is_map_on else self.app.get_icon('map-search'),
            text='Close Map' if self.is_map_on else 'Open Map',
            on_release=self.toggle_map_visibility,
            is_red_state=not self.is_map_on
        )

    def on_pre_enter(self, *args):
        self.ids.common_name.text = 'Loading...'
        self.top_bar.project_name = 'Loading...'
        self.ids.flag.source = 'assets/images/img_transparent.png'

    def on_enter(self, *args):
        map_btn = self.ids.top_bar.ids.button_container_right.children[0]
        map_btn.is_red_state = self.is_map_on

    def on_leave(self, *args):
        self.app.map_ui.target_name = ""

    def on_pre_leave(self, *args):
        self.app.map_ui.toggle_displayed_markers(self.map_marker, switch_to_target_marker=False)

    def toggle_map_visibility(self, *args):
        self.is_map_on = not self.is_map_on

    def close_map(self):
        self.is_map_on = False
        self.manager.get_screen('AllCountriesScreen').is_map_on = False

    def on_is_map_on(self, instance, value):
        self.app.toggle_app_map(value)
        map_btn = self.ids.top_bar.ids.button_container_right.children[0]
        map_btn.is_red_state = value
        map_btn.icon = self.app.get_icon('map-minus') if value else self.app.get_icon('map-search')
        map_btn.label_text = 'Close Map' if value else 'Open Map'
        self.manager.get_screen('AllCountriesScreen').is_map_on = self.is_map_on

    @wait_implicitly(callback=lambda self, country_data: self.set_country_data(country_data))
    def fetch_country_data(self, country):
        """ Fetch data for a specific country """
        return CountriesApi().get_country_data(country)

    def set_country_data(self, country_data):
        """ Set the country data and update the UI, and add map markers """
        self.country_data = country_data
        self.ids.common_name.text = self.country_data['name']['common']
        self.ids.official_name.text = self.country_data['name']['official']

        val = self.country_data.get('capital')
        if isinstance(val, list) and len(val) > 0:
            self.ids.capital.text = ', '.join(val)
        else:
            self.ids.capital.text = 'N/A'

        self.top_bar.project_name = self.ids.common_name.text
        self.ids.flag.source = self.country_data['flag']
        lat, lon = self.country_data['latlng']
        self.app.map_ui.lat_long = (lat, lon)
        self.app.map_ui.target_name = self.country_data['name']['common']
        self.map_marker.lat = lat
        self.map_marker.lon = lon
        self.map_marker.name = country_data['name']['common']

        self.app.map_ui.toggle_displayed_markers(self.map_marker, switch_to_target_marker=True)
        self.app.map_ui.center_map(lat, lon)

    def add_marker_to_map(self, lat, lon):
        """ Add a marker to the map at a specific location """
        self.app.map_ui.add_ui_marker(lat, lon, self.country_data['name']['common'])

    def go_back(self, *args):
        """ Transition back to AllCountriesScreen """
        self.manager.transition.direction = 'right'
        self.manager.current = 'AllCountriesScreen'


class CountryGridCardItem(FloatLayout):
    common_name = StringProperty('')
    flag = StringProperty('')
    coords = ListProperty([])
    is_pinned = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()

    def update_size(self, *args):
        """ Resize logic to scale image based on its aspect ratio to fit proeprly """
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

    def add_marker_to_map(self):
        """ Adds a marker to the map with the given coordinates and country name """
        all_countries_screen = self.parent.parent.parent.parent.parent.manager.get_screen('AllCountriesScreen')
        all_countries_screen.add_marker_to_map_and_update_data(self)


class CountryTableRowItem(BoxLayout):
    common_name = StringProperty('')
    region = StringProperty('')
    capital = StringProperty('')
    population = NumericProperty(0)
    row_color = ListProperty([])
    coords = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()

    def add_marker_to_map(self):
        """ Adds a marker to the map with the given coordinates and country name """
        all_countries_screen = self.parent.parent.parent.parent.parent.manager.get_screen('AllCountriesScreen')
        all_countries_screen.add_marker_to_map_and_update_data(self)
