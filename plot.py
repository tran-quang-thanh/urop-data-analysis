import numpy as np

import code.analyze as anl
import matplotlib.pyplot as plt


def grouping(data):
    time = data[0][0]
    ret = list()
    day_data = list()
    for item in data:
        if abs(item[0] - time) < 1209600:
            day_data.append(item)
        else:
            ret.append(day_data)
            time = item[0]
            day_data = [item]
    return ret


def plot_max_min(data, key):
    sub_max = list()
    sub_min = list()
    for array in data:
        sub_max.append(max(array, key=lambda item: item[1])[1])
        sub_min.append(min(array, key=lambda item: item[1])[1])
    time_arr = [array[0][0] for array in data]
    plt.plot(time_arr, sub_max, 'o')
    plt.plot(time_arr, sub_min, 'o')
    plt.title(key)
    plt.get_current_fig_manager().window.state('zoomed')
    plt.show()


def distribution_plot(data, key):
    hist, bin_edge = np.histogram([item[1] for item in data], bins=100, range=[0, 2.0])
    print(hist)
    fig, ax = plt.subplots()
    ax.bar(np.arange(0, 2, 0.02), hist, width=0.02)
    plt.title(key)
    plt.xlabel('acceleration')
    plt.ylabel('frequency')
    plt.get_current_fig_manager().window.state('zoomed')
    plt.show()


def sub_plot(key, array):
    timestamp = []
    mean = []
    std = []
    for item in array:
        timestamp.append(item[0])
        mean.append(item[1])
        std.append(item[2])
    axes = plt.gca()
    axes.set_ylim([0.5, 2])
    plt.plot(mean, 'o')
    plt.errorbar([i for i in range(len(mean))], mean, yerr=std, fmt=' ')
    # plt.plot(timestamp, 'o')
    plt.title(key)
    plt.get_current_fig_manager().window.state('zoomed')
    plt.show()


def plot():
    analyzed_accel_data = anl.analyze()
    for key, data in analyzed_accel_data.items():
        sub_plot(key, data)

        # data = grouping(data)
        # plot_max_min(data, key)
        # for array in data:
        #     sub_plot(key, array)

        # distribution_plot(data, key)


if __name__ == '__main__':
    plot()
