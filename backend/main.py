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

smallFont = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansBold.ttf', 20)
largeFont = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansBold.ttf', 27)


def draw_image(image, epd=epd):
    epd.prepare()
    epd.display(image)

@app.get('/text')
async def render_text(author, text):
    image = Image.new('1', (epd.width, epd.height), 255)
    draw = ImageDraw.Draw(image)

    # Top "Author Said" Box
    draw.rectangle((0, 0, epd.width, int(0.227 * epd.height)), fill=0)
    draw.text((10, 10), author, font=smallFont, fill=255)

    