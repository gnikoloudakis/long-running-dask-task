import matplotlib.pyplot as plt

from models.models import WaitingTime


def my_plotter(ax, data1, data2, param_dict):
    """
    A helper function to make a graph.
    """
    out = ax.plot(data1, data2, **param_dict)
    return out


all = WaitingTime.objects
x = [t.timestamp for t in all]
y = [v.value for v in all]

fig, ax = plt.subplots()
ax.plot(x[:100], y[:100])
plt.show()
