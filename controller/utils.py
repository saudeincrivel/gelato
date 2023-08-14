import json
import numpy as np
import ctypes 
def convert_numbers_to_strings(obj):
    if isinstance(obj, dict):
        new_dict = {}
        for key, value in obj.items():
            if isinstance(value, (int, float)):
                new_dict[key] = str(value)
            elif isinstance(value, dict) or isinstance(value, list):
                new_dict[key] = convert_numbers_to_strings(value)
            else:
                new_dict[key] = value
        return new_dict
    elif isinstance(obj, list):
        new_list = []
        for item in obj:
            if isinstance(item, (int, float)):
                new_list.append(str(item))
            elif isinstance(item, dict) or isinstance(item, list):
                new_list.append(convert_numbers_to_strings(item))
            else:
                new_list.append(item)
        return new_list
    else:
        return obj


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, ctypes.c_int64):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        
    
        return super(NpEncoder, self).default(obj)

