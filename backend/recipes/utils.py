import random


def get_random_hex_code():
    """Generate random color hex code."""
    return '#%06x' % random.randint(0, 0xFFFFFF)
