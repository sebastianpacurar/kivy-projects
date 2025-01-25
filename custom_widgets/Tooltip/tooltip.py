from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock


class Tooltip(FloatLayout):
    tooltip_text = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.target_widget = None  # widget which will render the tooltip
        self.tooltip_scheduled_event = None  # the actual clocked event, in this case a scheduled interval

    def show_tooltip(self, pos):
        """ Calculate the tooltip to properly fit in the screen without spilling out \n
            Add Tooltip widget to Window tree if not present
        """
        tooltip_width = self.ids.tooltip_label.texture_size[0] + 10
        tooltip_height = self.ids.tooltip_label.texture_size[1] + 10
        screen_width, screen_height = Window.size

        # default position (below the mouse, starts from the mouse towards right side)
        tooltip_x = pos[0]  # Position on the right side of the mouse
        tooltip_y = pos[1] - tooltip_height - 10  # Position below the mouse

        # no spillout on the right side (flip to display towards left side of the mouse)
        if tooltip_x + tooltip_width > screen_width:
            tooltip_x = pos[0] - tooltip_width

        # no spillout on bottom (dlip to display above the mouse)
        if tooltip_y < 0:
            tooltip_y = pos[1] + 10

        # update position only if different from tooltip pos
        if self.pos != (tooltip_x, tooltip_y):
            self.pos = (tooltip_x, tooltip_y)

        # add widget if there is no widget to Window tree
        if self not in Window.children:
            Window.add_widget(self)

    def hide_tooltip(self):
        """ Remove Tooltip widget from Window tree """
        if self in Window.children:
            Window.remove_widget(self)

    def start_tracking(self, target_widget):
        """ Start tracking a target widget for tooltip display \n
            This should be used as a trigger for when the tooltip should be tracked under certain conditions
        """
        self.target_widget = target_widget
        if self.tooltip_scheduled_event is None:
            self.tooltip_scheduled_event = Clock.schedule_interval(
                lambda dt: self.check_tooltip_periodically(dt, target_widget.parent), 1 / 60
            )

    def stop_tracking(self):
        """ Stop tracking the target widget for tooltip display \n
            This should be used as a trigger for when the start_tracking() condition is not respected anymore
        """
        if self.tooltip_scheduled_event:
            self.tooltip_scheduled_event.cancel()
            self.tooltip_scheduled_event = None
        self.target_widget = None
        self.hide_tooltip()

    def check_tooltip_periodically(self, dt, parent=None):
        """ Check if the tooltip should be shown, hidden, or repositioned """
        if not self.target_widget:
            return

        if parent is not None:  # using this in case the widget is part of a RV data, and is not currently visible in the viewport
            pos = Window.mouse_pos  # get the current mouse position on Window
            if self.target_widget.collide_point(*self.target_widget.to_widget(*pos)):
                # show tooltip if mouse overlaps the target widget
                self.show_tooltip((pos[0] + 10, pos[1] - 10))
            else:
                # hide tooltip if mouse is not over the target widget
                self.hide_tooltip()
        else:
            self.hide_tooltip()