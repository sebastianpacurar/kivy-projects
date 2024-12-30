from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton

from functools import partial

class SegmentedController(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 6  # Default number of columns, can be adjusted dynamically

    def add_segmented_buttons(self, buttons_list, change_unit_screen_method):
        """Dynamically add buttons to the SegmentedController."""
        self.cols = len(buttons_list)

        for i, text in enumerate(buttons_list):
            seg_btn = SegmentedButton(
                text=text,
                state='down' if i == 0 else 'normal',
                option_index=i,
            )

            seg_btn.bind(on_state=partial(self.handle_state_change, change_unit_screen_method, seg_btn))

            self.add_widget(seg_btn)

    def handle_state_change(self, change_unit_screen_method, seg_btn, instance, value):
        """Handles the state change and invokes the appropriate method."""
        if value == 'down':
            screen_name = f'{seg_btn.text}Screen'
            change_unit_screen_method(instance, value, screen_name)


class SegmentedButton(ToggleButton):
    option_index = NumericProperty(0)