from kivy.graphics import Color, RoundedRectangle
from kivy.properties import StringProperty, ListProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label


class IconButton(ButtonBehavior, Label):
    icon = StringProperty('')  # icon unicode
    bg_color = ListProperty([0.00823, 0.59843, 0.54355, 1])  # listener for color changing events
    default_bg_color = [0.00823, 0.59843, 0.54355, 1]
    pressed_bg_color = [0.01176, 0.8549, 0.7765, 1]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # make sure no other drawings are made while there is an animation or screen transition
        self.bind(size=self.update_canvas, pos=self.update_canvas)
        self.bind(bg_color=self.update_canvas)  # when bg_color changes, trigger canvas redraw
        self.bind(state=self.on_state)  # bind the state property to the on_state method

    def on_icon(self, instance, value):
        """ Set text to the Unicode value when the icon is assigned """
        self.text = value

    def on_state(self, instance, value):
        """ Set bg_color based on the state of the button 'down' vs 'normal' """
        if value == 'down':  # if button is pressed
            self.bg_color = self.pressed_bg_color  # Set pressed color
        else:  # if button is in 'normal' state
            if not self.collide_point(*self.to_window(0, 0)):  # check if mouse is not hovering
                self.bg_color = self.default_bg_color
        self.update_canvas()

    def update_canvas(self, *args):
        """ Update the background color and rectangle to match a button's behavior """
        self.canvas.before.clear()  # clear existent drawing
        with self.canvas.before:  # redraw with bg_color values
            Color(*self.bg_color)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos)
