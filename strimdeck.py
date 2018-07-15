import StreamDeck as StreamDeck
import threading
import random
import pyautogui
import pyperclip
import subprocess
from os import listdir
from streamdeck_image import get_key_alt_image, get_key_image, get_key_full_image

from PIL import Image, GifImagePlugin
import io
import time

key_images = []
key_alt_images = []
for k in range(15):
    # Choose a random icon and assign it to a key
    key_images.append(get_key_image(f"icons\{random.choice(listdir('icons'))}"))
    # Generate default alt images (when key is pressed)
    key_alt_images.append(get_key_alt_image(key_images[k]))

#key_images = get_key_full_image('full.png')


def test():
    image = Image.open("test.gif")

    for frame in range(0, image.n_frames):
        output = io.BytesIO()
        image.seek(frame)
        wpercent = (72 / float(image.size[0]))
        hsize = int((float(image.size[1]) * float(wpercent)))
        rescale = image.resize((72, hsize), Image.ANTIALIAS)
        img_w, img_h = rescale.size
        background = Image.new('RGBA', (72, 72), (0, 0, 0, 255))
        bg_w, bg_h = background.size
        offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
        background.paste(rescale, offset)
        background = background.rotate(180)
        background.convert('RGB').save(output, 'BMP')

        streamdeck.set_key_image(0, output.getvalue()[54:])
        output.close()
        time.sleep(0.03)



def key_change_callback(deck, key, state):
    print(f"Key {key} = {state}")
    if state:
        deck.set_key_image(key, key_alt_images[key])
        if key == 0:
            pyautogui.hotkey('ctrl', 'c')
            args = ['C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
                    f'http://rapptz.github.io/discord.py/docs/search.html?q={pyperclip.paste()}']
            subprocess.call(args)

    else:
        test()
        deck.set_key_image(key, key_images[key])


if __name__ == "__main__":
    streamdeck = StreamDeck.DeviceManager().enumerate()[0]
    streamdeck.open()
    streamdeck.reset()

    streamdeck.set_brightness(100)

    for k in range(streamdeck.key_count()):
        streamdeck.set_key_image(k, key_images[k])

    test()
    streamdeck.set_key_callback(key_change_callback)

    for t in threading.enumerate():
        if t is threading.currentThread():
            continue

        t.join()

