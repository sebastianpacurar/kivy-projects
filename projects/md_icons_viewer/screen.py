from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp, sp, Metrics
from kivy.properties import StringProperty, ListProperty, NumericProperty, BooleanProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from assets.fonts.material_design.webfont_unicodes import icons
from custom_widgets.Tooltip.tooltip import Tooltip


class MdIconsViewerScreen(Screen):
    data = ListProperty([])
    original_data = ListProperty([])  # unfiltered complete data
    filtered_data = ListProperty([])  # data subset based on toggle buttons
    counter = NumericProperty(0)  # count of currently filtered options
    is_compact = BooleanProperty(False)  # used to switch between small icons and large icons
    app = App().get_running_app()

    def on_leave(self, *args):
        """ Make sure compact is reset to False when leaving screen"""
        if self.is_compact:
            # toggle grid to extended to prevent tooltip from being displayed on other screens
            self.toggle_grid_display_size()

    def set_data(self):
        self.original_data = [{'icon': v, 'icon_name': k, 'is_name_displayed': not self.is_compact} for k, v in icons.items()]
        self.filtered_data = self.original_data.copy()  # start with all items
        self.data = self.filtered_data.copy()
        self.counter = len(self.data)

    def on_kv_post(self, base_widget):
        self.app = App.get_running_app()
        top_bar = self.ids.top_bar
        top_bar.add_right_button(icon=self.app.get_icon('grid'), text='Small', on_release=self.toggle_grid_display_size)
        self.set_data()
        self.ids.responsive_grid.ids.rv.data = self.data
        self.ids.responsive_grid.ids.rv.bind(on_scroll_start=self.clear_tooltips, on_scroll_stop=self.clear_tooltips)

    def clear_tooltips(self, *args):
        for widget in self.ids.responsive_grid.ids.rv.children[0].children:
            if isinstance(widget, IconItem):
                widget.tooltip.hide_tooltip()

    def set_filter_selection(self, instance, value):
        """ Update the filtered_data based on toggle button selection """
        self.clear_tooltips()
        query = self.ids.search_box.ids.search_input.text.strip().lower()
        if instance.btn_text == 'All':
            self.filtered_data = self.original_data.copy()
        elif instance.btn_text == 'Filled':
            self.filtered_data = [item for item in self.original_data if 'outline' not in item['icon_name'].lower()]
        elif instance.btn_text == 'Outlined':
            self.filtered_data = [item for item in self.original_data if 'outline' in item['icon_name'].lower()]
        self.ids.responsive_grid.ids.rv.scroll_y = 1.0  # reset REcycleView scroll to top
        self.filter_data(self.ids.search_box, query)

    def filter_data(self, instance, value):
        """ Filter data based on query and update RecycleView """
        self.clear_tooltips()
        if value:  # filter only if query is not empty
            self.data = [item for item in self.filtered_data if item['icon_name'].lower().startswith(value)]

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

        layout_btn = self.ids.top_bar.ids.button_container_right.children[0]

        if self.is_compact:
            layout_btn.icon = self.app.get_icon('grid-large')
            layout_btn.label_text = 'Large'
            self.ids.responsive_grid.item_width = dp(75)
        else:
            layout_btn.icon = self.app.get_icon('grid')
            layout_btn.label_text = 'Small'
            self.ids.responsive_grid.item_width = dp(200)

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
        """Toggle tooltip when mouse hovers over icon_label, accounting for DPI scaling."""
        try:
            data = self.parent.parent.parent.parent.parent.parent.data  # if this is null then do not continue logic
            pos = args[1]
            # add tooltip widget when mouse hovers over IconItem
            if self.collide_point(*self.to_widget(*pos)):
                self.tooltip.show_tooltip((pos[0] + 10, pos[1] - 10))
            # destroy tooltip widget when not hovering icon-label
            else:
                self.tooltip.hide_tooltip()
        except Exception as e:
            pass
            # do not toggle tooltip when self.parent is not present (this means that this specific IconItem is not attached on the RV as child)
