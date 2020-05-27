import json
import os

import numpy as np
import matplotlib.pyplot as plt

d = dict()
pos_array = ['bottom-right', "bottom-left", 'center', 'top-right', 'top-left']
distribution_array = [0.0, 50.0, 55.0, 60.0, 65.0, 70.0, 75.0, 80.0, 85.0, 90.0, 95.0, 100.0, 105.0, 110.0,
                      120.0, 125.0, 130.0, 135.0, 140.0, 145.0, 150.0, 20000.0]


def plot_acceleration(map, item):
    sub_dict = map[item]['accel']
    cur_time = 0
    timestamp_arr = []
    one_period_arr = []
    all_data_arr = []
    for sub_item in sub_dict:
        try:
            time = int(sub_item['timestamp'])
            if abs(time - cur_time) > 120 or time * cur_time < 0:
                cur_time = time
                timestamp_arr.append(time)
                all_data_arr.append(mean_and_std(one_period_arr))
                one_period_arr = []

            else:
                one_period_arr.append(sub_item['total-accel'])
        except:
            continue
    if len(timestamp_arr) < 10:
        return
    plt.plot(timestamp_arr, list(accel[0] for accel in all_data_arr), 'o')
    plt.errorbar(timestamp_arr, list(accel[0] for accel in all_data_arr), yerr=list(error[1] for error in all_data_arr), fmt=' ')
    plt.xlabel('timestamp')
    plt.ylabel(item)
    plt.show()
    # plt.pause(1)
    # plt.close()


def plot_distribution(map, item):
    accel_arr = list(data['total-accel'] for data in map[item]['accel'])
    hist, bin_edge = np.histogram(accel_arr, distribution_array)
    fig, ax = plt.subplots()
    ax.bar(range(len(hist)), hist, width=0.5)
    print(hist)
    ax.set_xticks([i - 0.5 for i, j in enumerate(hist)])
    ax.set_xticklabels(['{}'.format(distribution_array[i]) for i,j in enumerate(hist)])
    plt.title(item)
    plt.xlabel('acceleration')
    plt.ylabel('frequency')
    plt.get_current_fig_manager().window.state('zoomed')
    plt.show()


def calculate_acceleration(x, y, z):
    return np.sqrt(x**2 + y**2 + z**2)


def mean_and_std(arr):
    mean = np.mean(arr)
    std = np.std(arr)
    return mean, std


def overall_accel_analysis(arr):
    accel_arr = list(item['total-accel'] for item in arr)
    mean, std = mean_and_std(accel_arr)
    median = np.median(accel_arr)
    min_accel = np.min(accel_arr)
    max_accel = np.max(accel_arr)
    return mean, std, median, min_accel, max_accel


with open(os.path.join(os.getcwd(), '../data/B1-lab.json'), 'r') as json_file:
    i = 0
    cur_pos = 'bottom-right'
    cur_map = {}
    for line in json_file:
        # if i == 50000:
        #     break
        # if i % 50000 == 0:
        #     for item in d:
        #         plot_acceleration(d, item)
        #     d = dict()
        #     cur_map = []
        try:
            line = line[0: len(line)-2]
            temp = line.split(':', 1)
            value = json.loads(temp[1])
            if 'accel' in value:
                value['total-accel'] = calculate_acceleration(int(value['accel']['x']), int(value['accel']['y']), int(value['accel']['z']))
            str = temp[0].replace('"', '')
            if str != cur_pos:
                cur_pos = str

                plot_acceleration(cur_map, cur_pos)

                cur_map = {}
            else:
                if 'accel' in value and str in pos_array and 'timestamp' in value:
                    if str not in d:
                        d[str] = {'accel': [value]}
                    elif 'accel' not in d[str]:
                        d[str]['accel'] = [value]
                    else:
                        d[str]['accel'].append(value)

                    if str not in cur_map:
                        cur_map[str] = {'accel': [value]}
                    elif 'accel' not in cur_map[str]:
                        cur_map[str]['accel'] = [value]
                    else:
                        cur_map[str]['accel'].append(value)

                elif 'magnto' in value and str in pos_array and 'timestamp' in value:
                    if str not in d:
                        d[str] = {'magnto': [value]}
                    elif 'magnto' not in d[str]:
                        d[str]['magnto'] = [value]
                    else:
                        d[str]['magnto'].append(value)
            i += 1
        except:
            continue
    for item in d:
        tup = overall_accel_analysis(d[item]['accel'])
        print(item)
        print('mean', tup[0], 'std', tup[1], 'median', tup[2], 'min', tup[3], 'max', tup[4], '\n')
        # plot_distribution(d, item)
        # plot_acceleration(d, item)