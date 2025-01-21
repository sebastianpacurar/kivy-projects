from kivy.properties import ObjectProperty
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.screenmanager import Screen


class ColorPickerScreen(Screen):
    pass


class CustomColorPicker(ColorPicker):
    color_label = ObjectProperty(None)
    color_preview = ObjectProperty(None)

    def on_color(self, instance, value):
        r, g, b, _ = value
        self.color_label.text = f"RGB: ({int(r * 255)}, {int(g * 255)}, {int(b * 255)})"

    def set_color(self, color):
        print(self.children[0].children[1].children[0].canvas.children[1])
        super().set_color(color)
