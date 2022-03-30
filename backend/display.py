import sys

from omni_epd import EPDNotFoundError, displayfactory

try:
    epd = displayfactory.load_display_driver()
except EPDNotFoundError:
    print("No EPD display found")
    sys.exit(1)

epd.prepare()

# Fix Override
def c():
    epd._device.Clear(0xFF)
epd.clear = c
