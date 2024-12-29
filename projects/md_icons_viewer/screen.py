from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.properties import StringProperty, ListProperty, NumericProperty, BooleanProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from assets.fonts.material_design.webfont_unicodes import icons
from custom_components.Tooltip.tooltip import Tooltip


class MdIconsViewerScreen(Screen):
    data = ListProperty()
    original_data = ListProperty()  # unfiltered complete data
    filtered_data = ListProperty()  # data subset based on toggle buttons
    counter = NumericProperty(0)  # count of currently filtered options
    is_compact = BooleanProperty(False)  # used to switch between small icons and large icons

    def on_leave(self, *args):
        """ Make sure compact is reset to False when leaving screen"""
        if self.is_compact:
            # toggle grid to extended to prevent tooltip from being displayed on other screens
            self.toggle_grid_display_size()

    def set_data(self):
        # Convert icons dictionary to a list of dictionaries for RecycleView
        self.original_data = [{'icon': v, 'icon_name': k, 'is_name_displayed': not self.is_compact} for k, v in icons.items()]
        self.filtered_data = self.original_data.copy()  # Start with all items
        self.data = self.filtered_data.copy()
        self.counter = len(self.data)

    def on_kv_post(self, base_widget):
        top_bar = self.ids.top_bar
        top_bar.add_right_button(icon=App.get_running_app().get_icon('grid'), on_release=self.toggle_grid_display_size)
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
        self.ids.responsive_grid.ids.rv.scroll_y = 1.0  # reset REcycleView scroll to top
        self.filter_data(query)

    def filter_data(self, text):
        """ Filter data based on query and update RecycleView """
        if text:  # filter only if query is not empty
            self.data = [item for item in self.filtered_data if item['icon_name'].lower().startswith(text)]

        else:  # reset data if text is empty
            self.data = self.filtered_data.copy()

        self.counter = len(self.data)
        self.refresh_recycle_view()

    def toggle_grid_display_size(self, *args):
        """ Change layout for IconItem \n
            When is compact, then display small IconItems with tooltip
            When not compact, display large IconItems
            Update all data lists and refresh RV
        """
        self.is_compact = not self.is_compact  # toggle compact

        for lst in [self.data, self.filtered_data, self.original_data]:
            for item in lst:
                item['is_name_displayed'] = not self.is_compact

        if self.is_compact:
            self.ids.responsive_grid.item_width = dp(75)
            self.ids.top_bar.ids.button_container_right.children[0].icon = App.get_running_app().get_icon('grid-large')
        else:
            self.ids.responsive_grid.item_width = dp(200)
            self.ids.top_bar.ids.button_container_right.children[0].icon = App.get_running_app().get_icon('grid')

        self.refresh_recycle_view()

    def refresh_recycle_view(self):
        self.ids.responsive_grid.ids.rv.data = self.data


class IconItem(FloatLayout):
    icon = StringProperty('')  # icon unicode
    icon_name = StringProperty('')  # icon name
    is_name_displayed = BooleanProperty(True)  # start with large grid

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tooltip = Tooltip()

    def on_icon(self, instance, value):
        """ Change icon text to the unicode value of the icon """
        self.ids.icon_label.text = value

    def on_icon_name(self, instance, value):
        """ Update tooltip_text after icon_name receives its value """
        self.tooltip.tooltip_text = value

    def on_is_name_displayed(self, instance, value):
        """ Toggle between expanded and compact view of icons """
        if value:
            # if True, extended view enabled, no tooltip needed
            self.ids.icon_label.pos_hint = {'center_x': 0.5, 'center_y': 0.7}
            self.ids.icon_label.font_size = sp(52)
            self.ids.icon_name.opacity = 1
            Window.unbind(mouse_pos=self.on_mouse_pos_tooltip)  # unbind hover tooltip logic
        else:
            # if False, compact view enabled, tooltip needed
            self.ids.icon_name.opacity = 0
            self.ids.icon_label.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
            self.ids.icon_label.font_size = sp(34)
            Window.bind(mouse_pos=self.on_mouse_pos_tooltip)  # bind hover tooltip logic

    def on_mouse_pos_tooltip(self, *args):
        """ Toggle tooltip when mouse hovers over icon_label"""
        pos = args[1]
        # add tooltip widget when mouse hovers icon-label specifically
        if self.ids.icon_label.collide_point(*self.to_widget(*pos)):
            self.tooltip.show_tooltip((pos[0] + 10, pos[1] - 10))
        # destroy tooltip widget when not hovering icon-label
        else:
            self.tooltip.hide_tooltip()
