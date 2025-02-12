from random import randint
from string import ascii_letters
import re


def change_model_image(model, img_url, **kwargs):
    if model == 'user':
        instance = kwargs['request'].user
        instance.img_url = img_url
    elif model == 'chat':
        instance = kwargs['models_classes'][model].objects.get(
            id=int(kwargs['chat_id']))
        instance.img_url = img_url
    instance.save()

HEX_SYMBOLS = ''.join([str(n) for n in range(10)]) + ascii_letters[:6]
def get_random_hex_color():
    while True:
        hex_color = ''
        for _ in range(6):
            hex_color += HEX_SYMBOLS[randint(0, len(HEX_SYMBOLS) - 1)]
        if hex_color[:2] == hex_color[2:4]: hex_color = get_random_hex_color()
        m = re.match(r'^#?([0-9A-Fa-f]{6})$', hex_color)
        if m:
            hex_value = m.group(1)
            r = int(hex_value[0:2], 16)
            g = int(hex_value[2:4], 16)
            b = int(hex_value[4:6], 16)
            brightness = (r * 0.299 + g * 0.587 + b * 0.114)
            if brightness >= 155: return hex_color
