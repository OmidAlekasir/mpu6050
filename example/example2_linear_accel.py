__author__ = 'Majid Alekasir' # majid.alekasir@gmail.com

### Some changes are applied to the original library by 'Geir Istad' ###
### The changes aim to enhance the results of *roll-pitch-yaw* and *linear acceleration* ###
### Some changes are made for the ease of use ###
### You need to install 'Scipy library' which is used in 'DMP_get_roll_pitch_yaw' function. The former function was not accurate and was giving improper results ###

"""
MPU6050 Python I2C Class - MPU6050 example usage
Copyright (c) 2015 Geir Istad

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from mpu6050 import MPU6050

i2c_bus = 1
device_address = 0x68
freq_divider = 0x04

# Make an MPU6050
mpu = MPU6050(i2c_bus, device_address, freq_divider)

# Initiate your DMP
mpu.dmp_initialize()
mpu.set_DMP_enabled(True)

packet_size = mpu.DMP_get_FIFO_packet_size()
FIFO_buffer = [0]*64

g = 9.8 # gravity acceleration (m/s^2)

while True: # infinite loop
    if mpu.isreadyFIFO(packet_size): # Check if FIFO data are ready to use...
        
        FIFO_buffer = mpu.get_FIFO_bytes(packet_size) # get all the DMP data here

        # raw acceleration
        accel = mpu.get_acceleration()
        accel.x = accel.x * 2*g / 2**15
        accel.y = accel.y * 2*g / 2**15
        accel.z = accel.z * 2*g / 2**15
        
        # quaternion
        q = mpu.DMP_get_quaternion_int16(FIFO_buffer)
        q.normalize()

        # world-frame acceleration vectors (practical for INS)
        accel_linear = mpu.get_linear_accel(accel, q)
        Ax_linear = round(accel_linear.x, 2)
        Ay_linear = round(accel_linear.y, 2)
        Az_linear = round(accel_linear.z, 2)
        
        #
        print('linear Ax: ' + str(Ax_linear))
        print('linear Ay: ' + str(Ay_linear))
        print('linear Az: ' + str(Az_linear))
        print('\n')

        ### About DMP frequency ###
        # For optimal results in INS (Inertial Navigation System), it is advisable to set the frequency of the Digital Motion Processor (DMP) to 40 Hz or lower.
        # This configuration yields a less noisy quaternion vector and reduces the occurrence of FIFO overflows.
        # Note that the "get_linear_accel" function can also be used for the acceleration vector provided by the DMP.