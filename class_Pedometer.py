import numpy as np
from matplotlib import pyplot as plt
import pandas as pd


class Pedometer:
    timeout = 10
    step_min_time = 1  # minimum time between steps in seconds

    def sensor_sqrt(self, x, y, z, w):
        return (x ** 2 + y ** 2 + z ** 2 + w ** 2) ** 0.5

    def sensor_net(self, df):
        net = [self.sensor_sqrt(np.array(df.sensor1)[i], np.array(df.sensor2)[i], np.array(df.sensor3)[i],
                                np.array(df.sensor4)[i]) for i in range(len(np.array(df.sensor1)))]
        sensor_time = df['actual_time'].tolist()
        # print(sensor_time)
        return net, sensor_time

    def get_num_peaks(self, df, threshold=1.4):
        data, sensor_time = self.sensor_net(df)
        # print(data, sensor_time)
        mean = sum(data) / len(data)
        std_dev = (sum([(val - mean) ** 2 for val in data]) / (len(data) - 1)) ** 0.5
        peaks_x = []
        for i in range(1, len(data) - 1):
            if data[i] > data[i - 1] and data[i] > data[i + 1]:
                if abs(data[i] - mean) > threshold * std_dev:
                    peaks_x.append(i)
        peaks_y = [data[ind] for ind in peaks_x]
        # print(peaks_x)
        peaks_time = [sensor_time[ind] for ind in peaks_x]
        for i in range(len(peaks_time) - 1, 0, -1):
            if (peaks_time[i] - peaks_time[i - 1]) < self.step_min_time:
                if peaks_y[i] > peaks_y[i - 1]:
                    peaks_time.pop(i - 1)
                    peaks_y.pop(i - 1)
                    peaks_x.pop(i - 1)
                else:
                    peaks_time.pop(i)
                    peaks_y.pop(i)
                    peaks_x.pop(i)
            if i + 1 < len(peaks_time):
                if (peaks_time[i + 1] - peaks_time[i]) < self.step_min_time:
                    if peaks_y[i + 1] > peaks_y[i]:
                        peaks_time.pop(i)
                        peaks_y.pop(i)
                        peaks_x.pop(i)
                    else:
                        peaks_time.pop(i + 1)
                        peaks_y.pop(i + 1)
                        peaks_x.pop(i + 1)
        return len(peaks_x)

    def ped(self, df_list):
        ped_list = []
        for df in df_list:
            ped_list.append(self.get_num_peaks(df))
        return ped_list

    def walking_pace(self, df_list, run_time):
        left_pace = self.ped(df_list)[0] / run_time
        right_pace = self.ped(df_list)[1] / run_time
        return left_pace, right_pace

    # def get_num_peaks_for_regular_meas(self, df, mean, std_dev, threshold=1.4):
    #     # print('in')
    #     data = self.sensor_net(df)
    #     # print('data:')
    #     # print(data)
    #     peaks_x = []
    #     for i in range(1, len(data) - 1):
    #         if data[i] > data[i - 1] and data[i] > data[i + 1]:
    #             if abs(data[i] - mean) > threshold * std_dev:
    #                 peaks_x.append(i)
    #     # peaks_y = [data[ind] for ind in peaks_x]
    #     # return peaks_x, peaks_y
    #     return len(peaks_x)

    # def pace(self, start_time):
    #     self.pace_list.append(self.walking_pace(start_time))

    # def pace_measurement(self):
    #     while True:
    #         try:
    #             self.pace(time.time())
    #             time.sleep(self.timeout)
    #         except KeyboardInterrupt:
    #             print('break')
                # break

    def get_num_peaks_with_plot(self, df, threshold=1.4):
        data, sensor_time = self.sensor_net(df)
        mean = sum(data) / len(data)
        std_dev = (sum([(val - mean) ** 2 for val in data]) / (len(data) - 1)) ** 0.5
        peaks_x = []
        for i in range(1, len(data) - 1):
            if data[i] > data[i - 1] and data[i] > data[i + 1]:
                if abs(data[i] - mean) > threshold * std_dev:
                    peaks_x.append(i)
        peaks_y = [data[ind] for ind in peaks_x]
        peaks_time = [sensor_time[ind] for ind in peaks_x]
        for i in range(len(peaks_time) - 1, 0, -1):
            if (peaks_time[i] - peaks_time[i - 1]) < self.step_min_time:
                if peaks_y[i] > peaks_y[i - 1]:
                    peaks_time.pop(i - 1)
                    peaks_y.pop(i - 1)
                    peaks_x.pop(i - 1)
                else:
                    peaks_time.pop(i)
                    peaks_y.pop(i)
                    peaks_x.pop(i)
            if i + 1 < len(peaks_time):
                if (peaks_time[i + 1] - peaks_time[i]) < self.step_min_time:
                    if peaks_y[i + 1] > peaks_y[i]:
                        peaks_time.pop(i)
                        peaks_y.pop(i)
                        peaks_x.pop(i)
                    else:
                        peaks_time.pop(i + 1)
                        peaks_y.pop(i + 1)
                        peaks_x.pop(i + 1)
        plt.plot(peaks_x, peaks_y, 'ro')
        plt.xticks(peaks_x, peaks_time)  # Set x-axis ticks to peak times
        plt.plot(data, 'k-')
        plt.show()
        print(f'number of steps:{len(peaks_x)}')

    def csv_to_peak_plot(self, csv_name):
        if not csv_name.endswith(".csv"):
            csv_name += ".csv"
        data = pd.read_csv(csv_name)
        self.get_num_peaks_with_plot(data)
