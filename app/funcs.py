from random import randint
from string import ascii_letters


def change_model_image(model, img_url, **kwargs):
    if model == 'user':
        instance = kwargs['request'].user
        instance.img_url = img_url
        instance.save()

HEX_SYMBOLS = ''.join([str(n) for n in range(10)]) + ascii_letters[:6]
def get_random_hex_color():
    hex_color = ''
    for _ in range(6):
        hex_color += HEX_SYMBOLS[randint(0, len(HEX_SYMBOLS) - 1)]
    return hex_color
