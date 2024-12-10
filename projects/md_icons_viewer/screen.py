from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from assets.fonts.material_design.webfont_unicodes import icons


class MdIconsViewerScreen(Screen):
    data = ListProperty()
    original_data = ListProperty()  # unfiltered complete data
    filtered_data = ListProperty()  # data subset based on toggle buttons
    counter = NumericProperty(0)  # count of currently filtered options

    def set_data(self):
        # convert icons dictionary to a list of dictionaries for RecycleView
        self.original_data = [{'icon': v, 'icon_name': k} for k, v in icons.items()]
        self.filtered_data = self.original_data.copy()  # start with all items
        self.data = self.filtered_data.copy()
        self.counter = len(self.data)

    def on_kv_post(self, base_widget):
        self.set_data()
        self.ids.responsive_grid.ids.rv.data = self.data

    def set_filter_selection(self, toggle_value):
        """ Update the filtered_data based on toggle button selection """
        query = self.ids.filter_input.text.strip().lower()
        if toggle_value == 'All':
            self.filtered_data = self.original_data.copy()
        elif toggle_value == 'Filled':
            self.filtered_data = [item for item in self.original_data if 'outline' not in item['icon_name'].lower()]
        elif toggle_value == 'Outlined':
            self.filtered_data = [item for item in self.original_data if 'outline' in item['icon_name'].lower()]
        self.ids.responsive_grid.ids.rv.scroll_y = 1.0 # reset REcycleView scroll to top
        self.filter_data(query)

    def filter_data(self, text):
        """ Filter data based on query and update RecycleView """
        if text:  # filter only if query is not empty
            self.data = [item for item in self.filtered_data if item['icon_name'].lower().startswith(text)]

        else:  # reset data if text is empty
            self.data = self.filtered_data.copy()
        self.counter = len(self.data)
        self.ids.responsive_grid.ids.rv.data = self.data


class IconItem(FloatLayout):
    icon = StringProperty('')  # icon unicode
    icon_name = StringProperty('')  # icon name

    def on_icon(self, instance, value):
        self.ids.icon_label.text = value
