from kivy.properties import ListProperty, StringProperty, NumericProperty, BooleanProperty
from kivy.uix.floatlayout import FloatLayout
from kivy_garden.mapview import MapMarker


class MapUi(FloatLayout):
    lat_long = ListProperty([0, 0])  # [latitude, longitude]
    target_name = StringProperty('')  # map marker name
    min_zoom = NumericProperty(3)  # scroll out limit
    max_zoom = NumericProperty(10)  # scroll in limit
    is_fullscreen = BooleanProperty(False)
    map_size = NumericProperty(0)  # is rectangular, size = (map_size, map_size)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.map_marker = MapMarker()

    def on_lat_long(self, instance, value):
        """ Update the map's position and markers when lat_long changes"""
        self.ids.map_view.remove_widget(self.map_marker)
        self.ids.map_view.center_on(*self.lat_long)
        self.map_marker.lat, self.map_marker.lon = self.lat_long
        self.ids.map_view.add_marker(self.map_marker)

    def on_kv_post(self, base_widget):
        self.ids.map_view.bind(zoom=self.enforce_zoom_limits)
        self.size = self.map_size, self.map_size

    def enforce_zoom_limits(self, instance, value):
        """ Force the zoom level to stay within the min_zoom and max_zoom range """
        if value < self.min_zoom:
            self.ids.map_view.zoom = self.min_zoom
        elif value > self.max_zoom:
            self.ids.map_view.zoom = self.max_zoom

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
