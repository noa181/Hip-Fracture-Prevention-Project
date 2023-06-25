import class_Visualization

# Define the global variables
left_files = []
right_files = []
COP_files = []
calibration_file = ""
v = class_Visualization.Visualization()

# Define the functions to choose from
def function1():
    print("Running plot_IMU_data_actual_time")
    global left_files, right_files
    left_files = check_csv_extension(input("Enter a list with the names for the left foot CSV files: ").split(','))
    right_files = check_csv_extension(input("Enter a list with the names for the right foot CSV files: ").split(','))
    v.plot_IMU_data_actual_time(left_files, right_files)

def function2():
    print("Running plot_IMU_data_sensor_time")
    global left_files, right_files
    left_files = check_csv_extension(input("Enter a list with the names for the left foot CSV files: ").split(','))
    right_files = check_csv_extension(input("Enter a list with the names for the right foot CSV files: ").split(','))
    v.plot_IMU_data_sensor_time(left_files, right_files)

def function3():
    print("Running plot_FSR_data_actual_time")
    global left_files, right_files
    left_files = check_csv_extension(input("Enter a list with the names for the left foot CSV files: ").split(','))
    right_files = check_csv_extension(input("Enter a list with the names for the right foot CSV files: ").split(','))
    v.plot_FSR_data_actual_time(left_files, right_files)

def function4():
    print("Running plot_FSR_data_sensor_time")
    global left_files, right_files
    left_files = check_csv_extension(input("Enter a list with the names for the left foot CSV files: ").split(','))
    right_files = check_csv_extension(input("Enter a list with the names for the right foot CSV files: ").split(','))
    v.plot_FSR_data_sensor_time(left_files, right_files)

def function5():
    print("Running COP_GUI")
    global COP_files, calibration_file
    COP_files = check_csv_extension(input("Enter a list with the names for the COP CSV files: ").split(','))
    calibration_file = input("Enter the name for the calibration values CSV file: ")
    calibration_file = check_csv_extension([calibration_file])[0]
    v.COP_GUI(COP_files, calibration_file)

def function6():
    print("Running COP_GUI_video")
    global COP_files, calibration_file
    COP_files = check_csv_extension(input("Enter a list with the names for the COP CSV files: ").split(','))
    calibration_file = input("Enter the name for the calibration values CSV file: ")
    calibration_file = check_csv_extension([calibration_file])[0]
    v.COP_GUI_video(COP_files, calibration_file)

def check_csv_extension(file_list):
    return [file + ".csv" if not file.endswith(".csv") else file for file in file_list]

# Create a dictionary mapping function names to their corresponding function objects
functions = {
    "1": function1,
    "2": function2,
    "3": function3,
    "4": function4,
    "5": function5,
    "6": function6
}

# Display the list of functions for the user to choose from
print("Choose a function to run:")
print("1. plot IMU data with actual time")
print("2. plot IMU data with sensor time")
print("3. plot FSR data with actual time")
print("4. plot FSR data with sensor time")
print("5. COP GUI")
print("6. COP video")

# Prompt the user to enter their choice
choice = input("Enter the number of the function you want to run: ")

# Run the selected function and get the corresponding CSV file
selected_function = functions.get(choice)
if selected_function:
    selected_function()
else:
    print("Invalid choice")

# Use the variables outside the functions
print("Left foot CSV files:", left_files)
print("Right foot CSV files:", right_files)
print("COP CSV files:", COP_files)
print("Calibration values CSV files:", calibration_file)
