from kivy.app import App
from kivy.factory import Factory

import utils.components


class KivyProjectsApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pm = None

    def on_start(self):
        self.pm = self.root.ids.projectManager
        super().on_start()

    def nav_to_project(self, project_screen_name):
        """Navigate to a screen, loading it dynamically if needed."""
        if not self.pm.has_screen(project_screen_name):
            try:
                # Dynamically load the screen class from Factory
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


if __name__ == '__main__':
    KivyProjectsApp().run()
