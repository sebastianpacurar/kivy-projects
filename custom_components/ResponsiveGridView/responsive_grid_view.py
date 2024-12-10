from kivy.metrics import dp
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout


class ResponsiveGridView(BoxLayout):
    """ Responsive grid layout with dynamic column based on window resize on X-axis
        view_class = the viewclass widget of the RecycleView
        item_spacing = spacing value between grid items
        item_width = size (width, height) of each grid item
    """

    view_class = StringProperty('Label')  # default to Label to prevent on_kv_post error
    item_spacing = NumericProperty(dp(10))  # default spacing between items
    item_width = NumericProperty(dp(100))  # default item size

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # trigger update_grid_columns when size, spacing and item_width
        self.bind(size=self.update_grid_columns)
        self.bind(item_spacing=self.update_grid_columns)
        self.bind(item_width=self.update_grid_columns)

    def update_grid_columns(self, *args):
        """ Update the number of columns in the grid based on the widget's width, item_width, and spacing """
        grid_layout = self.ids.grid_layout

        # calculate the total width for each item including its spacing
        item_and_spacing_width = self.item_width + self.item_spacing

        # calculate the number of columns that fit into the total width
        cols = max(1, int((self.width + self.item_spacing) / item_and_spacing_width))
        grid_layout.cols = cols

        # set RecycleView default_size to item_width property
        grid_layout.default_size = self.item_width, self.item_width

        # recalculate total used space (including both items and the spacing between them)
        total_item_width = cols * self.item_width  # total width taken by items
        total_spacing = (cols - 1) * self.item_spacing  # total space taken by spacing between items
        total_used_space = total_item_width + total_spacing  # total space used by items and spacing

        # calculate the remaining space
        remaining_space = self.width - total_used_space

        if remaining_space > 0:
            # apply padding to left and right sides
            grid_layout.padding = [remaining_space / 2, 0, remaining_space / 2, 0]
        else:
            # reset padding if no remaining space
            grid_layout.padding = [0, 0, 0, 0]
