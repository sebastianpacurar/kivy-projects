from kivy.graphics import Line, Color
from kivy.properties import NumericProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock


class LoadingSpinner(FloatLayout):
    radius = NumericProperty(50)
    line_width = NumericProperty(6)
    angle_start = NumericProperty(0)
    angle_length = NumericProperty(60)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # fill the blue progress bar
        with self.canvas:
            self.background_color = Color(.75, .75, .75, 1)  # grey hollow circle bg
            self.background_arc = Line(
                circle=(self.center_x, self.center_y, self.radius, 0, 360),
                width=self.line_width,
            )
            self.foreground_color = Color(0.2, 0.6, 0.8, 1)  # blue progress bar
            self.blue_arc = Line(width=self.line_width)


        self.bind(pos=self.spin) # trigger spin when pos changes
        Clock.schedule_interval(self.spin, 0.0001) # perform smoothness

    def spin(self, *args):
        self.angle_start += 8  # speed of blue arch
        self.angle_start %= 360

        self.background_arc.circle = (self.center_x, self.center_y, self.radius, 0, 360)
        self.blue_arc.circle = (
            self.center_x,
            self.center_y,
            self.radius,
            self.angle_start,
            self.angle_start + self.angle_length,  # angle_end
        )
