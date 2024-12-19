import pytest
from kivy.clock import Clock
from functools import wraps
from main import KivyProjectsApp


@pytest.fixture()
def app_instance():
    app = KivyProjectsApp()

    # Ensure EventLoop is properly initialized
    Clock.tick()  # Process one frame for initialization
    yield app  # Provide the app instance to the test


def navigation_test(expected_screen, expected_top_bar_name):
    """ Handle common navigation test logic
        Set up navigation, assertions and cleanup
    """

    def decorator(test_func):
        @wraps(test_func)
        def wrapper(app_instance):
            def navigate_and_assert(dt):
                app_instance.nav_to_project(expected_screen)

                assert app_instance.pm.current == expected_screen
                assert app_instance.pm.screens[1].ids.get('top_bar').project_name == expected_top_bar_name

                home_btn = app_instance.pm.screens[1].ids.get('top_bar').ids.get('home_button')
                home_btn.dispatch('on_release')

                app_instance.stop()

            Clock.schedule_once(navigate_and_assert, 0)
            app_instance.run()

            return test_func(app_instance)

        return wrapper

    return decorator


@pytest.mark.ui
@navigation_test(expected_screen='MdIconsViewerScreen', expected_top_bar_name='Material Design Icons')
def test_navigation_to_MdIconsViewerScreen(app_instance):
    pass


@pytest.mark.ui
@navigation_test(expected_screen='TimeCalculatorScreen', expected_top_bar_name='Time Calculator')
def test_navigation_to_TimeCalculatorScreen(app_instance):
    pass


@pytest.mark.ui
@navigation_test(expected_screen='UnitConverterScreen', expected_top_bar_name='Unit Converter')
def test_navigation_to_UnitConverterScreen(app_instance):
    pass


@pytest.mark.ui
@navigation_test(expected_screen='CountriesMainScreen', expected_top_bar_name='Countries')
def test_navigation_to_CountriesScreen(app_instance):
    pass
