import numpy as np
from matplotlib import pyplot as plt


class Pedometer:
    # timeout = 10
    step_min_time = 1  # minimum time between steps in seconds

    def sensor_sqrt(self, x, y, z, w):
        # Calculate and return the square root of the sum of the squares of the given sensor values
        return (x ** 2 + y ** 2 + z ** 2 + w ** 2) ** 0.5

    def sensor_net(self, df):
        # Calculate the net sensor value for each row in the DataFrame
        net = [self.sensor_sqrt(np.array(df.sensor1)[i], np.array(df.sensor2)[i], np.array(df.sensor3)[i],
                                np.array(df.sensor4)[i]) for i in range(len(np.array(df.sensor1)))]
        # Extract the sensor time values from the DataFrame
        sensor_time = df['actual_time'].tolist()
        return net, sensor_time

    def get_num_peaks(self, df, threshold=1.4):
        # Calculate the net sensor values and extract sensor time values
        data, sensor_time = self.sensor_net(df)
        # Calculate the mean and standard deviation of the net sensor values
        mean = sum(data) / len(data)
        std_dev = (sum([(val - mean) ** 2 for val in data]) / (len(data) - 1)) ** 0.5
        # Find the peaks that exceed the threshold
        peaks_x = []
        for i in range(1, len(data) - 1):
            if data[i] > data[i - 1] and data[i] > data[i + 1]:
                if abs(data[i] - mean) > threshold * std_dev:
                    peaks_x.append(i)
        # Retrieve the net sensor values, sensor time values, and peaks for further processing
        peaks_y = [data[ind] for ind in peaks_x]
        peaks_time = [sensor_time[ind] for ind in peaks_x]
        # Remove peaks that are too close in time or have lower amplitudes
        for i in range(len(peaks_time) - 1, 0, -1):
            if (peaks_time[i] - peaks_time[i - 1]) < self.step_min_time:
                if peaks_y[i] > peaks_y[i - 1]:
                    # Remove previous peak if current peak has higher amplitude
                    peaks_time.pop(i - 1)
                    peaks_y.pop(i - 1)
                    peaks_x.pop(i - 1)
                else:
                    # Remove current peak if previous peak has higher amplitude
                    peaks_time.pop(i)
                    peaks_y.pop(i)
                    peaks_x.pop(i)
            if i + 1 < len(peaks_time):
                if (peaks_time[i + 1] - peaks_time[i]) < self.step_min_time:
                    if peaks_y[i + 1] > peaks_y[i]:
                        # Remove current peak if next peak has higher amplitude
                        peaks_time.pop(i)
                        peaks_y.pop(i)
                        peaks_x.pop(i)
                    else:
                        # Remove next peak if current peak has higher amplitude
                        peaks_time.pop(i + 1)
                        peaks_y.pop(i + 1)
                        peaks_x.pop(i + 1)
        return len(peaks_x)

    def ped(self, df_list):
        ped_list = []
        for df in df_list:
            # Calculate the number of peaks for the current DataFrame
            ped_list.append(self.get_num_peaks(df))  # Add the number of peaks to the list
        return ped_list

    def walking_pace(self, df_list, run_time):
        # Calculate the walking pace for left and right feet
        left_pace = self.ped(df_list)[0] / run_time
        right_pace = self.ped(df_list)[1] / run_time
        return left_pace, right_pace

    def get_num_peaks_with_plot(self, df, threshold=1.4):
        # Compute sensor net and sensor time
        data, sensor_time = self.sensor_net(df)
        # Calculate mean and standard deviation
        mean = sum(data) / len(data)
        std_dev = (sum([(val - mean) ** 2 for val in data]) / (len(data) - 1)) ** 0.5
        # Find peaks in the data based on threshold
        peaks_x = []
        for i in range(1, len(data) - 1):
            if data[i] > data[i - 1] and data[i] > data[i + 1]:
                if abs(data[i] - mean) > threshold * std_dev:
                    peaks_x.append(i)
        # Extract peak values and corresponding times
        peaks_y = [data[ind] for ind in peaks_x]
        peaks_time = [sensor_time[ind] for ind in peaks_x]
        # Remove adjacent peaks that occur too close in time
        for i in range(len(peaks_time) - 1, 0, -1):
            if (peaks_time[i] - peaks_time[i - 1]) < self.step_min_time:
                if peaks_y[i] > peaks_y[i - 1]:
                    # Remove previous peak if current peak has higher amplitude
                    peaks_time.pop(i - 1)
                    peaks_y.pop(i - 1)
                    peaks_x.pop(i - 1)
                else:
                    # Remove current peak if previous peak has higher amplitude
                    peaks_time.pop(i)
                    peaks_y.pop(i)
                    peaks_x.pop(i)
            if i + 1 < len(peaks_time):
                if (peaks_time[i + 1] - peaks_time[i]) < self.step_min_time:
                    if peaks_y[i + 1] > peaks_y[i]:
                        # Remove current peak if next peak has higher amplitude
                        peaks_time.pop(i)
                        peaks_y.pop(i)
                        peaks_x.pop(i)
                    else:
                        # Remove next peak if current peak has higher amplitude
                        peaks_time.pop(i + 1)
                        peaks_y.pop(i + 1)
                        peaks_x.pop(i + 1)
        # Plot the peaks and data curve
        plt.plot(peaks_x, peaks_y, 'ro')  # Plot red dots at peak locations
        plt.xticks(peaks_x, peaks_time)  # Set x-axis ticks to peak times
        plt.plot(data, 'k-')  # Plot the entire data curve in black
        plt.show()
        # Print the number of steps
        print(f'number of steps:{len(peaks_x)}')
