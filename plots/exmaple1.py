import matplotlib.pyplot as plt
import numpy as np


#
x = np.random.rand(100) # 100 random numbers
y = list(range(100))
#
# fig, ax = plt.subplots()
# ax.plot(x, y)
def my_plotter(ax, data1, data2, param_dict):
    """
    A helper function to make a graph.
    """
    out = ax.plot(data1, data2, **param_dict)
    return out


#
# x = np.linspace(0, 2, 100)  # Sample data.
#
# # Note that even in the OO-style, we use `.pyplot.figure` to create the Figure.
# fig, ax = plt.subplots(figsize=(5, 2.7), layout='constrained')
# ax.plot(x, x, label='linear')  # Plot some data on the axes.
# ax.plot(x, x ** 2, label='quadratic')  # Plot more data on the axes...
# ax.plot(x, x ** 3, label='cubic')  # ... and some more.
# ax.set_xlabel('x label')  # Add an x-label to the axes.
# ax.set_ylabel('y label')  # Add a y-label to the axes.
# ax.set_title("Simple Plot")  # Add a title to the axes.
# ax.legend()  # Add a legend.

data1, data2, data3, data4 = np.random.randn(4, 100)  # make 4 random data sets
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5, 2.7))
my_plotter(ax1, data1, data2, {'marker': 'x'})
my_plotter(ax2, data3, data4, {'marker': 'o', 'color': 'orange',
                               'linestyle': ':'})
plt.show()
