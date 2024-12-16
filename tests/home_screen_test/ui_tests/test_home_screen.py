import pytest
from kivy.clock import Clock

from main import KivyProjectsApp


def navigate_to_home_screen(btn):
    btn.dispatch('on_release')


@pytest.fixture()
def app_instance(request):
    app = KivyProjectsApp()

    # ensure EventLoop is properly initialized
    Clock.tick()  # process one frame for initialization
    yield app  # provide the app instance to the test


@pytest.mark.ui
def test_navigation_to_MdIconsViewerScreen(app_instance):
    def navigate_and_assert(dt):
        app_instance.nav_to_project('MdIconsViewerScreen')

        assert app_instance.pm.current == 'MdIconsViewerScreen'
        assert app_instance.pm.screens[1].ids.get("top_bar").project_name == 'Material Design Icons'

        home_btn = app_instance.pm.screens[1].ids.get("top_bar").ids.get("home_button")
        navigate_to_home_screen(home_btn)

        app_instance.stop()

    Clock.schedule_once(navigate_and_assert, 0)
    app_instance.run()

@pytest.mark.ui
def test_navigation_to_TimeCalculatorScreen(app_instance):
    def navigate_and_assert(dt):
        app_instance.nav_to_project('TimeCalculatorScreen')

        assert app_instance.pm.current == 'TimeCalculatorScreen'
        assert app_instance.pm.screens[1].ids.get("top_bar").project_name == 'Time Calculator'

        home_btn = app_instance.pm.screens[1].ids.get("top_bar").ids.get("home_button")
        navigate_to_home_screen(home_btn)

        app_instance.stop()

    Clock.schedule_once(navigate_and_assert, 0)
    app_instance.run()
