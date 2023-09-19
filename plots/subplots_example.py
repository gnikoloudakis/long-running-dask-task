import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

matplotlib.use("TkAgg")


# Function to update the data for each subplot
def update_data():
    # Replace these lines with your code to fetch dynamic data from a source
    new_data1 = np.random.rand(100)  # Example data for subplot 1
    new_data2 = np.random.rand(100)  # Example data for subplot 2
    new_data3 = np.random.rand(100)  # Example data for subplot 3
    new_data4 = np.random.rand(100)  # Example data for subplot 4

    return new_data1, new_data2, new_data3, new_data4


# Function to update the plot for each animation frame
def update(frame):
    data1, data2, data3, data4 = update_data()

    # Clear each subplot before updating
    ax1.clear()
    ax2.clear()
    ax3.clear()
    ax4.clear()

    # Update subplot 1
    ax1.plot(data1)
    ax1.set_title("Subplot 1")

    # Update subplot 2
    ax2.plot(data2)
    ax2.set_title("Subplot 2")

    # Update subplot 3
    ax3.plot(data3)
    ax3.set_title("Subplot 3")

    # Update subplot 4
    ax4.plot(data4)
    ax4.set_title("Subplot 4")


# Create the subplots
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)

# Set the initial data for each subplot (optional, you can start with empty plots)
initial_data1 = np.zeros(100)
initial_data2 = np.zeros(100)
initial_data3 = np.zeros(100)
initial_data4 = np.zeros(100)

ax1.plot(initial_data1)
ax1.set_title("Subplot 1")

ax2.plot(initial_data2)
ax2.set_title("Subplot 2")

ax3.plot(initial_data3)
ax3.set_title("Subplot 3")

ax4.plot(initial_data4)
ax4.set_title("Subplot 4")

# Create the animation
ani = FuncAnimation(fig, update, interval=1000)  # Update every 1000 milliseconds (1 second)

plt.show()
