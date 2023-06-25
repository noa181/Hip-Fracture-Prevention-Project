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
        pygame.mixer.music.load(file)  # Load the audio file for playback
        pygame.mixer.music.play(0)  # Play the loaded audio file (0 indicates starting from the beginning)

    def blocking_play_file(self, file):
        pygame.mixer.music.load(file)  # Load the audio file for playback
        pygame.mixer.music.play(1)  # Play the file once
        # Wait until the music playback is complete
        while pygame.mixer.music.get_busy():
            continue
        pygame.mixer.music.stop()  # Stop the playback of the music

    def calibration(self):
        pygame.init()  # Initialize the pygame module
        pygame.mixer.init()  # Initialize the mixer module for audio playback
        self.blocking_play_file('walking_calibration_intro.mp3')
        time.sleep(1)
        self.nonblocking_play_file('starting_to_calibrate.mp3')
        # Create two threads for data collection during calibration
        thread1 = threading.Thread(target=self.meas1.get_data_loop_cal)
        thread2 = threading.Thread(target=self.meas2.get_data_loop_cal)
        # Start the data collection threads
        thread1.start()
        thread2.start()
        # Wait for the data collection threads to finish
        thread1.join()
        thread2.join()
        self.blocking_play_file('calibration_complete_successfully.mp3')
        pygame.mixer.music.stop()  # Stop the audio playback
        pygame.quit()  # Quit the pygame module

    def calibration_calc(self):
        self.calibration()  # performing calibration
        df_list = self.create_df_list_for_calibration()
        cop = class_COP.COP()
        max_cop_value = 0
        min_cop_value = 0
        left_df, right_df = df_list  # Assign the left and right DataFrames from the list
        for right_row, left_row in zip(right_df.values, left_df.values):
            # Send the row to your custom function
            result = cop.total_center_of_pressure_just_x(right_row, left_row)
            # Update the maximum value if necessary
            if result > max_cop_value:
                max_cop_value = result
            # Update the minimum value if necessary
            if result < min_cop_value:
                min_cop_value = result
        df_list_ped = self.create_df_list_for_ped_calibration()
        ped = class_Pedometer.Pedometer()
        left_pace, right_pace = ped.walking_pace(df_list_ped, self.meas1.TIMEOUT)  # Calculate walking paces
        return max_cop_value, min_cop_value, left_pace, right_pace

    def create_df_list_for_calibration(self):
        df_list = []
        for imu, measurements_list in self.meas1.dict.imu_dict.items():
            if not measurements_list:
                continue
            # Remove incomplete measurements from the list
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
            # Remove incomplete measurements from the list
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
