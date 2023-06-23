import csv
import os


class Meas_To_File:
    COLUMNS = ['actual_time', 'time', 'heading', 'pitch', 'roll', 'ax', 'ay', 'az', 'sensor1',
               'sensor2', 'sensor3', 'sensor4', 'sensor5']
    COP_COLUMNS = ['actual_time', 'COP_x', 'COP_y']
    PED_COLUMNS = ['actual_time', 'left_pace', 'right_pace']
    CALIBRATION_COLUMNS = ['max_cop_value', 'min_cop_value', 'left_pace_calibration', 'right_pace_calibration']

    def add_csv_row(self, filename, columns, row):
        if not filename.endswith(".csv"):
            filename += ".csv"
        max_file_size = 2 * 1024 * 1024  # 2 megabytes
        if not os.path.exists(filename):
            with open(filename, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(columns)
            print(f"New CSV file '{filename}' created successfully!")
        file_size = os.path.getsize(filename)
        if file_size >= max_file_size:
            # Find the next available filename with the same base name plus a suffix
            suffix = 2
            while os.path.exists(f"{filename[:-4]}_{suffix}.csv"):
                suffix += 1
            new_filename = f"{filename[:-4]}_{suffix}.csv"
            with open(new_filename, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(columns)
            print(f"New CSV file '{new_filename}' created successfully!")
            filename = new_filename
        with open(filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(row)

    def calibration_add_row(self, info_list):
        imu = info_list[0]
        file_time_stamp = info_list[1]
        data = info_list[2]
        title = f'calibration-{imu}-{file_time_stamp}'
        self.add_csv_row(title, self.COLUMNS, data)

    def regular_measurement_add_row(self, info_list):
        imu = info_list[0]
        file_time_stamp = info_list[1]
        data = info_list[2]
        title = f'{imu}-{file_time_stamp}'
        self.add_csv_row(title, self.COLUMNS, data)

    def COP_file_add_row(self, file_time_stamp, data):
        title = f'COP-{file_time_stamp}'
        self.add_csv_row(title, self.COP_COLUMNS, data)

    def PED_file_add_row(self, file_time_stamp, data):
        title = f'walking pace-{file_time_stamp}'
        self.add_csv_row(title, self.PED_COLUMNS, data)

    def calibration_values_to_file(self, file_time_stamp, data):
        title = f'calibration values-{file_time_stamp}'
        self.add_csv_row(title, self.CALIBRATION_COLUMNS, data)
