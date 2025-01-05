from kivy.core.window import Window
from kivy.properties import NumericProperty, ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout


class SearchInputBox(BoxLayout):
    counter = NumericProperty(0)
    search_func = ObjectProperty(None)
    search_hint_text = StringProperty('')

    def on_kv_post(self, base_widget):
        if self.search_func:
            self.ids.search_input.bind(text=self.search_func)

    def bind_escape_key(self, focus_val):
        if focus_val:
            Window.bind(on_key_down=self.on_key_down)
        else:
            Window.unbind(on_key_down=self.on_key_down)

    def clear_text(self, *args):
        self.ids.search_input.text = ''

    def on_key_down(self, window, keycode, scancode, modifiers, is_keyboard):
        if keycode == 27:  # 'Escape' key
            self.clear_text()
            return True
