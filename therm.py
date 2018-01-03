from w1thermsensor import W1ThermSensor
import time

#for sensor in W1ThermSensor.get_available_sensors():
#    print ("Sensor %s temperature %.2f" % (sensor.id, sensor.get_temperature()))
    
sensor = W1ThermSensor()

while True:
	temp_celsius = sensor.get_temperature()
	temp_fahrenheit = (temp_celsius * 9/5) + 32
	print ("%s temp  %7.2f C, or %7.2f F" % (time.strftime("%H:%M:%S"), temp_celsius, temp_fahrenheit))
	time.sleep(5.0)
