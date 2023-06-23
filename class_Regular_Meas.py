import time
import pygame
from playsound import playsound
import class_Measurement
import threading
import class_COP
import class_Pedometer
from datetime import datetime
import class_Meas_To_File


class Regular_Meas:
    COP_TIMEOUT = 0.5  # TODO: to check with Aviv
    PEDOMETER_TIMEOUT = 10  # TODO: to check with Aviv

    def __init__(self, meas1: class_Measurement.Measurement, meas2: class_Measurement.Measurement):
        self.meas1 = meas1
        self.meas2 = meas2
        self.COP_flag = 0
        self.Pedometer_flag = 0
        self.trigger = 0

    def regular_meas_collector(self, max_cop_value, min_cop_value, left_pace_calibration, right_pace_calibration):
        thread1 = threading.Thread(target=self.meas1.get_data_loop)
        thread2 = threading.Thread(target=self.meas2.get_data_loop)
        thread3 = threading.Thread(target=self.timed_COP, args=(max_cop_value, min_cop_value,))
        thread4 = threading.Thread(target=self.timed_pedometer, args=(left_pace_calibration, right_pace_calibration,))
        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()
        try:
            while True:
                time.sleep(0.1)
                if self.COP_flag and self.Pedometer_flag:
                    self.trigger = 1
                    print("A fall has been detected")
                    # TODO: connecting to tomer system
                pass
        except KeyboardInterrupt:
            self.meas1.stop_receive_thread = True
            self.meas2.stop_receive_thread = True
            thread1.join()
            thread2.join()
            thread3.join()
            thread4.join()
            self.meas1.serial_port.close()
            self.meas2.serial_port.close()

    # def regular_meas_save_data(self):
    #     while not self.meas1.stop_receive_thread:
    #         time.sleep(self.SAVE_TO_FILE_TIMEOUT)
    #         meas_to_file = self.meas1.dict.remove_half()
    #         # df_list = self.meas1.dict.meas_to_file()
    #         self.meas1.dict.meas_to_file(meas_to_file)
        # return df_list

    def timed_COP(self, max_cop_value, min_cop_value):
        meas_list = []
        max_range = 1.13*max_cop_value
        min_range = 1.13*min_cop_value
        file_time_stamp = f'{datetime.now():%d-%m-%Y %H-%M-%S}'
        meas_to_file = class_Meas_To_File.Meas_To_File()
        while not self.meas1.stop_receive_thread:
            time.sleep(self.COP_TIMEOUT)
            stop_time = time.time()
            start_time = stop_time - self.COP_TIMEOUT
            meas_list = self.meas1.dict.time_range_dict(start_time, stop_time)
            cop = class_COP.COP()
            cop_x_value = 0
            cop_y_value = 0
            cop_data_to_file = [0, 0, 0]
            cop_data_to_file[0] = start_time
            left_df, right_df = meas_list
            for right_row, left_row in zip(right_df.values, left_df.values):
                cop_x_value = cop_x_value + cop.total_center_of_pressure_just_x(right_row, left_row)
                cop_y_value = cop_y_value + cop.total_center_of_pressure_just_y(right_row, left_row)
            cop_x_value = cop_x_value/min(len(right_df.values), len(left_df.values))
            cop_y_value = cop_y_value / min(len(right_df.values), len(left_df.values))
            cop_data_to_file[1] = cop_x_value
            cop_data_to_file[2] = cop_y_value
            meas_to_file.COP_file_add_row(file_time_stamp, cop_data_to_file)
            # print(f'cop: {cop_value}')
            if (cop_x_value >= max_range) or (cop_x_value <= min_range):
                self.COP_flag = 1
            else:
                self.COP_flag = 0

    def timed_pedometer(self, left_pace_calibration, right_pace_calibration):
        meas_list = []
        ped_list = []
        normal_right_pace = 0.878*right_pace_calibration
        normal_left_pace = 0.878*left_pace_calibration
        file_time_stamp = f'{datetime.now():%d-%m-%Y %H-%M-%S}'
        meas_to_file = class_Meas_To_File.Meas_To_File()
        while not self.meas1.stop_receive_thread:
            time.sleep(self.PEDOMETER_TIMEOUT)
            stop_time = time.time()
            start_time = stop_time - self.PEDOMETER_TIMEOUT
            meas_list = self.meas1.dict.time_range_dict_for_ped(start_time, stop_time)
            ped = class_Pedometer.Pedometer()
            ped_data_to_file = [0, 0, 0]
            ped_data_to_file[0] = start_time
            left_pace, right_pace = ped.walking_pace(meas_list, self.PEDOMETER_TIMEOUT)
            ped_data_to_file[1] = left_pace
            ped_data_to_file[2] = right_pace
            meas_to_file.PED_file_add_row(file_time_stamp, ped_data_to_file)
            if (left_pace < normal_left_pace) or (right_pace < normal_right_pace):
                self.Pedometer_flag = 1
            else:
                self.Pedometer_flag = 0

    # def step_threshold(self, data, mean, threshold, std_dev):
    #     ped = class_Pedometer.Pedometer()
    #     real_time = data[0]
    #     sensor1 = data[1]
    #     sensor2 = data[2]
    #     sensor3 = data[3]
    #     sensor4 = data[4]
    #     count = 0
    #     ped_value = ped.sensor_sqrt(sensor1, sensor2, sensor3, sensor4)
    #     if abs(ped_value - mean) > threshold * std_dev:
    #         count = 1
    #     return count, real_time

    # def step_time(self, data, mean, threshold, std_dev):
