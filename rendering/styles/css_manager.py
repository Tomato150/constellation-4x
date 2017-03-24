import sys

global_styles = {
    'color': (1, 1, 1, 1),
    'canvas_color': (1, 1, 0, 1)
}


class CSSManager:
    def __init__(self, parent, base_object=False):
        self.container = parent
        self.styles = {}
        if base_object:
            self.styles = global_styles

    def load_styles(self):
        for style_class in self.container.style_classes:
            for style, value in self.container.local_styles[style_class].items():
                self.styles[style] = value

    def apply_styles(self):
        self.update_styles()
        for style, value in self.styles.items():
            self.container.__setattr__(style, value)

    def update_styles(self):
        try:
            for style, value in self.styles.items():
                if value == 'inherit':
                    widget = self.container
                    parent_css = None
                    while parent_css is None:
                        widget = widget.parent
                        try:
                            parent_css = widget.css
                            if parent_css.styles[style] != 'inherit':
                                self.styles[style] = parent_css.styles[style]
                            else:
                                parent_css = None
                        except AttributeError:
                            parent_css = None
        except:
            e = sys.exc_info()[0]
            print('ERROR ENCOUNTERED')
            print(e)
