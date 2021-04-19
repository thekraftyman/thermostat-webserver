# rgbled.py
# By: Adam Kraft

from gpiozero import PWMLED as LED

class RGBLED:

    def __init__(self, red_pin, green_pin, blue_pin):
        self.red_pin   = red_pin
        self.green_pin = green_pin
        self.blue_pin  = blue_pin
        self.red_led   = LED(red_pin)
        self.green_led = LED(green_pin)
        self.blue_led  = LED(blue_led)
        self._leds = [self.red_led, self.green_led, self.blue_led]
        self.colors = {
            'red':    (1,0,0),
            'green':  (0,1,0),
            'blue':   (0,0,1),
            'purple': (1,0,1),
            'yellow': (1,1,0),
            'orange': (1,.5,0),
            'cyan' :  (0,1,1)
        }

    def set(self, value):
        ''' sets the leds '''
        if type(value) == str:
            ''' get the word used for color '''
            if value.lower() in self.colors:
                r,g,b = self.colors[value.lower()]
                self.red_led.value   = r
                self.green_led.value = g
                self.blue_led.value  = b
                return

        if type(value) == tuple:
            assert len(value) == 3
            for led, val in zip(self._leds, value):
                assert val <= 1 and val >= 0
                led.value = float(val)
            return

    def red(self, intensity=0.8):
        ''' sets the led to red with given intensity '''
        self.set((intensity, 0, 0))

    def green(self, intensity=0.8):
        ''' sets the led to green with given intensity '''
        self.set((0, intensity, 0))

    def blue(self, intensity=0.8):
        ''' sets the led to blue with given intensity '''
        self.set(( 0, 0, intensity))

    def off(self):
        ''' turns the led off '''
        for led in self._leds:
            led.off()

    def on(self, value = 0.8):
        ''' turns on the led with given value (can be a tuple) '''
        for led in self._leds:
            led.on()

        if type(value) == tuple:
            self.set(value)
        else:
            self.set((value,value,value))
