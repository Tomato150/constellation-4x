from kivy.uix.gridlayout import GridLayout

from rendering.custom_uix.custom_label import CustomLabel


class CustomTable(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._metadata = None
        self.data = list()

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, value):
        if self._metadata != value:
            self._metadata = value
            self.data = list()
            self.cols = len(self._metadata)

    def update_metadata(self, metadata):
        """
        
        :param metadata: A list with all the metadata keys in it.
        """
        self.clear_widgets()
        self.metadata = metadata

    def _draw_metadata(self):
        for key in self.metadata:
            self.add_widget(CustomLabel(text=key.replace('_', ' ').capitalize()))

    def add_data(self, dataset):
        if type(dataset) == list:
            self.data.extend(dataset)
        else:
            self.data.append(dataset)
        self.redraw_table()

    def remove_data(self, target):
        try:
            if target in self.data:
                self.data.remove(target)
        except:
            pass

    def remove_all_data(self):
        self.data = dict()

    def redraw_table(self, *args):
        self.clear_widgets()

        self._draw_metadata()
        self._draw_data()

    def _draw_data(self):
        for obj in self.data:
            try:
                data = obj.get_data_for_table()
                for key in self.metadata:
                    if type(data[key]) == float:
                        self.add_widget(CustomLabel(text=str(round(data[key], 2))))
                    else:
                        self.add_widget(CustomLabel(text=str(data[key])))
            except ReferenceError:
                self.remove_data(obj)

