# MPU6050 DMP Library
## Abstract
This library is primarily derived from the contributions of Geir Istad and has been released as a pip-installable package. This library aims to simplify the use of the digital motion processor (DMP) inside the inertial measurement unit (IMU), along with other motion data. The main focus of this package is on providing the orientation of the device in space as a quaternion, which is convertible to Euler angles. The resulting data are processed and denoised using an extended Kalman filter (EKF), inside the DMP module.

To install this package, execute the following command:

`pip install mpu6050`

My main contributions to this library are towards enhancing the DMP results, providing detailed examples, describing the usage, and making the library pip-installable. Apart from the great work done by Geir Istad, there were some issues encountered in practice.

The enhancements are listed below:
- Quaternion to Euler angles conversion (roll, pitch, yaw) enhanced using the SciPy library
- Linear (world-frame) acceleration rewritten using new formulas, based on the quaternion
- Better access to the DMP frequency
- Comprehensible, practical examples with detailed explanation
- pip-installable

**This library is tested on the Nvidia Jetson with the I2C communication protocol.**

This library can also be utilized for the MPU9250. However, the magnetometer data provided by the AK8963 module are not accessible.

## Introduction
The MPU6050 is a versatile accelerometer gyroscope chip with six axes of sensing capability and a 16-bit measurement resolution. This chip is widely popular due to its high accuracy and cost-effectiveness, making it a preferred choice among DIY enthusiasts and even in commercial products. The combination of gyroscope and accelerometers in the MPU6050 forms what is known as an Inertial Measurement Unit (IMU), which finds applications in various fields like mobile phones, tablets, robotics, and more.
The Digital Motion Processor (DMP) is a powerful feature of certain motion sensing chips, such as the MPU6050, which is a versatile accelerometer and gyroscope chip with six axes of sensing capability and a 16-bit measurement resolution. The DMP is an onboard processor that handles complex sensor processing and fusion, offloading these tasks from the microcontroller. This allows for faster and more accurate sensor readings, which is particularly important in applications where real-time motion tracking is crucial.

## Main Contributions
Here, we will discuss the key changes in this library and the enhancements made to improve usability and access to MPU6050 features.
### 1. Euler angles
One of the practical outputs from the DMP is the quaternion, which precisely represents the IMU's orientation in space. While quaternions are useful, there is often a need for Euler angles, which include roll, pitch, and yaw.

The previous library had issues with the conversion from quaternions to Euler angles, resulting in inaccuracies. The new conversion method utilizes scipy for improved accuracy. Through extensive experimentation on Nvidia Jetson, the results were found to be satisfactory.

### 2. World-frame acceleration
The acceleration data acquired from an IMU is represented in a body frame, aligning with the IMU's axes. However, in the realm of Inertial Navigation Systems (INS), having access to a world frame acceleration vector is essential for accurate navigation. The illustration below depicts the orientation of the world frame and body frame axes:

<p align="center"><img src="https://ars.els-cdn.com/content/image/3-s2.0-B9780128131893000162-f16-01-9780128131893.jpg"></p>

The rotation of a vector using a quaternion is achieved through the following formula:

$$A_p=q\times A\times q^*$$

where $q^*$ represents the conjugate of the quaternion q, and $A_p$ denotes the rotated original vector $A$.

Through this method, a reliable world frame acceleration is provided. For example, in a stationary situation with any orientation in space, this method gives $(0,0,g)$ as the acceleration vector. The old library had mathematical issues with calculating the world frame acceleration, and the results were impractical.

Note that this method works best with the DMP frequency at 40Hz or lower. By configuring the DMP at a higher frequency, the effect of the noise will not be negligible.

**Since the yaw is relative to the initial heading of the IMU, it must be rotated according to a heading modifier.**

### 3. Access to the DMP frequency
To set the frequency of the DMP in the old library, one had to refer to the MPU Constants and change the registers to set the frequency of the DMP at a specific value. Here, by assigning a value to the MPU module, the frequency is automatically configured. **Please note that the program has to be fast enough to keep up with the DMP frequency. Otherwise, the FIFO registers will overflow.**

It is worth noting that the structure of the library has slightly changed for the ease of use (i.e., waiting for the FIFO data).

### 4. Examples
Three examples are provided with detailed explanations on the calculations made to achieve the accurate data from the MPU6050 sensor. The examples are easy to read and without any confusion.

* **example0_raw_data**: Provides the accelerometer and gyroscope data, before and after the DMP fusion. Detailed explanations on how to calculate the values are also provided.
* **example1_rollpitchyaw**: Provides the roll, pitch and yaw rotations in degrees. Note that the yaw is relative to the initial heading of the IMU. Thus, it has an offset and may have a small drift over time.
* **example2_linear_accel**: Provides the world-frame acceleration. Since the yaw is relative to the initial heading of the IMU, the acceleration data must be rotated according to a heading modifier.

### 5. Available on PyPI
I am honored to state that this comprehensive library is now available on PyPI, encompassing all the features explained, which can be accessed by executing a simple command:

`pip install mpu6050`

This command will also install the 'quat' and 'smbus' libraries, which are essential for the proper functioning of the library.
For more details on the 'quat' library, a concise library for working with quaternions and vectors (also developed by Geir Istad), please refer to the GitHub repository [quat](https://github.com/OmidAlek/quat).