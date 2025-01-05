from kivy.graphics import Color, Line, RoundedRectangle, Rectangle
from kivy.metrics import dp
from kivy.properties import NumericProperty, ListProperty, ObjectProperty, StringProperty, BooleanProperty
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.boxlayout import BoxLayout


class SegmentedController(BoxLayout):
    toggle_func = ObjectProperty(None)  # callback to execute on SegmentedButton on_state change
    seg_group = StringProperty('')  # toggle group
    button_labels = ListProperty([])  # toggle buttons text
    controller_height = NumericProperty(dp(30))

    def on_button_labels(self, *args):
        for i, text in enumerate(self.button_labels):
            segmented_btn = SegmentedButton(
                is_first=i == 0,
                is_last=i == len(self.button_labels) - 1,
                btn_text=text,
                option_index=i,
                group=self.seg_group,
                toggle_func=self.toggle_func,
                state='down' if i == 0 else 'normal',
            )

            self.add_widget(segmented_btn)


class SegmentedButton(ToggleButtonBehavior, BoxLayout):
    is_first = BooleanProperty(False)
    is_last = BooleanProperty(False)
    btn_text = StringProperty('')
    toggle_func = ObjectProperty(None)
    option_index = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rect = None

    def on_state(self, instance, value):
        self.disabled = True if value == 'down' else False
        self.update_canvas()
        self.toggle_func(instance, value)  # execute the parent callback

    def on_size(self, instance, value):
        # Update the canvas whenever the button size changes
        self.update_canvas()

    def on_pos(self, instance, value):
        # Update the canvas whenever the button position changes
        self.update_canvas()

    def update_canvas(self):
        if not self.canvas:
            return  # prevent first time call crash
        padding = dp(2)
        line_width = dp(2)
        corner_radius = dp(10)  # radius for round corners
        self.canvas.before.clear()

        with self.canvas.before:
            Color(0.00823, 0.59843, 0.54355, 1)
            # write the outlines
            if self.is_first:  # left curved side
                Line(
                    rounded_rectangle=(
                        self.x + padding,
                        self.y + padding,
                        self.width - 2 * padding,
                        self.height - 2 * padding,
                        corner_radius, 0, 0, corner_radius  # left curved side
                    ),
                    width=line_width
                )

            elif self.is_last:
                Line(
                    rounded_rectangle=(
                        self.x + padding,
                        self.y + padding,
                        self.width - 2 * padding,
                        self.height - 2 * padding,
                        0, corner_radius, corner_radius, 0  # right curved side
                    ),
                    width=line_width
                )

            else:  # middle button
                Line(
                    rectangle=(
                        self.x + padding,
                        self.y + padding,
                        self.width - 2 * padding,
                        self.height - 2 * padding
                    ),
                    width=line_width
                )

            # when active fill the rectangle
            if self.state == 'down':
                if self.is_first:
                    RoundedRectangle(
                        pos=(self.x + padding, self.y + padding),
                        size=(self.width - 2 * padding, self.height - 2 * padding),
                        radius=[corner_radius, 0, 0, corner_radius]  # left curved side
                    )

                elif self.is_last:
                    RoundedRectangle(
                        pos=(self.x + padding, self.y + padding),
                        size=(self.width - 2 * padding, self.height - 2 * padding),
                        radius=[0, corner_radius, corner_radius, 0]  # right curved side
                    )

                else:  # middle button
                    Rectangle(
                        pos=(self.x + padding, self.y + padding),
                        size=(self.width - 2 * padding, self.height - 2 * padding)
                    )
