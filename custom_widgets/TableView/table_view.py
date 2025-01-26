from kivy.metrics import sp, dp
from kivy.properties import StringProperty, NumericProperty, ObjectProperty, ListProperty, ColorProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

from custom_widgets.base_widgets import BaseLabel


class TableView(BoxLayout):
    view_class = StringProperty('TableViewRow')
    column_names = ListProperty([])
    column_widths = ListProperty([])
    data_counter = NumericProperty(0)

    def on_column_names(self, instance, value):
        """ Add column headers and set their width responsively or statically"""
        # clear existing dummy column headers
        self.ids.columns.clear_widgets()

        # create new column headers with the specified column widths
        for i, col_name in enumerate(self.column_names):
            col_width = self.column_widths[i] if self.column_widths[i] > 0 else 1
            label = BaseLabel(
                font_size=sp(20),
                text=col_name,
                size_hint_y=0,
            )

            label.height = dp(30)
            if self.column_widths[i]:
                label.size_hint_x = None  # lock resizing
                label.width = col_width  # set width
            else:
                label.size_hint_x = 1  # allow resizing
                label.width = 0  # reset width
            self.ids.columns.add_widget(label)

        # Set header height dynamically based on content
        if self.ids.columns.children:
            self.ids.columns.height = 60


# table data cell
class TableData(Widget):
    pass


# table row
class TableViewRow(BoxLayout):
    pass


# table text data cell
class TableViewText(BoxLayout, TableData):
    text_val = StringProperty('')


# table button data cell
class TableViewButton(BoxLayout, TableData):
    text_val = StringProperty('')
    btn_action = ObjectProperty(None)

    def on_kv_post(self, base_widget):
        if self.btn_action:
            self.ids.base_btn.bind(on_release=self.btn_action)


# table icon button data cell
class TableViewIconButton(BoxLayout, TableData):
    icon = StringProperty('')
    btn_action = ObjectProperty(None)

    def on_kv_post(self, base_widget):
        if self.btn_action:
            self.ids.icon_btn.bind(on_release=self.btn_action)


# exceptional case to use a colored box - used for ColorPickerWidget
class TableViewColor(BoxLayout, TableData):
    color_val = ColorProperty([0, 0, 0, 1])

    def on_color_val(self, instance, value):
        self.canvas.ask_update()
