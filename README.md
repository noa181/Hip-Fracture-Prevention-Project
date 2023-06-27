# Hip-Fracture-Prevention-Project
The project's goal is to develop a smart system to prevent falls that could cause hip fracture among stroke survivors. 
We focused on stroke survivors that suffers from hemiparesis with moderate function who live in the community and use walking aids.
The system integrates a smart sensor system in the shoe insoles and a mechanical system of a smart walking cane.
The mechanical system:
![image](https://github.com/noa181/Hip-Fracture-Prevention-Project/assets/130772888/16b513a6-5b39-4828-a069-7e0c13c458e6)

The insole system:
![image](https://github.com/noa181/Hip-Fracture-Prevention-Project/assets/130772888/d377d088-ffaf-44c6-8e5d-2a79a24ee451)
Each shoe has a separate sensor system that includes:
4 pressure sensors (FSR), IMU (accelerometer, magnetometer, gyroscope) and a microcontroller connected to a rechargeable battery that wirelessly transmits the data.
As part of the project, we are using the data that was received from the sensors, to identify changes in the characteristics of the patient's gait, that can indicate a danger of falling in a future walking cycle. 
we chose to focus on two gait characteristics - decrease in the walking speed and a rapid deviation of the center of pressure to the side.
When the sensor system detects a future fall, it will send a signal to the mechanical system to activate it, and then the smart walking cane will open its support legs. 
the system block diagram:
![image](https://github.com/noa181/Hip-Fracture-Prevention-Project/assets/130772888/be51e72f-09a3-4349-9a5b-0f7bfa3ce0e3)

the code is devided to 2 main parts:
1. arduino code (C++) for the micro-controller:
   in this part we collect the measurements from all the sensors, there is initial data processing and we     send the processed data to the PC.
2. python code for PC:
   in this the we are doing the main data processing.
   this part is devided to several code files according to each file purpose.
   the data processing code scheme:
   ![image](https://github.com/noa181/Hip-Fracture-Prevention-Project/assets/130772888/1c89c14e-c83b-4aea-8d55-228ede9410af)

explanation:
main - from here we run the code, it calles the class_Start file.
class_Start - is devided to 2 main functions, one for the calibration process and one for the regular measurement process. it calles the class_Calibration file and the class_Regular_Meas file.
class_Calibration - in it we have audio instructions, calibration run and calculations for both legs simultaneously.
class_Regular_Meas - regular measurement run and calculation for both legs simultaneously, identify near fall.
the calibration and the regular measurement call this files:
class_Measurement - read the data from the sirial port and some data processing. it calles the class_IMU_dict file.
clas_IMU_dict - includes there is the dictionary that we save the data measurement in it, it also have a function that get part of the dict according to time range for the gait charecteristic calculation. the dictionary size is limited.
class_COP - COP calculation.
class_Pedometer - walking speed calculation.
class_Meas_To_File - saving the data in CSV files. the CSV files size is limited.
the CSV files are:
2 files for the data from the calibration, one for each leg.
file with calibration values that was calculated.
2 files for the data from the regular measurement, one for each leg.
file with the calculated COP from the regular measurement.
file with the calculated walking speed from the regular measurement.
if a file size exceed its size limit a new file with the same name + new index opens.









final project
https://lotanbs.wixsite.com/walk
https://drive.google.com/file/d/1Gw9kIsZNWJx-F5dWAqVrT-ABI2NpP5hU/view
https://github.com/arkadiraf/smartInSole
