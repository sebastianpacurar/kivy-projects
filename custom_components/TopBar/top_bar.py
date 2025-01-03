from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout

from custom_components.IconButton.icon_button import IconButton


class TopBar(BoxLayout):
    project_name = StringProperty('')

    def add_right_button(self, icon, on_release, text=''):
        """ Add icon based buttons to the right side of the top bar title """
        button = IconButton(icon=icon, label_text=text, on_release=on_release, pos_hint={'center_y': .5})
        self.ids.button_container_right.add_widget(button)

    def add_left_button(self, icon, on_release, text=''):
        """ Add icon based buttons to the left side of the top bar title """
        button = IconButton(icon=icon, label_text=text, on_release=on_release, pos_hint={'center_y': .5})
        self.ids.button_container_left.add_widget(button)
