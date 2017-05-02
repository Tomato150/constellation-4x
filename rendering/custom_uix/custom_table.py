from kivy.uix.gridlayout import GridLayout


class CustomTable(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._metadata = None

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, value):
        if self._metadata != value:
            self._metadata = value
            self.cols = len(self._metadata)

    def update_metadata(self, metadata):
        self.clear_widgets()
        self.metadata = metadata
        for key in self.metadata:
            pass
