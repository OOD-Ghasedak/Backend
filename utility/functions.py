def get_dict_subset(dictionary, keys):
    d = {}
    for key in keys:
        d[key] = dictionary[key]
    return d
