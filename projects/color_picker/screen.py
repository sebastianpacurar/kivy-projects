from kivy.app import App
from kivy.properties import ListProperty, StringProperty, BooleanProperty, ColorProperty, NumericProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen

from backend.color_picker_project.saved_colors_db_ops import select_all_colors, create_db
from custom_widgets.TableView.table_view import TableViewRow
from custom_widgets.Tooltip.tooltip import Tooltip
from named_rgb_hex import css_4_colors
from utils import convert_str_to_rgb


class ColorPickerScreen(Screen):
    data = ListProperty([])
    db_data = ListProperty([])
    is_tabular = BooleanProperty(True)
    saved_colors_count = NumericProperty(0)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = App.get_running_app()

    def on_kv_post(self, base_widget):
        create_db()
        self.set_data()
        self.set_saved_data()
        self.ids.responsive_grid.ids.rv.data = self.data
        self.ids.table_view.ids.rv.data = self.data

        # start with table
        self.ids.responsive_grid.opacity = 0
        self.ids.responsive_grid.size_hint_y = None
        self.ids.responsive_grid.height = 0

    def on_leave(self, *args):
        if not self.is_tabular:
            self.toggle_layout()

    def set_data(self):
        self.data = [{'name': c['name'], 'rgb': c['rgb'], 'hex': c['hex'], 'is_tabular': self.is_tabular} for c in css_4_colors]

    def set_saved_data(self):
        self.db_data = [{'rgb': convert_str_to_rgb(c[1][1:-1]), 'hex': c[2]} for c in select_all_colors()]
        self.ids.db_table_view.ids.rv.data = self.db_data

    def on_saved_colors_count(self, instance, value):
        self.set_saved_data()

    def clear_tooltips(self, *args):
        for widget in self.ids.responsive_grid.ids.rv.children[0].children:
            if isinstance(widget, ColorCard):
                widget.tooltip.hide_tooltip()

    def toggle_layout(self, *args):
        self.is_tabular = not self.is_tabular

        def update_view(view, show):
            view.opacity = 1 if show else 0
            view.size_hint_y = 1 if show else None
            view.height = self.ids.responsive_grid.height if show else 0

        # update views based on the current layout
        update_view(self.ids.table_view, self.is_tabular)
        update_view(self.ids.responsive_grid, not self.is_tabular)

        # change the toggle button icon
        layout_btn = self.ids.toggle_layout_btn
        layout_btn.icon = self.app.get_icon('grid-large') if self.is_tabular else self.app.get_icon('list-box-outline')
        layout_btn.label_text = 'Grid' if self.is_tabular else 'List'

        for item in self.data:
            item['is_tabular'] = self.is_tabular

        self.refresh_recycle_view()

    def refresh_recycle_view(self):
        grid_rv = self.ids.responsive_grid
        table_rv = self.ids.table_view

        grid_rv.ids.rv.data = self.data
        grid_rv.ids.rv.refresh_from_data()
        grid_rv.do_layout()

        table_rv.ids.rv.data = self.data
        table_rv.ids.rv.refresh_from_data()
        table_rv.do_layout()

        if hasattr(grid_rv, 'scroll_y'):
            grid_rv.scroll_y = 1.0
        if hasattr(table_rv, 'scroll_y'):
            table_rv.scroll_y = 1.0


class ColorCard(FloatLayout):
    name = StringProperty('')
    rgb = ColorProperty([0, 0, 0, 255])
    hex = StringProperty('')
    is_tabular = BooleanProperty(True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tooltip = Tooltip()

    def on_is_tabular(self, instance, value):
        if value:
            self.tooltip.stop_tracking()
        else:
            self.tooltip.start_tracking(self)

    def on_name(self, instance, value):
        self.tooltip.tooltip_text = value

    def on_touch_down(self, touch):
        """ Only trigger the event for this specific ColorCard """
        if self.collide_point(*touch.pos):
            App.get_running_app().copy_to_clipboard(str(self.rgb))
        return super().on_touch_up(touch)


class ColorRowItem(TableViewRow):
    name = StringProperty('')
    rgb = ColorProperty([0, 0, 0, 255])
    hex = StringProperty('')


class SavedColorRowItem(TableViewRow):
    rgb = ColorProperty([255, 255, 255, 255])
    hex = StringProperty('')
