import textwrap

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, ImageDraw, ImageFont

from display import epd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

small_font = ImageFont.truetype('/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf', 20)
large_font = ImageFont.truetype('/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf', 27)

def draw_image(image, epd=epd):
    epd.prepare()
    epd.display(image)

@app.get('/text')
async def render_text(author, text):

    w = epd.height
    h = epd.width


    image = Image.new('L', (w, h), 255)
    draw = ImageDraw.Draw(image)

    y_ratio = 0.227
    y_cutoff_height = int(y_ratio * h)

    # Author Box
    draw.rectangle((0, 0, w, y_cutoff_height), fill=0)
    draw.text((10, 10), f'{author}', font=small_font, fill=255)

    offset = 0
    for line in textwrap.wrap(text, width=15):
        draw.text((10, 50 + offset), line, font=large_font, fill=0)
        offset += large_font.getsize(line)[1]
    
    # image = image.transpose(Image.ROTATE_90)
    draw_image(image)

@app.get('/image')
async def render_image():
    image = Image.open('in.jpg')
    image = image.resize((epd.width, epd.height))
    # image = image.transpose(Image.ROTATE_90)
    draw_image(image)
