from gpiozero import PWMOutputDevice
from gpiozero import DigitalOutputDevice
from signal import pause
from time import sleep
from gpiozero import Device
from motorGPIOTest import Motor, DriveTrain

stbyLeft = DigitalOutputDevice(4)
stbyRight = DigitalOutputDevice(0)

fL = Motor(2, 3, 12, stbyLeft)
bL = Motor(17, 27, 13, stbyLeft)

bR = Motor(22, 10, 18, stbyRight)
fR = Motor(9, 11, 19, stbyRight)


bot = DriveTrain(fL, fR, bL, bR)


bot.forward(0.4, 1)
