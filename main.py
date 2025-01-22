import os

from kivy import Config
from kivy.app import App
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout

from utils import find_project_root, rgb_format

# custom widgets
import custom_widgets.base_widgets
import custom_widgets.AutoSuggestionInputBox.auto_suggestion_input_box
import custom_widgets.NumericInputBox.numeric_input_box
import custom_widgets.IconButton.icon_button
import custom_widgets.SimpleButton.simple_button
import custom_widgets.ResponsiveGridView.responsive_grid_view
import custom_widgets.LoadingSpinner.loading_spinner
import custom_widgets.TopBar.top_bar
import custom_widgets.Tooltip.tooltip
import custom_widgets.MapUi.map_ui
import custom_widgets.TableView.table_view
import custom_widgets.SearchInputBox.search_input_box
import custom_widgets.PillContainer.pill_container
import custom_widgets.SegmentedController.segmented_controller
import custom_widgets.FilterContainer.filter_container

# projects
import projects.md_icons_viewer.screen
import projects.time_calculator.screen
import projects.unit_converter.screen
import projects.countries.screen
import projects.color_picker.screen

# material design icons
from assets.fonts.material_design.webfont_unicodes import icons

Config.set('input', 'mouse', 'mouse,disable_multitouch')  # get rid of the red circle upon right-click on mouse

fonts_path = os.path.join(find_project_root(), 'assets', 'fonts')
custom_widgets_path = os.path.join(find_project_root(), 'custom_widgets')
projects_path = os.path.join(find_project_root(), 'projects')


class KivyProjectsApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        LabelBase.register(name='roboto-medium', fn_regular=os.path.join(fonts_path, 'roboto', 'Roboto-Medium.ttf'))
        LabelBase.register(name='roboto-bold', fn_regular=os.path.join(fonts_path, 'roboto', 'Roboto-Bold.ttf'))
        LabelBase.register(name='md-icon', fn_regular=os.path.join(fonts_path, 'material_design', 'materialdesignicons-webfont.ttf'))
        LabelBase.register(name='digital', fn_regular=os.path.join(fonts_path, 'digital_numbers', 'DigitalNumbers-Regular.ttf'))

        # load the base widgets components
        Builder.load_file(os.path.join(custom_widgets_path, 'BaseWidgets.kv'))

        # register custom widgets: python modules with corresponding class and .kv file
        Factory.register('AutoSuggestionInputBox', cls=custom_widgets.AutoSuggestionInputBox)
        Factory.register('NumericInputBox', cls=custom_widgets.NumericInputBox)
        Factory.register('IconButton', cls=custom_widgets.IconButton)
        Factory.register('SimpleButton', cls=custom_widgets.SimpleButton)
        Factory.register('ResponsiveGridView', cls=custom_widgets.ResponsiveGridView)
        Factory.register('LoadingSpinner', cls=custom_widgets.LoadingSpinner)
        Factory.register('TopBar', cls=custom_widgets.TopBar)
        Factory.register('Tooltip', cls=custom_widgets.Tooltip)
        Factory.register('MapUi', cls=custom_widgets.MapUi)
        Factory.register('TableView', cls=custom_widgets.TableView)
        Factory.register('SearchInputBox', cls=custom_widgets.SearchInputBox)
        Factory.register('PillContainer', cls=custom_widgets.PillContainer)
        Factory.register('SegmentedController', cls=custom_widgets.SegmentedController.segmented_controller)
        Factory.register('FilterContainer', cls=custom_widgets.FilterContainer.filter_container)

        # register screen classes (the projects of the app)
        Factory.register('MdIconsViewerScreen', cls=projects.md_icons_viewer.screen.MdIconsViewerScreen)
        Factory.register('CountriesMainScreen', cls=projects.countries.screen.CountriesMainScreen)
        Factory.register('TimeCalculatorScreen', cls=projects.time_calculator.screen.TimeCalculatorScreen)
        Factory.register('UnitConverterScreen', cls=projects.unit_converter.screen.UnitConverterScreen)
        Factory.register('ColorPickerScreen', cls=projects.color_picker.screen.ColorPickerScreen)

        self.pm, self.spinner, self.map_ui = None, None, None  # initialize project manager and global spinner
        self.icons = icons  # material design icons dictionary

    def build(self):
        # load custom widgets kv files
        Builder.load_file(os.path.join(custom_widgets_path, 'AutoSuggestionInputBox', 'AutoSuggestionInputBox.kv'))
        Builder.load_file(os.path.join(custom_widgets_path, 'NumericInputBox', 'NumericInputBox.kv'))
        Builder.load_file(os.path.join(custom_widgets_path, 'IconButton', 'IconButton.kv'))
        Builder.load_file(os.path.join(custom_widgets_path, 'SimpleButton', 'SimpleButton.kv'))
        Builder.load_file(os.path.join(custom_widgets_path, 'ResponsiveGridView', 'ResponsiveGridView.kv'))
        Builder.load_file(os.path.join(custom_widgets_path, 'LoadingSpinner', 'LoadingSpinner.kv'))
        Builder.load_file(os.path.join(custom_widgets_path, 'TopBar', 'TopBar.kv'))
        Builder.load_file(os.path.join(custom_widgets_path, 'Tooltip', 'Tooltip.kv'))
        Builder.load_file(os.path.join(custom_widgets_path, 'MapUi', 'MapUi.kv'))
        Builder.load_file(os.path.join(custom_widgets_path, 'TableView', 'TableView.kv'))
        Builder.load_file(os.path.join(custom_widgets_path, 'SearchInputBox', 'SearchInputBox.kv'))
        Builder.load_file(os.path.join(custom_widgets_path, 'PillContainer', 'PillContainer.kv'))
        Builder.load_file(os.path.join(custom_widgets_path, 'SegmentedController', 'SegmentedController.kv'))
        Builder.load_file(os.path.join(custom_widgets_path, 'FilterContainer', 'FilterContainer.kv'))

        # load the projects kv files
        Builder.load_file(os.path.join(projects_path, 'md_icons_viewer', 'MdIconsViewerScreen.kv'))
        Builder.load_file(os.path.join(projects_path, 'countries', 'CountriesScreen.kv'))
        Builder.load_file(os.path.join(projects_path, 'time_calculator', 'TimeCalculatorScreen.kv'))
        Builder.load_file(os.path.join(projects_path, 'unit_converter', 'UnitConverterScreen.kv'))
        Builder.load_file(os.path.join(projects_path, 'color_picker', 'ColorPickerScreen.kv'))

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

    def rgb_formatter(self, rgb_val, factor=0.0, darken=False, lighten=False):
        return rgb_format(rgb_val, factor, darken, lighten)

    # prevent app from closing when hitting Escape key
    def on_key_down(self, instance, keyboard, keycode, text, modifiers):
        if keycode == 27 or keycode == 41:  # 27 = Escape; 41 = Space, although 41 binds to Escape as well
            return True
        return False


class AppContainer(FloatLayout):
    pass


if __name__ == '__main__':
    Window.size = (1000, 650)
    KivyProjectsApp().run()
