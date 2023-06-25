import serial
import time
import class_IMU_dict
import class_Meas_To_File
from datetime import datetime


class Measurement:
    OUTPUT_DELIMITER = ':'
    TIMEOUT = 45  # the calibration time

    def __init__(self, serial_port: serial.Serial, dict: class_IMU_dict.IMU_dict):
        self.serial_port = serial_port
        self.dict = dict
        self.stop_receive_thread = False

    def read_line_from_serial(self):
        # reading a single data line from the serial port
        try:
            return self.serial_port.readline().decode()
        except UnicodeDecodeError:
            print('error')
            return -1

    def get_data(self):
        while self.serial_port.inWaiting() == 0:  # passing as long as we don't get data
            pass
        # Read a single data line from the serial port
        output = self.read_line_from_serial()  # reading a single data line from the serial port
        # Check if there was an error while reading the data line
        if output == -1:
            return -1
        if not any(output.startswith(key) for key in self.dict.imu_dict) or not output.endswith('\r\n'):
            # when we have a timing issue, and we get partial data
            print(f'error in data: {output=}')
            return -1
        splitted_output = output.split(self.OUTPUT_DELIMITER)  # separates the data
        return splitted_output

    def get_data_loop(self):
        # reading data in loop
        file_time_stamp = f'{datetime.now():%d-%m-%Y %H-%M-%S}'
        info_list = []
        meas_to_file = class_Meas_To_File.Meas_To_File()
        while not self.stop_receive_thread:
            # Get a single data line from the serial port
            data = self.get_data()
            # Check if there was an error while getting the data line
            if data == -1:
                continue
            # Append the data to the info_list and get the updated list
            info_list = self.dict.dict_append(data, file_time_stamp)
            if info_list == [0, 0, 0]:
                continue
            # Add the info_list as a row to the measurement file
            meas_to_file.regular_measurement_add_row(info_list)

    def get_data_loop_cal(self):
        # reading calibration data in loop
        file_time_stamp = f'{datetime.now():%d-%m-%Y %H-%M-%S}'
        # Get the initial time for timeout calculation
        initial_time = time.time()
        info_list = []
        meas_to_file = class_Meas_To_File.Meas_To_File()
        while True:
            # Check if the timeout has been reached
            if time.time() > self.TIMEOUT + initial_time:  # the calibration measurement is for a specific time period
                break
            # Get a single data line from the serial port
            data = self.get_data()
            # Check if there was an error while getting the data line
            if data == -1:
                continue
            # Append the data to the info_list and get the updated list
            info_list = self.dict.dict_append(data, file_time_stamp)
            # Check if the info_list contains valid data
            if info_list == [0, 0, 0]:
                continue
            # Add the info_list as a row to the calibration measurement file
            meas_to_file.calibration_add_row(info_list)
