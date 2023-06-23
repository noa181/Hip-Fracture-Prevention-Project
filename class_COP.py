import numpy as np
import matplotlib.pyplot as plt


class COP:
    # FSR positions in mm
    fsr_x_positions_left = [21.0, 45.0, 57.0, 70.0]
    fsr_x_positions_right = [11.5, 42.0, 50.0, 67.0]
    fsr_y_positions_left = [206.0, 54.0, 206.0, 120.0]
    fsr_y_positions_right = [208.0, 52.0, 208.0, 132.0]
    leg_distance = 500  # TODO: need to check with Aviv

    def center_of_pressure(self, fsr_data, fsr_positions):
        # Calculate the center of pressure given the FSR data and positions.
        # Calculate moments
        moments = np.array(fsr_data).astype(float) * np.array(fsr_positions)
        # Calculate total force and moment
        total_force = np.sum(fsr_data)
        total_moment = np.sum(moments)
        # Calculate center of pressure
        if total_force == 0:
            return 0
        cop = total_moment / total_force
        return cop

    def center_of_pressure_2D(self, fsr_data, x_positions, y_positions):
        x_cop = self.center_of_pressure(fsr_data, x_positions)
        y_cop = self.center_of_pressure(fsr_data, y_positions)
        cop2D = [x_cop, y_cop]
        return cop2D

    def total_center_of_pressure(self, right_data, left_data):
        right_cop = self.center_of_pressure_2D(right_data, self.fsr_x_positions_right, self.fsr_y_positions_right)
        left_cop = self.center_of_pressure_2D(left_data, self.fsr_x_positions_left, self.fsr_y_positions_left)
        left_cop[0] = left_cop[0]*(-1)
        left_cop[0] = left_cop[0]-(self.leg_distance/2)
        right_cop[0] = right_cop[0]+(self.leg_distance/2)
        total_cop = [0, 0]
        total_cop[0] = (right_cop[0] + left_cop[0]) / 2.0
        total_cop[1] = (right_cop[1] + left_cop[1]) / 2.0
        return total_cop

    def total_center_of_pressure_just_x(self, right_data, left_data):
        right_x_cop = self.center_of_pressure(right_data, self.fsr_x_positions_right)
        left_x_cop = self.center_of_pressure(left_data, self.fsr_x_positions_left)
        left_x_cop = left_x_cop * (-1)
        left_x_cop = left_x_cop - (self.leg_distance / 2)
        right_x_cop = right_x_cop + (self.leg_distance / 2)
        total_x_cop = (right_x_cop + left_x_cop) / 2.0
        return total_x_cop

    def total_center_of_pressure_just_y(self, right_data, left_data):
        right_y_cop = self.center_of_pressure(right_data, self.fsr_y_positions_right)
        left_y_cop = self.center_of_pressure(left_data, self.fsr_y_positions_left)
        total_y_cop = (right_y_cop + left_y_cop) / 2.0
        return total_y_cop

# fsr_left = [385.79, 3492.24, 557.8, 864.5]
# fsr_right = [268.29, 1182.84, 103.53, 1149.77]
# cop = COP()
# total_cop = cop.total_center_of_pressure(fsr_right, fsr_left)
# print(total_cop)
# # Determine the maximum absolute value of the COP coordinates
# max_value = abs(total_cop[0])*1.5
# fig, ax = plt.subplots()
# ax.scatter(total_cop[0], total_cop[1])
# ax.axvline(0, color='r', linestyle='--')  # Add a vertical line at x=0
# ax.set_xlim(-max_value, max_value)  # Set the same range for positive and negative x-axis
# # ax.set_ylim(-max_value, max_value)  # Set the same range for positive and negative y-axis
# ax.set_xlabel('X COP')
# ax.set_ylabel('Y COP')
# ax.set_title('Center of Pressure')
# plt.show()

# Define a list of tuples for time and COP coordinates


time_cop_list = [
    (0, [385.79, 3492.24, 557.8, 864.5], [268.29, 1182.84, 103.53, 1149.77]),
    (1, [123.45, 789.12, 456.78, 987.65], [234.56, 789.12, 345.67, 876.54]),
    (2, [567.89, 345.67, 890.12, 123.45], [345.67, 123.45, 567.89, 901.23])
]
#
# cop = COP()
#
# fig, ax = plt.subplots()
#
# # Extract time and COP coordinates from the list of tuples
# time, right_data, left_data = zip(*time_cop_list)
#
# # Calculate the total center of pressure for each time point
# total_cop_list = [cop.total_center_of_pressure(right, left) for (right, left) in zip(right_data, left_data)]
#
# # Plot the COP coordinates at each time point
# ax.scatter([cop[0] for cop in total_cop_list], [cop[1] for cop in total_cop_list], c=time)
#
# # Add a vertical line at x=0
# ax.axvline(0, color='r', linestyle='--')
#
# # Customize the time scale
# ax.set_xlim(min(time), max(time))
#
# ax.set_xlabel('X COP')
# ax.set_ylabel('Y COP')
# ax.set_title('Center of Pressure')
#
# plt.show()
