from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup


def create_alert(title, message, button_text="close", separator_color=(0.008, 0.459, 0.847, 1)):
    content = BoxLayout(
        orientation='vertical',
        padding=5
    )
    content.add_widget(Label(
            text=message,
        ))
    button = Button(text=button_text, size_hint=[1, None], size=[400, 30])
    content.add_widget(button)
    popup = Popup(
        title=title,
        content=content,
        size_hint=[None, None],
        size=[400, 400],
        separator_color=separator_color,
    ).open()
    button.bind(on_press=popup.dismiss)
