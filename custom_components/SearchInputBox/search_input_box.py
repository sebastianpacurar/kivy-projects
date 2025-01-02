from kivy.properties import NumericProperty, ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout


class SearchInputBox(BoxLayout):
    counter = NumericProperty(0)
    search_func = ObjectProperty(None)
    search_hint_text = StringProperty('')

    def on_kv_post(self, base_widget):
        if self.search_func:
            self.ids.search_input.bind(text=self.search_func)

    def clear_text(self, *args):
        self.ids.search_input.text = ''

