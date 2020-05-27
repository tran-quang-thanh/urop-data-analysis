import json
import os
from code.convert import convert_to_g
from code.fix_timestamp import update_timestamp

pos_array = ['bottom-right', "bottom-left", 'center', 'top-right', 'top-left']
all_pos = set()


def remove_false_reading(reading_value):
    if 'timestamp' not in reading_value or\
            ('magnto' not in reading_value and 'accel' not in reading_value):
        raise Exception
    fixed_value = dict()
    fixed_value['timestamp'] = int(reading_value['timestamp'])
    if 'magnto' in reading_value:
        raw_reading_magnto = reading_value['magnto']
        if 'x' not in raw_reading_magnto or 'y' not in raw_reading_magnto or\
                'z' not in raw_reading_magnto:
            raise Exception
        fixed_value['x'] = convert_to_g(int(raw_reading_magnto['x']))
        fixed_value['y'] = convert_to_g(int(raw_reading_magnto['y']))
        fixed_value['z'] = convert_to_g(int(raw_reading_magnto['z']))
        return fixed_value, 'magnto'
    else:
        raw_reading_accel = reading_value['accel']
        if 'x' not in raw_reading_accel or 'y' not in raw_reading_accel or \
                'z' not in raw_reading_accel:
            raise Exception
        fixed_value['x'] = convert_to_g(int(raw_reading_accel['x']))
        fixed_value['y'] = convert_to_g(int(raw_reading_accel['y']))
        fixed_value['z'] = convert_to_g(int(raw_reading_accel['z']))
        return fixed_value, 'accel'


def read_file():
    with open(os.path.join(os.getcwd(), '../data/B1-lab.json'), 'r') as json_file:
        accel_bottom_right = []
        accel_bottom_left = []
        accel_center = []
        accel_top_right = []
        accel_top_left = []
        magnto_bottom_right = []
        magnto_bottom_left = []
        magnto_center = []
        magnto_top_right = []
        magnto_top_left = []
        count = 0
        throwdata = 0
        for line in json_file:
            count += 1
            try:
                line = line[0: len(line)-2]
                temp = line.split(':', 1)
                reading_value = json.loads(temp[1])
                position = temp[0].replace('"', '')
                all_pos.add(position)
                value, device = remove_false_reading(reading_value)

                if device == 'magnto':
                    if position == 'bottom-right':
                        magnto_bottom_right.append(value)
                    elif position == 'bottom-left':
                        magnto_bottom_left.append(value)
                    elif position == 'center':
                        magnto_center.append(value)
                    elif position == 'top-right':
                        magnto_top_right.append(value)
                    elif position == 'top-left':
                        magnto_top_left.append(value)
                elif device == 'accel':
                    if position == 'bottom-right':
                        accel_bottom_right.append(value)
                    elif position == 'bottom-left':
                        accel_bottom_left.append(value)
                    elif position == 'center':
                        accel_center.append(value)
                    elif position == 'top-right':
                        accel_top_right.append(value)
                    elif position == 'top-left':
                        accel_top_left.append(value)
            except Exception:
                throwdata += 1
                continue
        accel_data = {
            'bottom-right': update_timestamp(accel_bottom_right),
            'bottom-left': update_timestamp(accel_bottom_left),
            'center': update_timestamp(accel_center),
            'top-right': update_timestamp(accel_top_right),
            'top-left': update_timestamp(accel_top_left)
        }
        magnto_data = {
            'bottom-right': update_timestamp(magnto_bottom_right),
            'bottom-left': update_timestamp(magnto_bottom_left),
            'center': update_timestamp(magnto_center),
            'top-right': update_timestamp(magnto_top_right),
            'top-left': update_timestamp(magnto_top_left)
        }
        return accel_data, magnto_data
