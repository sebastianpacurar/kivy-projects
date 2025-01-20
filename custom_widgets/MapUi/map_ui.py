import os

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import ListProperty, StringProperty, NumericProperty, BooleanProperty, DictProperty
from kivy.uix.floatlayout import FloatLayout
from kivy_garden.mapview import MapMarkerPopup, MapView
from kivy_garden.mapview.mbtsource import MBTilesMapSource

import utils
from custom_widgets.base_widgets import TextLabel


class MapUi(FloatLayout):
    lat_long = ListProperty([0, 0])  # [latitude, longitude]
    target_name = StringProperty(' ')  # map marker name
    markers = DictProperty({})  # store markers in a list
    is_fullscreen = BooleanProperty(False)
    is_map_displayed = BooleanProperty(False)
    map_size = NumericProperty(0)  # is rectangular, size = (map_size, map_size)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_zoom_set = False
        self.cached_size = None

        # check for any map marker popup mouse hover events
        Clock.schedule_interval(self.handle_marker_popup_display, 1 / 60.0)

    def on_lat_long(self, instance, value):
        """ Update the map's position and markers when lat_long changes"""
        self.smooth_center_map(*self.lat_long)

    def add_ui_marker(self, lat, lon, name):
        """Add a new marker with popup"""
        if name not in self.markers:
            marker = MapMarkerPopup(lat=lat, lon=lon)
            marker.add_widget(MarkerPopupLabel(label_text=name))
            self.markers[name] = marker
            self.map_view.add_marker(self.markers[name])

    def handle_marker_popup_display(self, *args):
        """ Open MapMarkerPopup when mouse is hovering, close otherwise """
        for name, marker in self.markers.items():
            if marker.collide_point(*Window.mouse_pos):
                if not marker.is_open:
                    marker.is_open = True
            else:
                if marker.is_open:
                    marker.is_open = False

    def remove_ui_marker(self, name):
        """ Remove a marker from the map based on its name """
        if name in self.markers:
            marker = self.markers[name]
            del self.markers[name]
            self.map_view.remove_marker(marker)

    def toggle_displayed_markers(self, target_marker, switch_to_target_marker):
        """ Switch between 2 displayed marker containers \n
            ex: All Countries with a set of markers, and Country with its own marker
        """
        if switch_to_target_marker:
            # if True then remove all markers which are in self.markers, and add the selected target marker
            for name in self.markers:
                marker = self.markers[name]
                self.map_view.remove_marker(marker)
            self.map_view.add_marker(target_marker)
        else:
            # if False then remove the selected target marker, and readd all markers from self.markers
            self.map_view.remove_marker(target_marker)
            for name in self.markers:
                marker = self.markers[name]
                self.map_view.add_marker(marker)

    def on_kv_post(self, base_widget):
        self.cached_size = self.map_size, self.map_size
        self.size = [0, 0]
        self.opacity = 0
        self.disabled = True

    def on_is_map_displayed(self, instance, value):
        """ Open or close map through fade animation """
        if value:
            # fade-in animation
            self.disabled = False
            self.size = self.cached_size
            fade_in = Animation(opacity=1, duration=0.3)
            fade_in.start(self)
        else:
            # fade-out animation
            fade_out = Animation(opacity=0, duration=0.3)

            def on_fade_out_complete(*args):
                # disable and remove size upon fade out completion
                self.disabled = True
                self.size = [0, 0]

            fade_out.bind(on_complete=on_fade_out_complete)
            fade_out.start(self)

    def toggle_full_screen(self):
        """ Switch between fullscreen and given size with fade animations """
        self.is_fullscreen = not self.is_fullscreen
        fade_out = Animation(opacity=0, duration=0.25)

        def on_fade_out_complete(*args):
            # update size_hint and size after fade-out completes
            if self.is_fullscreen:
                self.size_hint = (1, 1)
                self.size = (0, 0)
            else:
                self.size_hint = (None, None)
                self.size = self.map_size, self.map_size

            fade_in = Animation(opacity=1, duration=0.15)
            fade_in.start(self)

        fade_out.bind(on_complete=on_fade_out_complete)
        fade_out.start(self)

    # currently unused in favor to smooth_center_map
    def center_map(self, lat, lon):
        """ Manually center the map on given lat/lon """
        self.map_view.center_on(lat, lon)

    def smooth_center_map(self, lat, lon):
        """ Animate the map to smoothly scroll to the latest added marker """
        # define animation steps
        start_lat = self.map_view.lat
        start_lon = self.map_view.lon
        step_count = 100
        duration = .05
        step_time = duration / step_count
        # calculate lat/lon deltas for each step
        delta_lat = (lat - start_lat) / step_count
        delta_lon = (lon - start_lon) / step_count

        def animate_step(step=0):
            # move the map one step closer to the target
            if step < step_count:
                new_lat = start_lat + delta_lat * step
                new_lon = start_lon + delta_lon * step
                self.map_view.center_on(new_lat, new_lon)
                Clock.schedule_once(lambda dt: animate_step(step + 1), step_time)

        animate_step(0)


class MarkerPopupLabel(TextLabel):
    label_text = StringProperty('blank')


class MapUiView(MapView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        mbtiles_path = os.path.join(utils.find_project_root(), 'backend', 'countries_project', 'dbs', 'osm_offline.mbtiles')
        db_source = MBTilesMapSource(mbtiles_path)
        db_source.bounds = (-180.0, -85.0, 180.0, 85.0)  # min_long, min_lat, max_long, max_lat
        db_source.min_zoom = 3
        db_source.max_zoom = 7

        self.map_source = db_source

    def on_touch_up(self, touch):
        """ Override to get rid of animated_diff_scale() from parent which causes zooms when releasing mouse button \n
            Prevents from pinch-like zooming
        """
        if touch.grab_current == self:
            touch.ungrab(self)
            self._touch_count -= 1
            if self._touch_count == 0:
                self._pause = False
            return True
