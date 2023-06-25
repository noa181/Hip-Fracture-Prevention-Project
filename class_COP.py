import numpy as np


class COP:
    # FSR positions in mm
    fsr_x_positions_left = [21.0, 45.0, 57.0, 70.0]
    fsr_x_positions_right = [11.5, 42.0, 50.0, 67.0]
    fsr_y_positions_left = [206.0, 54.0, 206.0, 120.0]
    fsr_y_positions_right = [208.0, 52.0, 208.0, 132.0]
    leg_distance = 500  # here the therapist need to enter the measured value

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
        # Calculate center of pressure in the x-direction
        x_cop = self.center_of_pressure(fsr_data, x_positions)
        # Calculate center of pressure in the y-direction
        y_cop = self.center_of_pressure(fsr_data, y_positions)
        cop2D = [x_cop, y_cop]
        # Return the 2D center of pressure vector
        return cop2D

    def total_center_of_pressure(self, right_data, left_data):
        # Calculate the center of pressure for the right foot
        right_cop = self.center_of_pressure_2D(right_data, self.fsr_x_positions_right, self.fsr_y_positions_right)
        # Calculate the center of pressure for the left foot
        left_cop = self.center_of_pressure_2D(left_data, self.fsr_x_positions_left, self.fsr_y_positions_left)
        # Adjust the x-coordinate of the left foot COP
        left_cop[0] = left_cop[0]*(-1)
        left_cop[0] = left_cop[0]-(self.leg_distance/2)
        # Adjust the x-coordinate of the right foot COP
        right_cop[0] = right_cop[0]+(self.leg_distance/2)
        total_cop = [0, 0]
        # Calculate the total center of pressure by averaging the x and y coordinates
        total_cop[0] = (right_cop[0] + left_cop[0]) / 2.0
        total_cop[1] = (right_cop[1] + left_cop[1]) / 2.0
        return total_cop

    def total_center_of_pressure_just_x(self, right_data, left_data):
        # Calculate the x-coordinate of the center of pressure for the right foot
        right_x_cop = self.center_of_pressure(right_data, self.fsr_x_positions_right)
        # Calculate the x-coordinate of the center of pressure for the left foot
        left_x_cop = self.center_of_pressure(left_data, self.fsr_x_positions_left)
        # Adjust the x-coordinate of the left foot COP
        left_x_cop = left_x_cop * (-1)
        left_x_cop = left_x_cop - (self.leg_distance / 2)
        # Adjust the x-coordinate of the right foot COP
        right_x_cop = right_x_cop + (self.leg_distance / 2)
        # Calculate the total x-coordinate of the center of pressure by averaging the right and left foot values
        total_x_cop = (right_x_cop + left_x_cop) / 2.0
        return total_x_cop

    def total_center_of_pressure_just_y(self, right_data, left_data):
        # Calculate the y-coordinate of the center of pressure for the right foot
        right_y_cop = self.center_of_pressure(right_data, self.fsr_y_positions_right)
        # Calculate the y-coordinate of the center of pressure for the left foot
        left_y_cop = self.center_of_pressure(left_data, self.fsr_y_positions_left)
        # Calculate the total y-coordinate of the center of pressure by averaging the right and left foot values
        total_y_cop = (right_y_cop + left_y_cop) / 2.0
        return total_y_cop
