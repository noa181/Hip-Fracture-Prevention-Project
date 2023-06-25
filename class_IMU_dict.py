import time
import pandas
import copy


class IMU_dict:
    COLUMNS = ['actual_time', 'time', 'heading', 'pitch', 'roll', 'ax', 'ay', 'az', 'sensor1',
               'sensor2', 'sensor3', 'sensor4', 'sensor5']

    def __init__(self):
        self.imu_dict = {'left': [], 'right': []}

    def dict_append(self, splitted_output, file_time_stamp):
        # taking a single data line and appending it to the dict
        try:
            file_list = [0, 0, 0]
            imu_name = splitted_output[0]
            measurements = splitted_output[1]
            # Get the current timestamp
            time_stamp = time.time()
            data = [time_stamp] + [float(item) for item in measurements.split(',')]
            # Check if the data list has the expected number of elements
            if len(data) != 13:
                print(f'Error accrued in: {splitted_output}')
                return file_list
            self.imu_dict[imu_name].append(data)
            file_list[0] = imu_name
            file_list[1] = file_time_stamp
            file_list[2] = data
            if len(self.imu_dict[imu_name]) > 500000:
                self.imu_dict[imu_name] = self.imu_dict[imu_name][len(self.imu_dict[imu_name]) // 2:]
            return file_list
        except ValueError:
            print(f'Error accrued in: {splitted_output}')
            return file_list

    def time_range_dict(self, start_time, stop_time):
        df_list = []
        curr_imu_dict = copy.deepcopy(self.imu_dict)
        for imu, measurements_list in curr_imu_dict.items():
            if not measurements_list:
                continue
            for i in range(len(measurements_list)):
                # Check if the measurement list has the expected number of elements
                if len(measurements_list[i]) != 13:
                    measurements_list.pop(i)
                    print("pop")
            df = pandas.DataFrame(measurements_list, columns=self.COLUMNS)
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
                # Check if the measurement list has the expected number of elements
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
