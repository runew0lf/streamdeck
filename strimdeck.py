import StreamDeck as StreamDeck
import threading
import random
import pyautogui
import pyperclip
import subprocess
from os import listdir
from streamdeck_image import get_key_alt_image, get_key_image

key_images = []
# key_images = get_key_full_image('full.png')
key_alt_images = []
for k in range(15):
    # Choose a random icon and assign it to a key
    key_images.append(get_key_image(f"icons\{random.choice(listdir('icons'))}"))
    # Generate default alt images (when key is pressed)
    key_alt_images.append(get_key_alt_image(key_images[k]))


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
        deck.set_key_image(key, key_images[key])


if __name__ == "__main__":
    streamdeck = StreamDeck.DeviceManager().enumerate()[0]
    streamdeck.open()
    streamdeck.reset()

    streamdeck.set_brightness(100)

    for k in range(streamdeck.key_count()):
        streamdeck.set_key_image(k, key_images[k])

    streamdeck.set_key_callback(key_change_callback)

    for t in threading.enumerate():
        if t is threading.currentThread():
            continue

        t.join()
