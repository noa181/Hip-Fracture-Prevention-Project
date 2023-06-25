import time
import class_Measurement
import threading
import class_COP
import class_Pedometer
from datetime import datetime
import class_Meas_To_File


class Regular_Meas:
    # the time between each COP calculation
    COP_TIMEOUT = 0.5
    # the time between each walking pace calculation
    PEDOMETER_TIMEOUT = 10

    def __init__(self, meas1: class_Measurement.Measurement, meas2: class_Measurement.Measurement):
        self.meas1 = meas1
        self.meas2 = meas2
        self.COP_flag = 0
        self.Pedometer_flag = 0
        self.trigger = 0

    def regular_meas_collector(self, max_cop_value, min_cop_value, left_pace_calibration, right_pace_calibration):
        # Start data collection threads for the measurements
        thread1 = threading.Thread(target=self.meas1.get_data_loop)
        thread2 = threading.Thread(target=self.meas2.get_data_loop)
        # Start threads for COP and Pedometer calculations
        thread3 = threading.Thread(target=self.timed_COP, args=(max_cop_value, min_cop_value,))
        thread4 = threading.Thread(target=self.timed_pedometer, args=(left_pace_calibration, right_pace_calibration,))
        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()
        try:
            while True:
                time.sleep(0.1)
                # Check if both COP and Pedometer cross the threshold values and there is a near fall
                if self.COP_flag and self.Pedometer_flag:
                    self.trigger = 1
                    print("A fall has been detected")
                    # TODO: connecting to the mechanical system in the future
                pass
        except KeyboardInterrupt:
            self.meas1.stop_receive_thread = True
            self.meas2.stop_receive_thread = True
            # Stop the data collection and calculation threads and wait for them to complete
            thread1.join()
            thread2.join()
            thread3.join()
            thread4.join()
            # Close the serial ports
            self.meas1.serial_port.close()
            self.meas2.serial_port.close()

    def timed_COP(self, max_cop_value, min_cop_value):
        meas_list = []
        max_range = 1.13 * max_cop_value  # Maximum COP range threshold
        min_range = 1.13 * min_cop_value  # Minimum COP range threshold
        file_time_stamp = f'{datetime.now():%d-%m-%Y %H-%M-%S}'  # Current timestamp for file name
        meas_to_file = class_Meas_To_File.Meas_To_File()
        while not self.meas1.stop_receive_thread:
            time.sleep(self.COP_TIMEOUT)  # Wait for COP_TIMEOUT duration
            stop_time = time.time()  # Get the current time
            start_time = stop_time - self.COP_TIMEOUT  # Calculate the start time of the time range
            # Retrieve the IMU measurement data within the specified time range
            meas_list = self.meas1.dict.time_range_dict(start_time, stop_time)
            cop = class_COP.COP()
            cop_x_value = 0
            cop_y_value = 0
            cop_data_to_file = [0, 0, 0]
            cop_data_to_file[0] = start_time
            left_df, right_df = meas_list  # Separate the left and right IMU measurement data
            # Calculate COP values for each measurement pair
            for right_row, left_row in zip(right_df.values, left_df.values):
                cop_x_value = cop_x_value + cop.total_center_of_pressure_just_x(right_row, left_row)
                cop_y_value = cop_y_value + cop.total_center_of_pressure_just_y(right_row, left_row)
            # Calculate the average COP values
            cop_x_value = cop_x_value/min(len(right_df.values), len(left_df.values))
            cop_y_value = cop_y_value / min(len(right_df.values), len(left_df.values))
            cop_data_to_file[1] = cop_x_value
            cop_data_to_file[2] = cop_y_value
            meas_to_file.COP_file_add_row(file_time_stamp, cop_data_to_file)  # Write COP data to the file
            if (cop_x_value >= max_range) or (cop_x_value <= min_range):
                self.COP_flag = 1  # Set COP flag to indicate a fall detection
            else:
                self.COP_flag = 0  # Reset COP flag

    def timed_pedometer(self, left_pace_calibration, right_pace_calibration):
        meas_list = []
        ped_list = []
        normal_right_pace = 0.878 * right_pace_calibration  # Normalized right pace threshold
        normal_left_pace = 0.878 * left_pace_calibration  # Normalized left pace threshold
        file_time_stamp = f'{datetime.now():%d-%m-%Y %H-%M-%S}'  # Current timestamp for file name
        meas_to_file = class_Meas_To_File.Meas_To_File()
        while not self.meas1.stop_receive_thread:
            time.sleep(self.PEDOMETER_TIMEOUT)  # Wait for PEDOMETER_TIMEOUT duration
            stop_time = time.time()  # Get the current time
            start_time = stop_time - self.PEDOMETER_TIMEOUT  # Calculate the start time of the time range
            # Retrieve the IMU measurement data within the specified time range
            meas_list = self.meas1.dict.time_range_dict_for_ped(start_time, stop_time)
            ped = class_Pedometer.Pedometer()
            ped_data_to_file = [0, 0, 0]
            ped_data_to_file[0] = start_time
            left_pace, right_pace = ped.walking_pace(meas_list, self.PEDOMETER_TIMEOUT)  # Calculate walking pace
            ped_data_to_file[1] = left_pace
            ped_data_to_file[2] = right_pace
            meas_to_file.PED_file_add_row(file_time_stamp, ped_data_to_file)  # Write pedometer data to the file
            if (left_pace < normal_left_pace) or (right_pace < normal_right_pace):
                self.Pedometer_flag = 1  # Set Pedometer flag to indicate a fall detection
            else:
                self.Pedometer_flag = 0  # Reset Pedometer flag
