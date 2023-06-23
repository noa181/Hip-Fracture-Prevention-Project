import time
import pygame
import class_Measurement
import threading
import class_COP
import class_Pedometer
import pandas


class Calibration:

    def __init__(self, meas1: class_Measurement.Measurement, meas2: class_Measurement.Measurement):
        self.meas1 = meas1
        self.meas2 = meas2

    def nonblocking_play_file(self, file):
        pygame.mixer.music.load(file)
        pygame.mixer.music.play(0)

    def blocking_play_file(self, file):
        pygame.mixer.music.load(file)
        pygame.mixer.music.play(1)  # Play the file once
        while pygame.mixer.music.get_busy():
            continue
        pygame.mixer.music.stop()

    def calibration(self):
        pygame.init()
        pygame.mixer.init()
        self.blocking_play_file('walking_calibration_intro.mp3')
        time.sleep(1)
        self.nonblocking_play_file('starting_to_calibrate.mp3')  # need to find other mp3 file
        thread1 = threading.Thread(target=self.meas1.get_data_loop_cal)
        thread2 = threading.Thread(target=self.meas2.get_data_loop_cal)
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
        self.blocking_play_file('calibration_complete_successfully.mp3')
        # TODO: to add a check for good calibration and audio if failed
        pygame.mixer.music.stop()
        pygame.quit()

    def calibration_calc(self):
        # TODO: think what will happened if the sole isn't on the foot
        self.calibration()
        df_list = self.create_df_list_for_calibration()
        cop = class_COP.COP()
        max_cop_value = 0
        min_cop_value = 0
        left_df, right_df = df_list
        for right_row, left_row in zip(right_df.values, left_df.values):
            # Send the row to your custom function
            result = cop.total_center_of_pressure_just_x(right_row, left_row)
            # Update the maximum value if necessary
            if result > max_cop_value:
                max_cop_value = result
            # Update the minimum value if necessary
            if result < min_cop_value:
                min_cop_value = result
        # print(max_cop_value)
        # print(min_cop_value)
        df_list_ped = self.create_df_list_for_ped_calibration()
        ped = class_Pedometer.Pedometer()
        left_pace, right_pace = ped.walking_pace(df_list_ped, self.meas1.TIMEOUT)
        # print(left_pace)
        # print(right_pace)
        return max_cop_value, min_cop_value, left_pace, right_pace

    def create_df_list_for_calibration(self):
        df_list = []
        for imu, measurements_list in self.meas1.dict.imu_dict.items():
            if not measurements_list:
                continue
            for i in range(len(measurements_list)-1):
                if len(measurements_list[i]) != 13:
                    measurements_list.pop(i)
            df = pandas.DataFrame(measurements_list, columns=self.meas1.dict.COLUMNS)
            df = df.drop('actual_time', axis=1)
            df = df.drop('time', axis=1)
            df = df.drop('heading', axis=1)
            df = df.drop('pitch', axis=1)
            df = df.drop('roll', axis=1)
            df = df.drop('ax', axis=1)
            df = df.drop('ay', axis=1)
            df = df.drop('az', axis=1)
            df = df.drop('sensor5', axis=1)
            df = df.astype(float)
            df.drop(df.index[0])
            df_list.append(df)
        return df_list

    def create_df_list_for_ped_calibration(self):
        df_list = []
        for imu, measurements_list in self.meas1.dict.imu_dict.items():
            if not measurements_list:
                continue
            for i in range(len(measurements_list)-1):
                if len(measurements_list[i]) != 13:
                    measurements_list.pop(i)
            df = pandas.DataFrame(measurements_list, columns=self.meas1.dict.COLUMNS)
            df = df.drop('time', axis=1)
            df = df.drop('heading', axis=1)
            df = df.drop('pitch', axis=1)
            df = df.drop('roll', axis=1)
            df = df.drop('ax', axis=1)
            df = df.drop('ay', axis=1)
            df = df.drop('az', axis=1)
            df = df.drop('sensor5', axis=1)
            df = df.astype(float)
            df.drop(df.index[0])
            df_list.append(df)
        return df_list
