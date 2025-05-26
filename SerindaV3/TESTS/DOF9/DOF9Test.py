# sudo pip3 install adafruit-circuitpython-fxos8700
# sudo pip3 install adafruit-circuitpython-fxas21002c
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
 
# Simple demo of the FXAS21002C gyroscope.
# Will print the gyroscope values every second.
import time
 
import board
import busio
 
import adafruit_fxas21002c
import adafruit_fxos8700

import requests
 
# Initialize I2C bus and device.
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_fxas21002c.FXAS21002C(i2c)
sensor2 = adafruit_fxos8700.FXOS8700(i2c)

# Optionally create the sensor with a different gyroscope range (the
# default is 250 DPS, but you can use 500, 1000, or 2000 DPS values):
# sensor = adafruit_fxas21002c.FXAS21002C(i2c, gyro_range=adafruit_fxas21002c.GYRO_RANGE_500DPS)
# sensor = adafruit_fxas21002c.FXAS21002C(i2c, gyro_range=adafruit_fxas21002c.GYRO_RANGE_1000DPS)
# sensor = adafruit_fxas21002c.FXAS21002C(i2c, gyro_range=adafruit_fxas21002c.GYRO_RANGE_2000DPS)

# data = {'api_dev_key':API_KEY,
#        'api_option':'paste',
#        'api_paste_code':source_code,
#        'api_paste_format':'python'}

data = {}

# Main loop will read the gyroscope values every second and print them out.
while True:
    # Read gyroscope.
    gyro_x, gyro_y, gyro_z = sensor.gyroscope
    accel_x, accel_y, accel_z = sensor2.accelerometer
    mag_x, mag_y, mag_z = sensor2.magnetometer

    API_ENDPOINT = "http://192.168.0.11:8000/dofdata?gyrox={0:0.3f}&gyroy={0:0.3f}&gyroz={0:0.3f}&accelx={0:0.3f}&accely={0:0.3f}&accelz={0:0.3f}&magx={0:0.3f}&magy={0:0.3f}&magz={0:0.3f}".format(gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z, mag_x, mag_y, mag_z)

    # print("Gyroscope (radians/s): ({0:0.3f},  {1:0.3f},  {2:0.3f})".format(gyro_x, gyro_y, gyro_z))
    # print('Acceleration (m/s^2): ({0:0.3f}, {1:0.3f}, {2:0.3f})'.format(accel_x, accel_y, accel_z))
    # print('Magnetometer (uTesla): ({0:0.3f}, {1:0.3f}, {2:0.3f})'.format(mag_x, mag_y, mag_z))

    # sending post request and saving response as response object
    r = requests.post(url=API_ENDPOINT, data=data)

    # Delay for a second.
    time.sleep(1.0)
