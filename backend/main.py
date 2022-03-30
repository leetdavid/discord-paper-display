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

def draw_image(image, epd=epd):
    epd.prepare()
    epd.display(image)

@app.get('/text')
async def render_text(author, text):
    image = Image.new('1', (epd.width, epd.height), 255)
