import csv
import matplotlib.pyplot as plt
import class_COP
import class_Index
import datetime
import time


class Visualization:

    def plot_IMU_data_actual_time(self, left_csv_files, right_csv_files):
        fig, axes = plt.subplots(2, 2, figsize=(10, 6))

        for file in left_csv_files:
            left_timestamps = []
            left_accelerations = []
            left_gyroscopes = []
            left_real_time = []
            with open(file, 'r') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip header row
                for row in reader:
                    timestamp = float(row[0])
                    acceleration = [float(row[5]), float(row[6]), float(row[7])]
                    gyroscope = [float(row[2]), float(row[3]), float(row[4])]
                    real = datetime.datetime.utcfromtimestamp(timestamp).strftime('%H:%M:%S')
                    left_timestamps.append(timestamp)
                    left_accelerations.append(acceleration)
                    left_gyroscopes.append(gyroscope)
                    left_real_time.append(real)

        for file in right_csv_files:
            right_timestamps = []
            right_accelerations = []
            right_gyroscopes = []
            right_real_time = []
            with open(file, 'r') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip header row
                for row in reader:
                    timestamp = float(row[0])
                    acceleration = [float(row[5]), float(row[6]), float(row[7])]
                    gyroscope = [float(row[2]), float(row[3]), float(row[4])]
                    real = datetime.datetime.utcfromtimestamp(timestamp).strftime('%H:%M:%S')
                    right_timestamps.append(timestamp)
                    right_accelerations.append(acceleration)
                    right_gyroscopes.append(gyroscope)
                    right_real_time.append(real)

        left_accelerations = list(zip(*left_accelerations))  # Transpose the list
        axes[0, 0].plot(left_timestamps, left_accelerations[0], label='Acc_X')
        axes[0, 0].plot(left_timestamps, left_accelerations[1], label='Acc_Y')
        axes[0, 0].plot(left_timestamps, left_accelerations[2], label='Acc_Z')

        left_gyroscopes = list(zip(*left_gyroscopes))  # Transpose the list
        axes[1, 0].plot(left_timestamps, left_gyroscopes[0], label='Gyro_X')
        axes[1, 0].plot(left_timestamps, left_gyroscopes[1], label='Gyro_Y')
        axes[1, 0].plot(left_timestamps, left_gyroscopes[2], label='Gyro_Z')

        right_accelerations = list(zip(*right_accelerations))  # Transpose the list
        axes[0, 1].plot(right_timestamps, right_accelerations[0], label='Acc_X')
        axes[0, 1].plot(right_timestamps, right_accelerations[1], label='Acc_Y')
        axes[0, 1].plot(right_timestamps, right_accelerations[2], label='Acc_Z')

        right_gyroscopes = list(zip(*right_gyroscopes))  # Transpose the list
        axes[1, 1].plot(right_timestamps, right_gyroscopes[0], label='Gyro_X')
        axes[1, 1].plot(right_timestamps, right_gyroscopes[1], label='Gyro_Y')
        axes[1, 1].plot(right_timestamps, right_gyroscopes[2], label='Gyro_Z')

        axes[0, 0].set_xlabel('Timestamp')
        axes[0, 0].set_ylabel('Acceleration')
        axes[0, 0].set_title('Left IMU Acceleration Data')
        axes[0, 0].legend(loc='upper right')

        axes[1, 0].set_xlabel('Timestamp')
        axes[1, 0].set_ylabel('Gyroscope')
        axes[1, 0].set_title('Left IMU Gyroscope Data')
        axes[1, 0].legend(loc='upper right')

        axes[0, 1].set_xlabel('Timestamp')
        axes[0, 1].set_ylabel('Acceleration')
        axes[0, 1].set_title('Right IMU Acceleration Data')
        axes[0, 1].legend(loc='upper right')

        axes[1, 1].set_xlabel('Timestamp')
        axes[1, 1].set_ylabel('Gyroscope')
        axes[1, 1].set_title('Right IMU Gyroscope Data')
        axes[1, 1].legend(loc='upper right')

        left_step = max(1, len(left_timestamps) // 10)  # Display a tick label for every 10th data point
        axes[0, 0].set_xticks(left_timestamps[::left_step])
        axes[0, 0].set_xticklabels(left_real_time[::left_step], rotation=45)
        axes[1, 0].set_xticks(left_timestamps[::left_step])
        axes[1, 0].set_xticklabels(left_real_time[::left_step], rotation=45)

        right_step = max(1, len(right_timestamps) // 10)  # Display a tick label for every 10th data point
        axes[0, 1].set_xticks(right_timestamps[::right_step])
        axes[0, 1].set_xticklabels(right_real_time[::right_step], rotation=45)
        axes[1, 1].set_xticks(right_timestamps[::right_step])
        axes[1, 1].set_xticklabels(right_real_time[::right_step], rotation=45)

        plt.tight_layout()
        plt.show()

    def plot_IMU_data_sensor_time(self, left_csv_files, right_csv_files):
        # TODO: need to fix x axis
        fig, axes = plt.subplots(2, 2, figsize=(10, 6))

        for file in left_csv_files:
            left_timestamps = []
            left_accelerations = []
            left_gyroscopes = []
            with open(file, 'r') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip header row
                for row in reader:
                    timestamp = float(row[1])
                    acceleration = [float(row[5]), float(row[6]), float(row[7])]
                    gyroscope = [float(row[2]), float(row[3]), float(row[4])]
                    left_timestamps.append(timestamp)
                    left_accelerations.append(acceleration)
                    left_gyroscopes.append(gyroscope)

        for file in right_csv_files:
            right_timestamps = []
            right_accelerations = []
            right_gyroscopes = []
            with open(file, 'r') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip header row
                for row in reader:
                    timestamp = float(row[1])
                    acceleration = [float(row[5]), float(row[6]), float(row[7])]
                    gyroscope = [float(row[2]), float(row[3]), float(row[4])]
                    right_timestamps.append(timestamp)
                    right_accelerations.append(acceleration)
                    right_gyroscopes.append(gyroscope)

        left_accelerations = list(zip(*left_accelerations))  # Transpose the list
        axes[0, 0].plot(left_timestamps, left_accelerations[0], label='Acc_X')
        axes[0, 0].plot(left_timestamps, left_accelerations[1], label='Acc_Y')
        axes[0, 0].plot(left_timestamps, left_accelerations[2], label='Acc_Z')

        left_gyroscopes = list(zip(*left_gyroscopes))  # Transpose the list
        axes[1, 0].plot(left_timestamps, left_gyroscopes[0], label='Gyro_X')
        axes[1, 0].plot(left_timestamps, left_gyroscopes[1], label='Gyro_Y')
        axes[1, 0].plot(left_timestamps, left_gyroscopes[2], label='Gyro_Z')

        right_accelerations = list(zip(*right_accelerations))  # Transpose the list
        axes[0, 1].plot(right_timestamps, right_accelerations[0], label='Acc_X')
        axes[0, 1].plot(right_timestamps, right_accelerations[1], label='Acc_Y')
        axes[0, 1].plot(right_timestamps, right_accelerations[2], label='Acc_Z')

        right_gyroscopes = list(zip(*right_gyroscopes))  # Transpose the list
        axes[1, 1].plot(right_timestamps, right_gyroscopes[0], label='Gyro_X')
        axes[1, 1].plot(right_timestamps, right_gyroscopes[1], label='Gyro_Y')
        axes[1, 1].plot(right_timestamps, right_gyroscopes[2], label='Gyro_Z')

        axes[0, 0].set_xlabel('Timestamp')
        axes[0, 0].set_ylabel('Acceleration')
        axes[0, 0].set_title('Left IMU Acceleration Data')
        axes[0, 0].legend(loc='upper right')

        axes[1, 0].set_xlabel('Timestamp')
        axes[1, 0].set_ylabel('Gyroscope')
        axes[1, 0].set_title('Left IMU Gyroscope Data')
        axes[1, 0].legend(loc='upper right')

        axes[0, 1].set_xlabel('Timestamp')
        axes[0, 1].set_ylabel('Acceleration')
        axes[0, 1].set_title('Right IMU Acceleration Data')
        axes[0, 1].legend(loc='upper right')

        axes[1, 1].set_xlabel('Timestamp')
        axes[1, 1].set_ylabel('Gyroscope')
        axes[1, 1].set_title('Right IMU Gyroscope Data')
        axes[1, 1].legend(loc='upper right')

        plt.tight_layout()
        plt.show()

    def plot_FSR_data_actual_time(self, left_csv_files, right_csv_files):
        # fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))

        for file in left_csv_files:
            left_timestamps = []
            left_sensors = []
            left_real_time = []
            with open(file, 'r') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip header row
                for row in reader:
                    timestamp = float(row[0])
                    sensor = [float(row[8]), float(row[9]), float(row[10]), float(row[11])]
                    real = datetime.datetime.utcfromtimestamp(timestamp).strftime('%H:%M:%S')
                    left_timestamps.append(timestamp)
                    left_sensors.append(sensor)
                    left_real_time.append(real)

        # for file in right_csv_files:
        #     right_timestamps = []
        #     right_sensors = []
        #     right_real_time = []
        #     with open(file, 'r') as csvfile:
        #         reader = csv.reader(csvfile)
        #         next(reader)  # Skip header row
        #         for row in reader:
        #             timestamp = float(row[0])
        #             sensor = [float(row[8]), float(row[9]), float(row[10]), float(row[11])]
        #             real = datetime.datetime.utcfromtimestamp(timestamp).strftime('%H:%M:%S')
        #             right_timestamps.append(timestamp)
        #             right_sensors.append(sensor)
        #             right_real_time.append(real)

        left_sensors = list(zip(*left_sensors))  # Transpose the list
        # ax1.plot(left_timestamps, left_sensors[0], label='sensor 1')
        # ax1.plot(left_timestamps, left_sensors[1], label='sensor 2')
        # ax1.plot(left_timestamps, left_sensors[2], label='sensor 3')
        # ax1.plot(left_timestamps, left_sensors[3], label='sensor 4')
        # ax1.set_xlabel('Timestamp')
        # ax1.set_ylabel('FSR')
        # ax1.set_title('Left FSR Data')
        # ax1.legend(loc='upper right')

        plt.plot(left_timestamps, left_sensors[0], label='sensor 1')
        plt.plot(left_timestamps, left_sensors[1], label='sensor 2')
        plt.plot(left_timestamps, left_sensors[2], label='sensor 3')
        plt.plot(left_timestamps, left_sensors[3], label='sensor 4')
        plt.xlabel('Timestamp')
        plt.ylabel('FSR')
        plt.title('Left FSR Data')
        plt.legend(loc='upper right', fontsize="14")

        # right_sensors = list(zip(*right_sensors))  # Transpose the list
        # ax2.plot(right_timestamps, right_sensors[0], label='sensor 1')
        # ax2.plot(right_timestamps, right_sensors[1], label='sensor 2')
        # ax2.plot(right_timestamps, right_sensors[2], label='sensor 3')
        # ax2.plot(right_timestamps, right_sensors[3], label='sensor 4')
        # ax2.set_xlabel('Timestamp')
        # ax2.set_ylabel('FSR')
        # ax2.set_title('Right FSR Data')
        # ax2.legend(loc='upper right')

        # left_step = max(1, len(left_timestamps) // 10)  # Display a tick label for every 10th data point
        # ax1.set_xticks(left_timestamps[::left_step])
        # ax1.set_xticklabels(left_real_time[::left_step], rotation=45)

        # plt.xticks(left_timestamps[::left_step])
        # plt.xticklabels(left_real_time[::left_step], rotation=45)

        # right_step = max(1, len(right_timestamps) // 10)  # Display a tick label for every 10th data point
        # ax2.set_xticks(right_timestamps[::right_step])
        # ax2.set_xticklabels(right_real_time[::right_step], rotation=45)

        plt.tight_layout()
        plt.show()

    def plot_FSR_data_sensor_time(self, left_csv_files, right_csv_files):
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))

        for file in left_csv_files:
            left_timestamps = []
            left_sensors = []
            with open(file, 'r') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip header row
                for row in reader:
                    timestamp = float(row[1])
                    sensor = [float(row[8]), float(row[9]), float(row[10]), float(row[11])]
                    left_timestamps.append(timestamp)
                    left_sensors.append(sensor)

        for file in right_csv_files:
            right_timestamps = []
            right_sensors = []
            with open(file, 'r') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip header row
                for row in reader:
                    timestamp = float(row[1])
                    sensor = [float(row[8]), float(row[9]), float(row[10]), float(row[11])]
                    right_timestamps.append(timestamp)
                    right_sensors.append(sensor)

        left_sensors = list(zip(*left_sensors))  # Transpose the list
        ax1.plot(left_timestamps, left_sensors[0], label='sensor 1')
        ax1.plot(left_timestamps, left_sensors[1], label='sensor 2')
        ax1.plot(left_timestamps, left_sensors[2], label='sensor 3')
        ax1.plot(left_timestamps, left_sensors[3], label='sensor 4')
        ax1.set_xlabel('Timestamp')
        ax1.set_ylabel('FSR')
        ax1.set_title('Left FSR Data')
        ax1.legend(loc='upper right')

        right_sensors = list(zip(*right_sensors))  # Transpose the list
        ax2.plot(right_timestamps, right_sensors[0], label='sensor 1')
        ax2.plot(right_timestamps, right_sensors[1], label='sensor 2')
        ax2.plot(right_timestamps, right_sensors[2], label='sensor 3')
        ax2.plot(right_timestamps, right_sensors[3], label='sensor 4')
        ax2.set_xlabel('Timestamp')
        ax2.set_ylabel('FSR')
        ax2.set_title('Right FSR Data')
        ax2.legend(loc='upper right')

        plt.tight_layout()
        plt.show()

    def COP_GUI(self, csv_files, calibration_csv):
        timestamps = []
        cop_points = []
        for file in csv_files:

            cops_time_list = []
            cop = class_COP.COP()
            with open(file, 'r') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip header row
                for row in reader:
                    timestamp = float(row[0])
                    timestamp = datetime.datetime.utcfromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M:%S')
                    cop_point = [float(row[1]), float(row[2])/10]
                    timestamps.append(timestamp)
                    cop_points.append(cop_point)
        max_cop_value, min_cop_value = self.COP_limits(calibration_csv)
        # class_Index.Index(cop_points, timestamps, max_cop_value, min_cop_value)
        index = class_Index.Index(cop_points, timestamps, max_cop_value, min_cop_value)
        # index.save_animation('animation.mp4', fps=30)
        plt.show()

    def COP_limits(self, calibration_csv):
        with open(calibration_csv, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header row
            for row in reader:
                max_cop_value = float(row[0])
                min_cop_value = float(row[1])
                # left_pace_calibration = float(row[2])
                # right_pace_calibration = float(row[3])
        return max_cop_value, min_cop_value



# files = ['COP-10-06-2023 22-02-55.csv']
files = ['COP-14-06-2023 11-08-44.csv']
l_files = ['right-14-06-2023 11-08-44.csv']
r_files = ['left-14-06-2023 11-08-44.csv']

# calib_file = "calibration values-10-06-2023 22-02-55.csv"
calib_file = "calibration values-14-06-2023 11-08-43.csv"

v = Visualization()
v.plot_FSR_data_actual_time(l_files, r_files)
# v.COP_GUI(files, calib_file)

