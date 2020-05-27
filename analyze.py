import numpy as np
import code.clean as dc


def get_total(value):
    return np.sqrt(value['x'] ** 2 + value['y'] ** 2 + value['z'] ** 2)


def std_and_mean(array):
    timestamp = array[0]['timestamp']
    mean = np.mean([item['total'] for item in array])
    std = np.std([item['total'] for item in array])
    return timestamp, mean, std


def analyze():
    accel_data, magnto_data = dc.read_file()
    for _, array in accel_data.items():
        i = 0
        while i < len(array):
            total = get_total(array[i])
            if total < 2:
                array[i]['total'] = total
                i += 1
            else:
                array.pop(i)

    for _, array in magnto_data.items():
        for value in array:
            value['total'] = get_total(value)

    accel = dict()
    for pos, array in accel_data.items():
        data = []
        sub_array = [array[0]]
        start_time = array[0]['timestamp']
        for i in range(1, len(array)):
            if array[i]['timestamp'] - start_time < 120:
                sub_array.append(array[i])
            else:
                if len(sub_array) > 20:
                    data.append(std_and_mean(sub_array))
                start_time = array[i]['timestamp']
                sub_array = [array[i]]
        accel[pos] = data
    return accel
