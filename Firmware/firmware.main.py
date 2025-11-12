import time, board, digitalio
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.modules import Module
from kmk.extensions.rgb import RGB

class Haptic(Module):
    def __init__(self, pin, pulse_ms=40):
        self._pin = digitalio.DigitalInOut(pin)
        self._pin.direction = digitalio.Direction.OUTPUT
        self._pin.value = False
        self._off_time = 0.0
        self._pulse = pulse_ms / 1000.0

    def process_key(self, keyboard, key, pressed, int_coord=None):
        if pressed:
            self._pin.value = True
            self._off_time = time.monotonic() + self._pulse
        return key

    def before_matrix_scan(self, keyboard):
        if self._off_time and time.monotonic() >= self._off_time:
            self._pin.value = False
            self._off_time = 0.0

kbd = KMKKeyboard()
kbd.col_pins = []
kbd.row_pins = []
kbd.diode_orientation = None

kbd.direct_pins = [
    board.GP0,
    board.GP1,
    board.GP2,
    board.GP3,
    board.GP4,
    board.GP5,
]

rgb = RGB(
    pixel_pin=board.GP14,
    num_pixels=2,
    hue_default=180,
    sat_default=255,
    val_default=60,
)
kbd.extensions.append(rgb)

kbd.modules.append(Haptic(board.GP15, 40))

kbd.keymap = [
    [
        KC.MUTE,
        KC.VOLD,
        KC.VOLU,
        KC.MPLY,
        KC.COPY,
        KC.PASTE,
    ],
]

if __name__ == "__main__":
    kbd.go()
