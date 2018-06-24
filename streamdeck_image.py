from PIL import Image
import io


def get_key_image(filename: str):
    output = io.BytesIO()
    image = Image.open(filename)
    image.thumbnail((72, 72))

    img_w, img_h = image.size
    background = Image.new('RGBA', (72, 72), (0, 0, 0, 255))
    bg_w, bg_h = background.size
    offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
    background.paste(image, offset)
    background = background.rotate(180)

    background.convert('RGB').save(output, 'BMP')
    return output.getvalue()[54:]


def get_key_alt_image(filename):
    output = io.BytesIO()
    image = Image.frombytes("RGB", (72, 72), filename)
    image.thumbnail((50, 50))
    b, g, r = image.split()
    image = Image.merge("RGB", (r, g, b))

    img_w, img_h = image.size
    background = Image.new('RGBA', (72, 72), (0, 0, 0, 255))
    bg_w, bg_h = background.size
    offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
    background.paste(image, offset)
    background = background.rotate(180)
    background = background.transpose(Image.FLIP_LEFT_RIGHT)

    background.convert('RGB').save(output, 'BMP')
    return output.getvalue()[54:]


def get_key_full_image(filename):
    image_list = []
    image = Image.open(filename)
    size = 72 * 5, 72 * 3
    image.thumbnail(size)
    img_w, img_h = image.size
    background = Image.new('RGBA', (size), (0, 0, 0, 255))
    bg_w, bg_h = background.size
    offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
    background.paste(image, offset)
    background = background.rotate(180)

    for rows in range(0, 3):
        for columns in range(0, 5):
            crop_size = 72
            output = io.BytesIO()
            x = img_w - ((5 - columns) * crop_size)
            y = (2 - rows) * crop_size
            box = (x, y, x + crop_size, y + crop_size)
            key_image = background.crop(box)
            key_image.convert('RGB').save(output, 'BMP')
            image_list.append(output.getvalue()[54:])

    return image_list
