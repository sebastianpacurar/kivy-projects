import os

from kivy import Config
from kivy.app import App
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout

from utils import find_project_root, rgb_format

# custom components
from custom_components.BaseComponents.base_components import *
import custom_components.AutoSuggestionInputBox.auto_suggestion_input_box
import custom_components.NumericInputBox.numeric_input_box
import custom_components.IconButton.icon_button
import custom_components.ResponsiveGridView.responsive_grid_view
import custom_components.LoadingSpinner.loading_spinner
import custom_components.TopBar.top_bar
import custom_components.Tooltip.tooltip
import custom_components.MapUi.map_ui
import custom_components.TableView.table_view
import custom_components.SearchInputBox.search_input_box
import custom_components.PillContainer.pill_container
import custom_components.SegmentedController.segmented_controller
import custom_components.FilterContainer.filter_container

# projects
import projects.md_icons_viewer.screen
import projects.time_calculator.screen
import projects.unit_converter.screen
import projects.countries.screen

# material design icons
from assets.fonts.material_design.webfont_unicodes import icons

Config.set('input', 'mouse', 'mouse,disable_multitouch')  # get rid of the red circle upon right-click on mouse


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

        # register python-defined components: present in BaseComponents.kv but without a specific python module
        Factory.register('BaseButton', cls=BaseButton)
        Factory.register('BaseLabel', cls=BaseLabel)
        Factory.register('TextLabel', cls=TextLabel)

        # register custom components: python modules with corresponding class and .kv file
        Factory.register('AutoSuggestionInputBox', cls=custom_components.AutoSuggestionInputBox)
        Factory.register('NumericInputBox', cls=custom_components.NumericInputBox)
        Factory.register('IconButton', cls=custom_components.IconButton)
        Factory.register('ResponsiveGridView', cls=custom_components.ResponsiveGridView)
        Factory.register('LoadingSpinner', cls=custom_components.LoadingSpinner)
        Factory.register('TopBar', cls=custom_components.TopBar)
        Factory.register('Tooltip', cls=custom_components.Tooltip)
        Factory.register('MapUi', cls=custom_components.MapUi)
        Factory.register('TableView', cls=custom_components.TableView)
        Factory.register('SearchInputBox', cls=custom_components.SearchInputBox)
        Factory.register('PillContainer', cls=custom_components.PillContainer)
        Factory.register('SegmentedController', cls=custom_components.SegmentedController.segmented_controller)
        Factory.register('FilterContainer', cls=custom_components.FilterContainer.filter_container)

        # register screen classes (the projects of the app)
        Factory.register('MdIconsViewerScreen', cls=projects.md_icons_viewer.screen.MdIconsViewerScreen)
        Factory.register('CountriesMainScreen', cls=projects.countries.screen.CountriesMainScreen)
        Factory.register('TimeCalculatorScreen', cls=projects.time_calculator.screen.TimeCalculatorScreen)
        Factory.register('UnitConverterScreen', cls=projects.unit_converter.screen.UnitConverterScreen)

        self.pm, self.spinner, self.map_ui = None, None, None  # initialize project manager and global spinner
        self.icons = icons  # material design icons dictionary

    def build(self):
        Builder.load_file(os.path.join(self.project_root, 'custom_components', 'AutoSuggestionInputBox', 'AutoSuggestionInputBox.kv'))
        Builder.load_file(os.path.join(self.project_root, 'custom_components', 'NumericInputBox', 'NumericInputBox.kv'))
        Builder.load_file(os.path.join(self.project_root, 'custom_components', 'IconButton', 'IconButton.kv'))
        Builder.load_file(os.path.join(self.project_root, 'custom_components', 'ResponsiveGridView', 'ResponsiveGridView.kv'))
        Builder.load_file(os.path.join(self.project_root, 'custom_components', 'LoadingSpinner', 'LoadingSpinner.kv'))
        Builder.load_file(os.path.join(self.project_root, 'custom_components', 'TopBar', 'TopBar.kv'))
        Builder.load_file(os.path.join(self.project_root, 'custom_components', 'Tooltip', 'Tooltip.kv'))
        Builder.load_file(os.path.join(self.project_root, 'custom_components', 'MapUi', 'MapUi.kv'))
        Builder.load_file(os.path.join(self.project_root, 'custom_components', 'TableView', 'TableView.kv'))
        Builder.load_file(os.path.join(self.project_root, 'custom_components', 'SearchInputBox', 'SearchInputBox.kv'))
        Builder.load_file(os.path.join(self.project_root, 'custom_components', 'PillContainer', 'PillContainer.kv'))
        Builder.load_file(os.path.join(self.project_root, 'custom_components', 'SegmentedController', 'SegmentedController.kv'))
        Builder.load_file(os.path.join(self.project_root, 'custom_components', 'FilterContainer', 'FilterContainer.kv'))

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
        self.spinner = self.root.ids.loadingSpinner
        self.map_ui = self.root.ids.map
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

    def show_spinner(self):
        """ Disable projectManager and display Spinner """
        self.pm.disabled = True
        self.spinner.opacity = 1

    def hide_spinner(self, *args):
        """ Enable projectManager and hide spinner """
        self.spinner.opacity = 0
        self.pm.disabled = False

    def toggle_app_map(self, value):
        self.map_ui.is_map_displayed = value

    def rgb_formatter(self, rgb_val,  factor=0.0, darken=False, lighten=False):
        return rgb_format(rgb_val, factor, darken, lighten)

    # prevent app from closing when hitting Escape key
    def on_key_down(self, instance, keyboard, keycode, text, modifiers):
        if keycode == 27 or keycode == 41:  # 27 = Escape; 41 = Space, although 41 binds to Escape as well
            return True
        return False


class AppContainer(FloatLayout):
    pass


if __name__ == '__main__':
    KivyProjectsApp().run()
