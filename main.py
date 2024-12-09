from kivy.app import App
from kivy.core.window import Window
from kivy.factory import Factory

import custom_components.base_components
import custom_components.auto_suggestion_input_box
import custom_components.labeled_numeric_input
import custom_components.icon_button
import custom_components.responsive_grid_view
from assets.fonts.material_design.webfont_unicodes import icons


class KivyProjectsApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pm = None
        self.icons = icons

    def get_icon(self, icon_name):
        """ Returns the icon unicode based on the webfonts material design font """
        return self.icons.get(icon_name, None)

    def on_start(self):
        self.pm = self.root.ids.projectManager
        Window.bind(on_key_down=self.on_key_down)
        super().on_start()

    def nav_to_project(self, project_screen_name):
        """ Navigate to a screen, loading it dynamically if needed """
        if not self.pm.has_screen(project_screen_name):
            try:
                # dynamically load the screen class from Factory
                new_screen = Factory.get(project_screen_name)()
                self.pm.add_widget(new_screen)
            except Exception as e:
                print(f"Error loading screen '{project_screen_name}': {e}")
                return

        self.pm.transition.direction = 'left'
        self.pm.current = project_screen_name

    def nav_to_home(self, *args):
        self.pm.transition.direction = 'right'
        self.pm.current = 'home_screen'

    # prevent app from closing when hitting Escape key
    def on_key_down(self, instance, keyboard, keycode, text, modifiers):
        if keycode == 27 or keycode == 41:  # 27 = Escape; 41 = Space, although 41 binds to Escape as well
            return True
        return False


if __name__ == '__main__':
    KivyProjectsApp().run()
