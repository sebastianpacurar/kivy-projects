from kivy.uix.boxlayout import BoxLayout

from custom_components.IconButton.icon_button import IconButton


class PillContainer(BoxLayout):
    def on_kv_post(self, base_widget):
        self.ids.pills_stack.remove_widget(self.ids.test)

    def add_pill(self, icon, on_press, text=''):
        """ Add pill with given name and icon \n
            Bind callback to on_press and remove logic to on_release
        """
        button = IconButton(
            icon=icon,
            label_text=text,
            on_press=on_press,
            on_release=lambda i: self.remove_pill(i),
            pos_hint={'center_y': .5})
        self.ids.pills_stack.add_widget(button)

    # remove the pill when touch up. triggers along with on_release callback
    def remove_pill(self, instance):
        self.ids.pills_stack.remove_widget(instance)
