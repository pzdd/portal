import base64
from PIL import Image
from io import BytesIO

with open("cbf.png", "rb") as image_file:
    data = base64.b64encode(image_file.read())

im = Image.open(BytesIO(base64.b64decode(data)))
im.save('image1.png', 'PNG')