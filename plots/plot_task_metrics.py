import datetime

import matplotlib

# matplotlib.use("Agg")  # Use the Agg backend before importing pyplot
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

from models.models import IdleTime, WaitingTime, ExecutionTime

ax1 = None
ax2 = None
ax3 = None


# ax4 = None


# Function to update the data for each subplot
def update_data():
    # Replace these lines with your code to fetch dynamic data from a source
    ide_time_obs = IdleTime.objects.order_by('-timestamp')
    idle_time_y = [v.value for v in ide_time_obs] if len(ide_time_obs) > 0 else []
    idle_time_x = [datetime.datetime.fromtimestamp(t.timestamp) for t in ide_time_obs] if len(ide_time_obs) > 0 else []

    waiting_time_obs = WaitingTime.objects.order_by('-timestamp')
    waiting_time_y = [v.value for v in waiting_time_obs] if len(waiting_time_obs) > 0 else []
    waiting_time_x = [datetime.datetime.fromtimestamp(t.timestamp) for t in waiting_time_obs] if len(waiting_time_obs) > 0 else []

    execution_time_obs = ExecutionTime.objects.order_by('-timestamp')
    execution_time_y = [v.value for v in execution_time_obs] if len(execution_time_obs) > 0 else []
    execution_time_x = [datetime.datetime.fromtimestamp(t.timestamp) for t in execution_time_obs] if len(execution_time_obs) > 0 else []

    return idle_time_x, idle_time_y, waiting_time_x, waiting_time_y, execution_time_x, execution_time_y


# Function to update the plot for each animation frame
def update(i):
    idle_time_x, idle_time_y, waiting_time_x, waiting_time_y, execution_time_x, execution_time_y = update_data()
    # Clear each subplot before updating
    ax1.clear()
    ax2.clear()
    ax3.clear()
    # ax4.clear()

    # Update subplot 1
    ax1.plot(idle_time_x, idle_time_y, **{'color': 'red', 'linestyle': ':'})
    ax1.set_title("Idle Time")

    # Update subplot 2
    ax2.plot(waiting_time_x, waiting_time_y, **{'color': 'orange', 'linestyle': '--'})
    ax2.set_title("Waiting Time")

    # Update subplot 3
    ax3.plot(execution_time_x, execution_time_y, **{'color': 'green', 'linestyle': '-.'})
    ax3.set_title("Execution Time")

    # Update subplot 4
    # ax4.plot(data4)
    # ax4.set_title("Subplot 4")


def show_plots():
    # Create the subplots
    # fig, ((_ax1, _ax2), (_ax3, _ax4)) = plt.subplots(2, 2)
    fig, ((_ax1), (_ax2), (_ax3)) = plt.subplots(3, 1)
    global ax1, ax2, ax3
    ax1 = _ax1
    ax2 = _ax2
    ax3 = _ax3
    # ax4 = _ax4

    # Set the initial data for each subplot (optional, you can start with empty plots)
    initial_data1 = np.zeros(1000)
    initial_data2 = np.zeros(1000)
    initial_data3 = np.zeros(1000)
    # initial_data4 = np.zeros(1000)

    ax1.plot(initial_data1)
    ax1.set_title("Idle Time")

    ax2.plot(initial_data2)
    ax2.set_title("Waiting Time")

    ax3.plot(initial_data3)
    ax3.set_title("Execution Time")

    # ax4.plot(initial_data4)
    # ax4.set_title("Subplot 4")

    # Create the animation
    ani = FuncAnimation(fig, update, interval=1000, cache_frame_data=False)  # Update every 1000 milliseconds (1 second)
    plt.show()


show_plots()
