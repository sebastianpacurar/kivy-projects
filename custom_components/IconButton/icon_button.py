from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.properties import StringProperty, ListProperty, BooleanProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label


class IconButton(ButtonBehavior, Label):
    icon = StringProperty('')  # icon unicode
    bg_color = ListProperty([0.00823, 0.59843, 0.54355, 1])  # listener for color changing events
    default_bg_color = [0.00823, 0.59843, 0.54355, 1]
    pressed_bg_color = [0.01176, 0.8549, 0.7765, 1]
    red_state_default_bg_color = [.8, 0, 0, 1]
    red_state_pressed_bg_color = [1, 0, 0, 1]
    disabled_bg_color = [0.6, 0.6, 0.6, 1]
    is_round = BooleanProperty(True)
    is_red_state = BooleanProperty(False)  # change color to red if is_red_state is True

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if touch.button == 'left':
                # if left click, proceed with the button press logic
                return super(IconButton, self).on_touch_down(touch)
            if touch.button == 'right':
                # do nothing if right click
                return False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # make sure no other drawings are made while there is an animation or screen transition
        self.bind(size=self.update_canvas, pos=self.update_canvas)
        self.bind(bg_color=self.update_canvas)  # when bg_color changes, trigger canvas redraw
        self.bind(state=self.on_state, is_red_state=self.on_state)  # bind the state property to the on_state method

    def on_icon(self, instance, value):
        """ Set text to the Unicode value when the icon is assigned """
        self.text = value

    def on_state(self, instance, value):
        """ Set bg_color based on the state of the button and is_red_state """
        # if is_red_state is True, use red background
        if self.is_red_state:
            if value == 'down':  # if button is pressed
                self.bg_color = self.red_state_pressed_bg_color  # set red pressed color
            else:  # if button is in 'normal' state
                self.bg_color = self.red_state_default_bg_color  # set red default color
        # if is_red_state is False, use teal background
        else:
            if value == 'down':  # if button is pressed
                self.bg_color = self.pressed_bg_color  # set pressed color
            else:  # if button is in 'normal' state
                if not self.collide_point(*self.to_window(0, 0)):  # check if mouse is not hovering
                    self.bg_color = self.default_bg_color  # set default teal color
        self.update_canvas()

    def on_disabled(self, instance, value):
        """ Update bg color to greyed out when disabled """
        if value:
            self.bg_color = self.disabled_bg_color
        else:
            self.bg_color = self.default_bg_color

    def update_canvas(self, *args):
        """ Update the background color and rectangle to match a button's behavior """
        self.canvas.before.clear()  # clear existent drawing
        with self.canvas.before:  # redraw with bg_color values
            Color(*self.bg_color)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos) if self.is_round else Rectangle(size=self.size, pos=self.pos)
