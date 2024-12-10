from kivy.properties import StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen

from assets.fonts.material_design.webfont_unicodes import icons


class MdIconsViewerScreen(Screen):
    data = []

    def set_data(self):
        for k, v in icons.items():
            self.data.append({'icon': v, 'icon_name': k})

    def on_kv_post(self, base_widget):
        self.set_data()
        self.ids.responsive_grid.ids.rv.data = self.data


class IconItem(FloatLayout):
    icon = StringProperty('')  # icon unicode
    icon_name = StringProperty('')  # icon name

    def on_icon(self, instance, value):
        self.ids.icon_label.text = value
