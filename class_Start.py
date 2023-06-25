import class_Measurement
import class_IMU_dict
import serial
import class_Calibration
import class_Regular_Meas
from datetime import datetime
import class_Meas_To_File


class Start:

    def calling_calibration(self):
        imu_dict = class_IMU_dict.IMU_dict()
        # Create 2 instances of the Measurement class with the same dict, the port number may change with different PCs
        meas1 = class_Measurement.Measurement(serial.Serial(port="COM3", baudrate=57600), imu_dict)
        meas2 = class_Measurement.Measurement(serial.Serial(port="COM4", baudrate=57600), imu_dict)
        cal = class_Calibration.Calibration(meas1, meas2)
        # Perform calibration calculations and retrieve the values
        max_cop_value, min_cop_value, left_pace, right_pace = cal.calibration_calc()
        # Generate a file timestamp using the current date and time
        file_time_stamp = f'{datetime.now():%d-%m-%Y %H-%M-%S}'
        meas_to_file = class_Meas_To_File.Meas_To_File()
        data = [max_cop_value, min_cop_value, left_pace, right_pace]
        # Save the calibration values to a file with the generated timestamp
        meas_to_file.calibration_values_to_file(file_time_stamp, data)
        # Return the calibration values
        return max_cop_value, min_cop_value, left_pace, right_pace

    def calling_regular_meas(self):
        # Call the calling_calibration method to obtain the calibration values
        max_cop_value, min_cop_value, left_pace_calibration, right_pace_calibration = self.calling_calibration()
        imu_dict2 = class_IMU_dict.IMU_dict()
        # Create 2 instances of the Measurement class with the same dict, the port number may change with different PCs
        meas3 = class_Measurement.Measurement(serial.Serial(port="COM3", baudrate=57600), imu_dict2)
        meas4 = class_Measurement.Measurement(serial.Serial(port="COM4", baudrate=57600), imu_dict2)
        reg_meas = class_Regular_Meas.Regular_Meas(meas3, meas4)
        # Collect regular measurements using the calibration values
        reg_meas.regular_meas_collector(max_cop_value, min_cop_value, left_pace_calibration, right_pace_calibration)
