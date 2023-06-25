import matplotlib.pyplot as plt
from matplotlib.widgets import Button


class Index:
    i = 0

    def __init__(self, points_list: list, timestamps_list: list, max_cop_value: float,
                 min_cop_value: float):
        self.points_list = points_list
        self.timestamps_list = timestamps_list
        self.max_cop_value = max_cop_value
        self.min_cop_value = min_cop_value
        self.fig, self.ax = plt.subplots()
        axprev = self.fig.add_axes([0.7, 0.05, 0.1, 0.055])
        axnext = self.fig.add_axes([0.81, 0.05, 0.1, 0.055])
        bnext = Button(axnext, 'Next')
        bnext.on_clicked(self.next)
        bprev = Button(axprev, 'Previous')
        bprev.on_clicked(self.prev)
        plt.subplots_adjust(bottom=0.2)
        # Calculate maximum X and Y values
        self.max_x_value = max([point[0] for point in self.points_list])
        self.max_y_value = max([point[1] for point in self.points_list])
        # Calculate minimum X and Y values
        self.min_x_value = min([point[0] for point in self.points_list])
        # self.min_y_value = min([point[1] for point in self.points_list])
        self.scatter = None

        self.show_dot(points_list[0][0], points_list[0][1])

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
        self.ax.set_xlabel('X COP [cm]')
        self.ax.set_ylabel('Y COP [cm]')
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

                    self.ax.text(x_clicked, y_clicked*0.9, f'({self.points_list[self.i][0]:.2f},'
                                                           f' 'f'{self.points_list[self.i][1]:.2f})', ha='center',
                                 va='bottom', fontsize=8, color='k')

                    if self.i == 0:
                        self.ax.text(x, y * 1.1, 'Beginning of data', ha='center', va='bottom')
                    elif self.i == len(self.points_list) - 1:
                        self.ax.text(x, y * 1.1, 'End of data', ha='center', va='bottom')

                    plt.draw()

        self.fig.canvas.mpl_connect('button_press_event', on_click)

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
