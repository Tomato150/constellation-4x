from kivy.utils import get_color_from_hex

colors = {
    'primary': (0.008, 0.459, 0.847, 1),
    'success': (0.361, 0.722, 0.361, 1),
    'info': (0.192, 0.69, 0.835, 1),
    'warning': (0.941, 0.678, 0.306, 1),
    'danger': (0.851, 0.325, 0.31, 1),

    'black': get_color_from_hex('#000000'),
    'jet_black': get_color_from_hex('#232324'),
    'white': (1, 1, 1, 1),
    'opaque': (0, 0, 0, 0)
}

fonts = {
    'sizes': {
        'display_1': 96,
        'display_2': 88,
        'display_3': 72,
        'display_4': 56,
        'h1': 40,
        'h2': 32,
        'h3': 28,
        'h4': 24,
        'h5': 20,
        'standard': 16
    }
}
