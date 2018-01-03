from w1thermsensor import W1ThermSensor
import time
import RPi.GPIO as GPIO

HEATER_PIN  = 26

TEMP_OFF = 45
TEMP_ON  = 40

TIME_PER_DISPLAY = 10
TIME_PER_LOG     = 5 * 60

heaterPin = 26
heaterState = False
heaterMsg = 'OFF'

sensor = W1ThermSensor()

GPIO.setmode (GPIO.BCM)
GPIO.setup (heaterPin, GPIO.OUT)
GPIO.output (heaterPin, GPIO.LOW)

LOGFILE = "/home/pi/ph/thermoheater.log"

time_next_log = time.time()
time_next_display = time.time()

def c_to_f (temp_c):
	return (temp_c * 9.0 / 5.0) + 32.0

def log_temp (temp_c, htr_msg):
	msg = '%s %7.2f C  %7.2f F  Htr %s' % (time.strftime ('%Y:%m:%d:%H:%M:%S'), temp_c, c_to_f (temp_c), htr_msg)
	with open (LOGFILE, "a+") as logfile:
		logfile.write (msg + '\r\n')

print ('Thermostatic Heater')
print ('  Reading one-wire temperature sensor on pin 4')
print ('  And controlling heater on relay pin %d' % (heaterPin))
c = sensor.get_temperature()
print ('  Current temp: %7.2f C %7.2f F' % (c, c_to_f(c)))
print ('')
print ('  The heater comes on at %7.2f F' % (TEMP_ON))
print ('  And turns off again at %7.2f F' % (TEMP_OFF))
print ('')

while True:
	temp_celsius = sensor.get_temperature()
	temp_fahrenheit = c_to_f (temp_celsius)
	if temp_fahrenheit > TEMP_OFF and heaterState:
		# was on, reached off temp, so turn it off
		heaterState = False
		heaterMsg = 'OFF'
		GPIO.ouput (heaterPin, GPIO.LOW)
		print ("%s Heater Turned Off" % (time.strftime ("%H:%M:%S")))
	if temp_fahrenheit <= TEMP_ON and not heaterState:
		# was off, reached on temp, so turn it on
		heaterState = True
		heaterMsg = 'ON'
		GPIO.output (heaterPin, GPIO.HIGH)
		print ("%s Heater Turned On" % (time.strftime ("%H:%M:%S")))
	t = time.time()
	if t >= time_next_log:
		log_temp (temp_celsius, heaterMsg)
		time_next_log = t + TIME_PER_LOG
	if t >= time_next_display:
		print ("%s temp  %7.2f C, %7.2f F   heater %s" % (time.strftime("%H:%M:%S"), temp_celsius, temp_fahrenheit, heaterMsg))
		time_next_display = t + TIME_PER_DISPLAY
	time.sleep(0.2)
