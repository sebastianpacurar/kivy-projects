from kivy.properties import DictProperty, ListProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout

from custom_components.AutoSuggestionInputBox.auto_suggestion_input_box import AutoSuggestionInputBox


class FilterContainer(BoxLayout):
    filters_labels = ListProperty([])
    filters_selected_option = ListProperty([])
    filters_default_option = ListProperty([])
    filters_options = ListProperty([])
    filters_widths = ListProperty([])
    filters_func = ObjectProperty(None)
    dynamic_widgets = DictProperty({})  # store references to dynamic widgets by id

    def on_kv_post(self, base_widget):
        self.init_filters()

    def init_filters(self, *args):
        for index, (label, selected_opt, default_opt, options, width) in enumerate(
                zip(self.filters_labels, self.filters_selected_option, self.filters_default_option, self.filters_options, self.filters_widths)
        ):
            widget_id = f"filter_{label.lower()}"
            filter_box = AutoSuggestionInputBox(
                label_text=label,
                selected_option=selected_opt,
                default_option=default_opt,
                options=options,
                width=width,
                size_hint_x=None,
                enhanced=True,
                filter_widget_index=index,
            )
            filter_box.bind(selected_option=self.filters_func)

            self.dynamic_widgets[widget_id] = filter_box
            self.add_widget(filter_box)

    def get_widget_by_id(self, widget_id):
        """Retrieve a dynamically created widget by its ID."""
        return self.dynamic_widgets.get(widget_id, None)
