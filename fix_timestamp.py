MAX = 2*(2**31)


def update(prev_timestamp, timestamp, adder):
    if prev_timestamp / timestamp < 0 and timestamp < prev_timestamp:
        adder += 1
    new_timestamp = timestamp + adder * MAX
    return timestamp, new_timestamp, adder


def is_edit(arr, i):
    return i < len(arr) - 1 and not (2 > arr[i]['timestamp'] / arr[i-1]['timestamp'] > 1/2)\
            and not (2 > arr[i]['timestamp'] / arr[i+1]['timestamp'] > 1/2)


def update_timestamp(arr):
    prev_timestamp = arr[0]['timestamp']
    adder = 0
    i = 1
    while i < len(arr):
        if is_edit(arr, i):
            if abs(arr[i - 1]['timestamp'] - arr[i + 1]['timestamp']) < 10:
                arr[i]['timestamp'] = arr[i + 1]['timestamp']
            else:
                arr.pop(i)
                i -= 1
        i += 1

    i = 1
    while i < len(arr):
        timestamp = arr[i]['timestamp']
        prev_timestamp, new_timestamp, adder = update(prev_timestamp, timestamp, adder)
        arr[i]['timestamp'] = new_timestamp
        i += 1
    return arr
