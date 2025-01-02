from kivy.metrics import sp
from kivy.properties import StringProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout

from custom_components.BaseComponents.base_components import TextLabel


class TableView(BoxLayout):
    view_class = StringProperty('TextLabel')
    column_names = ListProperty([])

    def on_column_names(self, instance, value):
        """ Add the column names, and set column headers height based on first child's height """
        for widget in self.ids.columns.children:
            if isinstance(widget, TextLabel):
                self.ids.columns.remove_widget(widget)

        for col in self.column_names:
            self.ids.columns.add_widget(TextLabel(font_size=sp(20), text=col, size_hint=(1, 0)))

        self.ids.columns.height = self.ids.columns.children[0].height
