import serial
import time
import class_IMU_dict
import class_Meas_To_File
from datetime import datetime


class Measurement:
    OUTPUT_DELIMITER = ':'
    TIMEOUT = 45

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
        output = self.read_line_from_serial()  # reading a single data line from the serial port
        if output == -1:
            return -1
        if not any(output.startswith(key) for key in self.dict.imu_dict) or not output.endswith('\r\n'):
            # TODO: add a condition that a line that dont have the data from all the sensors wont pass
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
            data = self.get_data()
            if data == -1:
                continue
            # print(data)
            info_list = self.dict.dict_append(data, file_time_stamp)
            if info_list == [0, 0, 0]:
                continue
            meas_to_file.regular_measurement_add_row(info_list)

    def get_data_loop_cal(self):
        # reading calibration data in loop
        file_time_stamp = f'{datetime.now():%d-%m-%Y %H-%M-%S}'  # TODO: check why it opens several files instead of one
        initial_time = time.time()
        info_list = []
        meas_to_file = class_Meas_To_File.Meas_To_File()
        while True:
            if time.time() > self.TIMEOUT + initial_time:  # the calibration measurement is for a specific time period
                break
            data = self.get_data()
            if data == -1:
                continue
            # print(data)
            info_list = self.dict.dict_append(data, file_time_stamp)
            if info_list == [0, 0, 0]:
                continue
            meas_to_file.calibration_add_row(info_list)
