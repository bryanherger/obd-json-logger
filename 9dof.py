#!/usr/bin/python3

# data capture support for 9-DOF ACCEL/MAG/GYRO+TEMP BREAKOUT BOARD - LSM9DS1 from https://www.adafruit.com/product/3387
# install Adafruit libraries: sudo pip3 install adafruit-circuitpython-lsm9ds1
# this file adapted from Adafruit example at https://github.com/adafruit/Adafruit_CircuitPython_LSM9DS1/blob/master/examples/lsm9ds1_simpletest.py
# Will print the acceleration, magnetometer, and gyroscope values every 0.25 second.
import time
import board
import busio
import adafruit_lsm9ds1
import json
import math
import obd
import time

sessionId = math.floor(time.time())
vehicleId = "subaru"
sourceFile = open('/home/pi/9dof-'+str(sessionId)+'.json', 'a')

# I2C connection:
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)

#SPI connection:
# from digitalio import DigitalInOut, Direction
# spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
# csag = DigitalInOut(board.D5)
# csag.direction = Direction.OUTPUT
# csag.value = True
# csm = DigitalInOut(board.D6)
# csm.direction = Direction.OUTPUT
# csm.value = True
# sensor = adafruit_lsm9ds1.LSM9DS1_SPI(spi, csag, csm)

# Main loop will read the acceleration, magnetometer, gyroscope, Temperature
# values every second and print them out.
while True:
    ts = math.floor(time.time())
    obdDict = {}
    obdDict["vehicle"] = vehicleId
    obdDict["sessionId"] = str(sessionId)
    obdDict["timestamp"] = str(ts)
    # Read acceleration, magnetometer, gyroscope, temperature.
    accel_x, accel_y, accel_z = sensor.acceleration
    mag_x, mag_y, mag_z = sensor.magnetic
    gyro_x, gyro_y, gyro_z = sensor.gyro
    temp = sensor.temperature
    # Print values.
    # print('Acceleration (m/s^2): ({0:0.3f},{1:0.3f},{2:0.3f})'.format(accel_x, accel_y, accel_z))
    # print('Magnetometer (gauss): ({0:0.3f},{1:0.3f},{2:0.3f})'.format(mag_x, mag_y, mag_z))
    # print('Gyroscope (degrees/sec): ({0:0.3f},{1:0.3f},{2:0.3f})'.format(gyro_x, gyro_y, gyro_z))
    # print('Temperature: {0:0.3f}C'.format(temp))
    # print JSON
    obdDict["accel_x"] = accel_x
    obdDict["accel_y"] = accel_y
    obdDict["accel_z"] = accel_z
    obdDict["mag_x"] = mag_x
    obdDict["mag_y"] = mag_y
    obdDict["mag_z"] = mag_z
    obdDict["gyro_x"] = gyro_x
    obdDict["gyro_y"] = gyro_y
    obdDict["gyro_z"] = gyro_z
    obdDict["temp_C"] = temp
    obdJson = json.dumps(obdDict)
    print(obdJson, file = sourceFile)
    sourceFile.flush()
    # Delay for a second.
    time.sleep(0.25)
