from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.uix.floatlayout import FloatLayout


class Tooltip(FloatLayout):
    tooltip_text = StringProperty('')

    def show_tooltip(self, pos):
        """ Calculate the tooltip to properly fit in the screen without spilling out \n
            Add Tooltip widget to Window tree if not present
        """
        tooltip_width = self.ids.tooltip_label.texture_size[0] + 10
        tooltip_height = self.ids.tooltip_label.texture_size[1] + 10
        screen_width, screen_height = Window.size

        # default position (below the mouse, starts from the mouse towards right side)
        tooltip_x = pos[0]  # position on the right side of the mouse
        tooltip_y = pos[1] - tooltip_height - 10  # position below the mouse

        # no spillout on the right side (flip to display towards left side of the mouse)
        if tooltip_x + tooltip_width > screen_width:
            tooltip_x = pos[0] - tooltip_width

        # no spillout on bottom (dlip to display above the mouse)
        if tooltip_y < 0:
            tooltip_y = pos[1] + 10

        self.pos = (tooltip_x, tooltip_y)

        # add widget if there is no widget to Window tree
        if self not in Window.children:
            Window.add_widget(self)

    def hide_tooltip(self):
        """ Remove Tooltip widget from Window tree"""
        Window.remove_widget(self)
