from kivy.properties import ObjectProperty, BooleanProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout

from custom_widgets.base_widgets import PropCachedWidget
from custom_widgets.IconButton.icon_button import IconButton


class PillContainer(BoxLayout, PropCachedWidget):
    pin_all_func = ObjectProperty(None)
    is_pin_all_disabled = BooleanProperty(False)

    unpin_all_func = ObjectProperty(None)
    is_unpin_all_disabled = BooleanProperty(False)

    def on_kv_post(self, base_widget):
        self.ids.pills_stack.remove_widget(self.ids.test)
        super().on_kv_post(base_widget)

    def add_single_pill(self, icon, on_press, text=''):
        """ Add single clickable pill with given name and icon """
        single_pill_button = SinglePillWidget(icon=icon, label_text=text, on_press=on_press, on_release=lambda i: self.remove_pill(i))
        pill_names = [pill.label_text for pill in self.ids.pills_stack.children if isinstance(pill, SinglePillWidget)]
        if not single_pill_button.label_text in pill_names:
            self.ids.pills_stack.add_widget(single_pill_button)

    def add_double_pill(self, icon, on_label_press, on_icon_press, text=''):
        """ Add double event clickable pill with given name and icon """
        double_pill_button = DoublePillWidget(pill_label=text, pill_icon=icon, label_press=on_label_press, icon_press=on_icon_press, icon_release=lambda i: self.remove_pill(i.parent))
        pill_names = [pill.pill_label for pill in self.ids.pills_stack.children if isinstance(pill, DoublePillWidget)]
        if not double_pill_button.pill_label in pill_names:
            self.ids.pills_stack.add_widget(double_pill_button)

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


class SinglePillWidget(IconButton):
    pass


class DoublePillWidget(BoxLayout):
    pill_label = StringProperty('')
    pill_icon = StringProperty('')
    label_press = ObjectProperty(None)
    icon_press = ObjectProperty(None)
    icon_release = ObjectProperty(None)

    def on_kv_post(self, base_widget):
        self.ids.label_button.bind(on_press=self.label_press)
        self.ids.icon_button.bind(on_press=self.icon_press, on_release=self.icon_release)
