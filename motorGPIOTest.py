from gpiozero import PWMOutputDevice
from gpiozero import DigitalOutputDevice
from signal import pause
from time import sleep
from gpiozero import Device

from ollama import chat


class Motor:
	
	def __init__(self, in1, in2, INpwm, INstby):
		self.input1 = DigitalOutputDevice(in1)
		self.input2 = DigitalOutputDevice(in2)
		self.stby = INstby
		self.pwm = PWMOutputDevice(INpwm)
		
	def forwardSeconds(speed, seconds):
		input1.on()
		input2.off()
		stby.on()
		pwm.value = speed
		sleep(seconds)
		pwm.value = 0.0	
	
	def forward(self, speed):
		self.input1.on()
		self.input2.off()
		self.stby.on()
		self.pwm.value = speed
	
	def reverseSeconds(speed, seconds):
		input1.off()
		input2.on()
		stby.on()
		pwm.value = speed
		sleep(seconds)
		pwm.value = 0.0	
	
	def reverse(self, speed):
		self.input1.off()
		self.input2.on()
		self.stby.on()
		self.pwm.value = speed	
	
	def stop(self):
		self.input1.off()
		self.input2.off()
		self.pwm.value = 0.0

class DriveTrain:
	fL = None
	fR = None
	bL = None
	bR = None
	
	def __init__(self, frontLeft, frontRight, backLeft, backRight):
		fL = frontLeft
		fR = frontRight
		bL = backLeft
		bR = backRight
	
	def stopAll(self):
		fR.stop()
		bL.stop()
		bR.stop()
		fL.stop()
	
	def forward(self, speed, seconds):
		fR.forward(speed)
		bL.forward(speed)
		bR.reverse(speed)
		fL.reverse(speed)
		sleep(seconds)
		self.stopAll()
	
	def reverse(self, speed, seconds):
		fR.reverse(speed)
		bL.reverse(speed)
		bR.forward(speed)
		fL.forward(speed)
		sleep(seconds)
		self.stopAll()
	
	def turnRight(self, speed, seconds):
		fR.reverse(speed)
		bL.forward(speed)
		bR.forward(speed)
		fL.forward(speed)
		sleep(seconds)
		self.stopAll()
		
	def turnLeft(self, speed, seconds):
		fR.forward(speed)
		bL.reverse(speed)
		bR.reverse(speed)
		fL.forward(speed)
		sleep(seconds)
		self.stopAll()
		
	def strafeRight(self, speed, seconds):
		fR.reverse(speed)
		bL.reverse(speed)
		bR.reverse(speed)
		fL.reverse(speed)
		sleep(seconds)
		self.stopAll()
		
	def strafeLeft(self, speed, seconds):
		fR.forward(speed)
		bL.forward(speed)
		bR.forward(speed)
		fL.forward(speed)
		sleep(seconds)
		self.stopAll()

	

stbyLeft = DigitalOutputDevice(4)
stbyRight = DigitalOutputDevice(0)

fL = Motor(2, 3, 12, stbyLeft)
bL = Motor(17, 27, 13, stbyLeft)

bR = Motor(22, 10, 18, stbyRight)
fR = Motor(9, 11, 19, stbyRight)

defaultSpeed = 0.45

bot = DriveTrain(fL, fR, bL, bR)

while True:
	instruction = input("Enter bot command: ")
	stream = chat(
		model='gemma3',
		messages=[
		{'role': 'user', 
		'content': 'You will be given an instruction and decide on appropriate actions and times. Allowed actions: driveForward, driveBackward, strafeLeft, strafeRight, turnLeft, turnRight. Return ONLY a JSON in the following format: {action : time, action : time, action : time ...} where action is a string from the Allowed actions and time is the number of seconds to do the action for, each action time pair should be seperated by a comma and there should be as many action time pairs as necessary as per the instruction. THIS IS THE INSTRUCTION:' + instruction}],
		stream=True,
	)
	print("initializing path...")
	response = ""
	for chunk in stream:
		response += (chunk['message']['content']).replace("}", "").replace("{", "").replace("\n", "").replace(":", " ").replace("```", "").replace("json", "").replace('"', '').replace(" ", "")
	path = response.split(",")
	for i in path:
		if("driveForward" in i):
			bot.forward(0.45, int(i[-1]))
			print("forward!")
		elif("driveBackward" in i):
			bot.reverse(0.45, int(i[-1]))
		elif("strafeLeft" in i):
			bot.strafeLeft(0.45, int(i[-1]))
		elif("strafeRight" in i):
			bot.strafeRight(0.45, int(i[-1]))
		elif("turnLeft" in i):
			bot.turnLeft(0.45, int(i[-1]))
		elif("turnRight" in i):
			bot.turnRight(0.45, int(i[-1]))
		else:
			print("none of the above")
	print("done!")

print(Device.pin_factory)



