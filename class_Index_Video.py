import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.animation import FuncAnimation
import imageio
import os


class Index:
    i = 0
    is_playing = True

    def __init__(self, points_list: list, timestamps_list: list, max_cop_value: float,
                 min_cop_value: float):
        self.points_list = points_list
        self.timestamps_list = timestamps_list
        self.max_cop_value = max_cop_value
        self.min_cop_value = min_cop_value
        self.fig, self.ax = plt.subplots()

        axplay = self.fig.add_axes([0.7, 0.05, 0.1, 0.055])
        axstop = self.fig.add_axes([0.81, 0.05, 0.1, 0.055])

        self.bplay = Button(axplay, 'Play/Pause')
        self.bplay.on_clicked(self.toggle_play)

        self.bstop = Button(axstop, 'Stop')
        self.bstop.on_clicked(self.stop)

        plt.subplots_adjust(bottom=0.2)
        # Calculate maximum X and Y values
        self.max_x_value = max([point[0] for point in self.points_list])
        self.max_y_value = max([point[1] for point in self.points_list])
        # Calculate minimum X and Y values
        self.min_x_value = min([point[0] for point in self.points_list])
        # self.min_y_value = min([point[1] for point in self.points_list])
        self.scatter = None

        # self.show_dot(points_list[0][0], points_list[0][1])
        self.anim = FuncAnimation(self.fig, self.update_plot, frames=len(self.points_list),
                                  interval=500, repeat=False)  # Adjust the frames and repeat parameters

    plt.show()

    def show_dot(self, x, y):
        print(self.i)
        self.ax.clear()  # Clear the previous plot
        x_max_lim = 1.5 * self.max_x_value
        if (1.5 * self.max_cop_value) > x_max_lim:
            x_max_lim = 1.5 * self.max_cop_value
        x_min_lim = 1.5 * self.min_x_value
        if (1.5 * self.min_cop_value) < x_min_lim:
            x_min_lim = 1.5 * self.min_cop_value
        self.ax.axvline(0, color='r', linestyle='--')  # Add a vertical line at x=0
        self.ax.axvline(self.max_cop_value*1.13, color='k', linestyle='--')
        self.ax.axvline(self.min_cop_value*1.13, color='k', linestyle='--')
        self.ax.set_xlim(x_min_lim, x_max_lim)
        self.ax.set_ylim(0, 1.5 * self.max_y_value)
        self.ax.set_xlabel('X COP')
        self.ax.set_ylabel('Y COP')
        timestamp = self.timestamps_list[self.i]
        self.ax.set_title(f'Center of Pressure\nTimestamp: {timestamp}')
        self.ax.scatter(x, y, color='steelblue')  # Plot the line

        self.scatter = self.ax.scatter(x, y, color='steelblue')  # Assign the scatter plot object

        if self.i == 0:
            self.ax.text(x, y*1.1, 'Beginning of data', ha='center', va='bottom')
        elif self.i == len(self.points_list) - 1:
            self.ax.text(x, y*1.1, 'End of data', ha='center', va='bottom')

        self.ax.axvline(self.max_cop_value * 1.13, color='k', linestyle='--')  # Add the vertical line

        plt.draw()

        def on_click(event):
            if event.button == 1 and event.inaxes == self.ax:
                # Check if left mouse button is clicked and click event occurred in the axes
                contains, _ = self.scatter.contains(event)  # Check if the click event occurred on a scatter point
                if contains:
                    x_clicked = event.xdata
                    y_clicked = event.ydata

                    # Remove previous annotations
                    for text in self.ax.texts:
                        text.remove()

                    self.ax.text(x_clicked, y_clicked*0.9, f'({self.points_list[self.i][0]:.2f}, '
                                                           f'{self.points_list[self.i][1]:.2f})',
                                 ha='center', va='bottom', fontsize=8, color='k')

                    if self.i == 0:
                        self.ax.text(x, y * 1.1, 'Beginning of data', ha='center', va='bottom')
                    elif self.i == len(self.points_list) - 1:
                        self.ax.text(x, y * 1.1, 'End of data', ha='center', va='bottom')

                    plt.draw()

        self.fig.canvas.mpl_connect('button_press_event', on_click)

    def update_plot(self, i):
        if hasattr(self, 'is_playing') and self.is_playing:  # Check if the attribute exists
            self.i = i
            t = self.points_list[self.i]
            self.show_dot(t[0], t[1])

    def next(self, event):
        self.i += 1
        if self.i >= len(self.points_list):
            self.i = len(self.points_list) - 1
            print("End of data")
        t = self.points_list[self.i]
        self.show_dot(t[0], t[1])

    def prev(self, event):
        if self.i <= 0:
            self.i = 0
            print("Beginning of data")
        else:
            self.i -= 1
        t = self.points_list[self.i]
        self.show_dot(t[0], t[1])

    def save_animation(self, filename, fps):
        temp_dir = 'temp'  # Temporary directory to store PNG frames
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        with imageio.get_writer(filename, fps=fps) as writer:
            for i in range(len(self.points_list)):
                t = self.points_list[i]
                self.show_dot(t[0], t[1])

                # Save the plot as a temporary PNG file
                temp_filename = os.path.join(temp_dir, f'frame_{i}.png')
                self.fig.savefig(temp_filename)

                # Append the temporary PNG file to the writer
                writer.append_data(imageio.imread(temp_filename))

                # Remove the temporary PNG file
                os.remove(temp_filename)

    def toggle_play(self, event):
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.bplay.label.set_text('Pause')
        else:
            self.bplay.label.set_text('Play')

    def stop(self, event):
        self.is_playing = False
        self.i = 0
        t = self.points_list[self.i]
        self.show_dot(t[0], t[1])
