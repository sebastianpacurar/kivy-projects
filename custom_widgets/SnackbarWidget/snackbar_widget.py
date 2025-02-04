from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.floatlayout import FloatLayout


class SnackbarWidget(FloatLayout):
    text = StringProperty('')
    duration = NumericProperty(1.5)
    status = StringProperty('success')  # this can be 'success' (green) or 'warning' (yellow) or 'fail' (red)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_color(self):
        """ Returns the color based on the snackbar status"""
        colors = {
            'success': [24, 184, 75, 255],
            'fail': [172, 35, 51, 255],
            'warning': [226, 166, 38, 255]
        }
        return colors[self.status]

    def show(self):
        """ Bring the snackbar up from bottom left side of the screen """
        target_pos = (self.x, dp(10))  # dp(10) units from the bottom
        self.pos = (self.x, -self.height)  # start from below the screen
        anim = Animation(pos=target_pos, d=self.duration / 10, t='out_quad')
        anim.bind(on_complete=lambda *x: self.start_progress_bar())
        anim.start(self)

    def start_progress_bar(self):
        """ Start timeout for Snackbar and animate progress bar"""
        anim = Animation(value=100, d=self.duration, t='linear')
        anim.bind(on_complete=lambda *x: Clock.schedule_once(self.dismiss))
        anim.start(self.ids.progress_bar)

    def dismiss(self, *args):
        """ Push the Snackbar down, below the screen then remove it from root tree"""
        offscreen_pos = (self.x, -self.height)  # go below the screen (same val as self.pos in show func)
        anim = Animation(pos=offscreen_pos, d=self.duration / 10, t='in_quad')
        anim.bind(on_complete=lambda *x: self.parent.remove_widget(self))
        anim.start(self)
