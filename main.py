import os

from kivy.app import App
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.lang import Builder

from path_finder import find_project_root

# custom components
from custom_components.BaseComponents.base_components import *
import custom_components.AutoSuggestionInputBox.auto_suggestion_input_box
import custom_components.NumericInputBox.numeric_input_box
import custom_components.IconButton.icon_button
import custom_components.ResponsiveGridView.responsive_grid_view

# projects
import projects.md_icons_viewer.screen
import projects.time_calculator.screen
import projects.unit_converter.screen
import projects.countries.screen

# material design icons
from assets.fonts.material_design.webfont_unicodes import icons


class KivyProjectsApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.project_root = find_project_root()

        LabelBase.register(
            name="roboto-medium",
            fn_regular=os.path.join(self.project_root, "assets/fonts/roboto/Roboto-Medium.ttf"),
        )

        LabelBase.register(
            name="md-icon",
            fn_regular=os.path.join(self.project_root, "assets/fonts/material_design/materialdesignicons-webfont.ttf"),
        )

        LabelBase.register(
            name="digital",
            fn_regular=os.path.join(self.project_root, "assets/fonts/digital_numbers/DigitalNumbers-Regular.ttf"),
        )

        # load the KV file for rule-based components like <Filler@Widget>
        Builder.load_file(os.path.join(self.project_root, 'custom_components', 'BaseComponents', 'BaseComponents.kv'))

        # register python-defined components (present in BaseComponents.kv but without a specific python class)
        Factory.register('BaseButton', cls=BaseButton)
        Factory.register('BaseLabel', cls=BaseLabel)
        Factory.register('TopBar', cls=TopBar)
        Factory.register('SimpleDropdown', cls=SimpleDropdown)
        Factory.register('SegmentedButton', cls=SegmentedButton)

        # register custom components (python classes with corresponding .kv files)
        Factory.register('AutoSuggestionInputBox', cls=custom_components.AutoSuggestionInputBox)
        Factory.register('NumericInputBox', cls=custom_components.NumericInputBox)
        Factory.register('IconButton', cls=custom_components.IconButton)
        Factory.register('ResponsiveGridView', cls=custom_components.ResponsiveGridView)

        # register screen classes (the projects of the app)
        Factory.register('MdIconsViewerScreen', cls=projects.md_icons_viewer.screen.MdIconsViewerScreen)
        Factory.register('CountriesMainScreen', cls=projects.countries.screen.CountriesMainScreen)
        Factory.register('TimeCalculatorScreen', cls=projects.time_calculator.screen.TimeCalculatorScreen)
        Factory.register('UnitConverterScreen', cls=projects.unit_converter.screen.UnitConverterScreen)

        self.pm = None  # initialize project manager
        self.icons = icons  # material design icons dictionary

    def build(self):
        Builder.load_file(os.path.join(self.project_root, 'custom_components', 'AutoSuggestionInputBox', 'AutoSuggestionInputBox.kv'))
        Builder.load_file(os.path.join(self.project_root, 'custom_components', 'NumericInputBox', 'NumericInputBox.kv'))
        Builder.load_file(os.path.join(self.project_root, 'custom_components', 'IconButton', 'IconButton.kv'))
        Builder.load_file(os.path.join(self.project_root, 'custom_components', 'ResponsiveGridView', 'ResponsiveGridView.kv'))

        # load the screens dynamically
        Builder.load_file(os.path.join(self.project_root, 'projects', 'md_icons_viewer', 'MdIconsViewerScreen.kv'))
        Builder.load_file(os.path.join(self.project_root, 'projects', 'countries', 'CountriesScreen.kv'))
        Builder.load_file(os.path.join(self.project_root, 'projects', 'time_calculator', 'TimeCalculatorScreen.kv'))
        Builder.load_file(os.path.join(self.project_root, 'projects', 'unit_converter', 'UnitConverterScreen.kv'))

        # attach AppContainer() to root explicitly, to make sure pytests instantiate the app and widget tree properly
        self.root = AppContainer()
        return self.root

    def get_icon(self, icon_name):
        """ Returns the icon unicode based on the webfonts material design font """
        return self.icons.get(icon_name, None)

    def on_start(self):
        super().on_start()
        self.pm = self.root.ids.projectManager
        Window.bind(on_key_down=self.on_key_down)

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


class AppContainer(BoxLayout):
    pass


if __name__ == '__main__':
    KivyProjectsApp().run()
