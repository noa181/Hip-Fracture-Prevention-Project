import time
import pandas
import copy
from datetime import datetime


class IMU_dict:
    COLUMNS = ['actual_time', 'time', 'heading', 'pitch', 'roll', 'ax', 'ay', 'az', 'sensor1',
               'sensor2', 'sensor3', 'sensor4', 'sensor5']
# TODO: need to add - delete the dict after it reaches some volume

    def __init__(self):
        self.imu_dict = {'left': [], 'right': []}

    # def meas_to_file(self, dict_to_file):
    #     # printing the measurement data into csv file
    #     df_list = []
    #     for imu, measurements_list in dict_to_file.items():
    #         if not measurements_list:
    #             continue
    #         title = f'{imu}{datetime.now():%d-%m-%Y %H-%M-%S}'
    #         df = pandas.DataFrame(measurements_list, columns=self.COLUMNS)
    #         df.to_csv(f'{title}.csv', index=False)
    #         df_list.append(df)
    #     return df_list

    # def meas_to_file_cal(self):
    #     # printing the calibration measurement data into csv file and returning a dict with df for every imu
    #     df_dict = {}
    #     for imu, measurements_list in self.imu_dict.items():
    #         if not measurements_list:
    #             continue
    #         title = f'calibration-{imu}{datetime.now():%d-%m-%Y %H-%M-%S}'
    #         df = pandas.DataFrame(measurements_list, columns=self.COLUMNS)
    #         df.to_csv(f'{title}.csv', index=False)
    #         df_dict[imu] = df
    #     return df_dict

    # def remove_half(self):
    #     deleted_dict = {}
    #     new_dict = {}
    #     for key, value in self.imu_dict.items():
    #         print(f'removing half of: {key}')
    #         half_value = value[:len(value) // 2]
    #         deleted_dict[key] = half_value
    #         new_dict[key] = value[len(value) // 2:]
    #     self.imu_dict = new_dict
    #     return deleted_dict

    def dict_append(self, splitted_output, file_time_stamp):
        # taking a single data line and appending it to the dict
        try:
            file_list = [0, 0, 0]
            imu_name = splitted_output[0]
            measurements = splitted_output[1]
            time_stamp = time.time()
            data = [time_stamp] + [float(item) for item in measurements.split(',')]
            if len(data) != 13:
                print(f'Error accrued in: {splitted_output}')
                return file_list
            self.imu_dict[imu_name].append(data)
            file_list[0] = imu_name
            file_list[1] = file_time_stamp
            file_list[2] = data
            return file_list
            # TODO: check with yoav why the exception always work
        except ValueError:
            print(f'Error accrued in: {splitted_output}')
            return file_list

    def time_range_dict(self, start_time, stop_time):
        df_list = []
        curr_imu_dict = copy.deepcopy(self.imu_dict)  # TODO: check if it fixed the error
        for imu, measurements_list in curr_imu_dict.items():
            if not measurements_list:
                continue
            for i in range(len(measurements_list)):
                if len(measurements_list[i]) != 13:
                    measurements_list.pop(i)
                    print("pop")
            # print(len(measurements_list))
            df = pandas.DataFrame(measurements_list, columns=self.COLUMNS)
            # print(df)
            df = df[df.actual_time >= start_time]
            df = df[df.actual_time < stop_time]
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

    def time_range_dict_for_ped(self, start_time, stop_time):
        df_list = []
        curr_imu_dict = copy.deepcopy(self.imu_dict)
        for imu, measurements_list in curr_imu_dict.items():
            if not measurements_list:
                continue
            for i in range(len(measurements_list)):
                if len(measurements_list[i]) != 13:
                    measurements_list.pop(i)
            df = pandas.DataFrame(measurements_list, columns=self.COLUMNS)
            df = df[df.actual_time >= start_time]
            df = df[df.actual_time < stop_time]
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

    # def create_df_list(self):
    #     df_list = []
    #     for imu, measurements_list in self.imu_dict.items():
    #         df = pandas.DataFrame(measurements_list, columns=self.COLUMNS)
    #         df_list.append(df)
    #     print(df_list)
    #     return df_list
