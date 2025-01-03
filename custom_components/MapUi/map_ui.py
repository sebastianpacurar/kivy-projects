from kivy.properties import ListProperty, StringProperty, NumericProperty, BooleanProperty, DictProperty
from kivy.uix.floatlayout import FloatLayout
from kivy_garden.mapview import MapMarker


class MapUi(FloatLayout):
    lat_long = ListProperty([0, 0])  # [latitude, longitude]
    target_name = StringProperty('')  # map marker name
    min_zoom = NumericProperty(3)  # scroll out limit
    max_zoom = NumericProperty(6)  # scroll in limit
    is_fullscreen = BooleanProperty(False)
    is_map_displayed = BooleanProperty(False)
    map_size = NumericProperty(0)  # is rectangular, size = (map_size, map_size)
    markers = DictProperty({})  # store markers in a list

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_zoom_set = False
        self.cached_size = None

    def on_lat_long(self, instance, value):
        """ Update the map's position and markers when lat_long changes"""
        # Update the map center
        self.ids.map_view.center_on(*self.lat_long)

    def add_ui_marker(self, lat, lon, name):
        """ Add a new marker to the map """
        marker = MapMarker(lat=lat, lon=lon)
        if name not in self.markers:
            self.markers[name] = marker
        self.ids.map_view.add_marker(marker)

    def remove_ui_marker(self, name):
        """ Remove a marker from the map based on its name """
        if name in self.markers:
            marker = self.markers[name]
            del self.markers[name]
            self.ids.map_view.remove_marker(marker)

    def on_kv_post(self, base_widget):
        self.cached_size = self.map_size, self.map_size
        self.size = [0, 0]
        self.opacity = 0
        self.disabled = True

    def on_is_map_displayed(self, instance, value):
        self.opacity = int(value)
        self.disabled = not value
        self.size = [0, 0] if not value else self.cached_size
        if not self.is_zoom_set:
            self.ids.map_view.map_source.min_zoom = self.min_zoom
            self.ids.map_view.map_source.max_zoom = self.max_zoom
            self.is_zoom_set = True

    def toggle_full_screen(self):
        """ Switch between fullscreen and given size """
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.size_hint = (1, 1)
            self.size = (0, 0)
        else:
            self.size_hint = (None, None)
            self.size = self.map_size, self.map_size

    def scroll_to_marker(self, *args):
        self.ids.map_view.center_on(*self.lat_long)

    def center_map(self, lat, lon):
        """ Manually center the map on given lat/lon """
        self.ids.map_view.center_on(lat, lon)
