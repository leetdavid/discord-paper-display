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

w = epd.height
h = epd.width
y_ratio = 0.227
text_size_ratio = 0.8

author_box_height = y_ratio * h
author_text_size = text_size_ratio * author_box_height
author_text_offset = (1 - text_size_ratio) * author_box_height - 3

author_box_height = int(author_box_height)
author_text_size = int(author_text_size)
author_text_offset = int(author_text_offset)

text_char_break_width = 24

author_font = ImageFont.truetype(
    '/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf',
    author_text_size
)

text_font = ImageFont.truetype(
    '/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf',
    int(0.8 * author_text_size)
)

def draw_image(image, epd=epd):
    epd.prepare()
    epd.display(image)

@app.get('/text')
async def render_text(author, text):
    image = Image.new('L', (w, h), 255)
    draw = ImageDraw.Draw(image)

    # Author Box
    draw.rectangle((0, 0, w, author_box_height), fill=0)
    draw.text((author_text_offset, author_text_offset),
              f'{author}', font=author_font, fill=255)

    offset = 0
    for line in textwrap.wrap(text, width=text_char_break_width):
        draw.text((author_text_offset, author_box_height + author_text_offset + offset),
                  line, font=text_font, fill=0)
        offset += text_font.getsize(line)[1]
    
    # image = image.transpose(Image.ROTATE_90)
    draw_image(image)

@app.get('/image')
async def render_image():
    image = Image.open('in.jpg')
    image = image.resize((epd.width, epd.height))
    # image = image.transpose(Image.ROTATE_90)
    draw_image(image)
