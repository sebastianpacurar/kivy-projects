from kivy.properties import DictProperty, ListProperty, ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from custom_widgets.AutoSuggestionInputBox.auto_suggestion_input_box import AutoSuggestionInputBox
from custom_widgets.base_widgets import PropCachedWidget


class FilterContainer(BoxLayout, PropCachedWidget):
    filters_labels = ListProperty([])
    filters_selected_option = ListProperty([])
    filters_default_option = ListProperty([])
    filters_options = ListProperty([])
    filters_widths = ListProperty([])
    filters_func = ObjectProperty(None)

    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        self.init_filters()

    def init_filters(self, *args):
        for index, (label, selected_opt, default_opt, options, width) in enumerate(
                zip(self.filters_labels, self.filters_selected_option, self.filters_default_option, self.filters_options, self.filters_widths)
        ):
            filter_box = FilterBox(
                label_text=label,
                selected_option=selected_opt,
                default_option=default_opt,
                options=options,
                width=width,
                size_hint_x=None,
                enhanced=True,
                filters_func=self.filters_func,
            )

            reset_btn = ResetFilters(
                text_field=filter_box.ids.input_field,
                default_option=filter_box.default_option,
                options=filter_box.options,
            )

            filter_box.add_widget(reset_btn)
            self.add_widget(filter_box)

    def hide_widgets(self):
        self.recursive_hide(self)
        super().hide_widget(self.cached_props)

    def reveal_widgets(self):
        self.recursive_reveal(self)
        super().reveal_widget()


class FilterBox(AutoSuggestionInputBox, PropCachedWidget):
    filters_func = ObjectProperty(None)
    data = DictProperty({})

    def on_kv_post(self, base_widget):
        AutoSuggestionInputBox.on_kv_post(self, base_widget)
        PropCachedWidget.on_kv_post(self, base_widget)

    def on_selected_option(self, instance, value):
        if self.filters_func and self.parent:
            self.data = self.filters_func(instance, value)
            self.refresh_data()

    def refresh_data(self):
        for i in reversed(self.parent.children):
            opt = list(self.data[i.label_text])
            if len(opt) > 1:
                i.options = ['All'] + sorted(opt)
            else:
                i.options = opt


class ResetFilters(RelativeLayout, PropCachedWidget):
    text_field = ObjectProperty(None)
    default_option = StringProperty('All')
    options = ListProperty([])

    def reset_to_default(self, *args):
        """ Reset selected option to default option """
        self.text_field.text = self.default_option
        self.parent.selected_option = self.default_option
        self.ids.reset_button.disabled = True
        if len(self.parent.options) > 1:
            self.parent.highlighted_index = -1
