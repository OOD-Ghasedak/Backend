def get_dict_subset(dictionary, keys, abort_on_not_found=True):
    d = {}
    for key in keys:
        try:
            d[key] = dictionary[key]
        except KeyError as e:
            if abort_on_not_found:
                raise e
    return d
