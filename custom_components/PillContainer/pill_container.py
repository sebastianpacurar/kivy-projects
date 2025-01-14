from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout

from custom_components.BaseComponents.base_components import PropCachedWidget
from custom_components.IconButton.icon_button import IconButton


class PillContainer(BoxLayout, PropCachedWidget):
    pin_all_func = ObjectProperty(None)
    is_pin_all_disabled = BooleanProperty(False)

    unpin_all_func = ObjectProperty(None)
    is_unpin_all_disabled = BooleanProperty(False)

    def on_kv_post(self, base_widget):
        self.ids.pills_stack.remove_widget(self.ids.test)
        super().on_kv_post(base_widget)

    def add_pill(self, icon, on_press, text=''):
        """ Add pill with given name and icon \n
            Bind callback to on_press and remove logic to on_release
        """
        button = PillWidget(icon=icon, label_text=text, on_press=on_press, on_release=lambda i: self.remove_pill(i))
        self.ids.pills_stack.add_widget(button)

    def on_pin_all_func(self, *args):
        self.ids.pin_all_button.bind(on_release=lambda i, v=None: self.pin_all_func(i, v))

    def on_unpin_all_func(self, *args):
        self.ids.unpin_all_button.bind(on_release=lambda i, v=None: self.unpin_all_func(i, v))

    # remove the pill when touch up. triggers along with on_release callback
    def remove_pill(self, instance):
        self.ids.pills_stack.remove_widget(instance)

    def hide_widgets(self):
        # hack to update when self.minimum_height is calculated
        self.cached_props.update({'size': {'displayed': tuple(self.size), 'hidden': (0, 0)}})
        self.recursive_hide(self)
        super().hide_widget(self.cached_props)

    def reveal_widgets(self):
        self.recursive_reveal(self)
        super().reveal_widget()


class PillWidget(IconButton):
    pass
