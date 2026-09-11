def get_value(data, key, default=None):
    return data.get(key, default)


def merge_dicts(first, second):
    result = first.copy()
    result.update(second)
    return result


def filter_by_value(data, minimum):
    return {
        key: value
        for key, value in data.items()
        if value >= minimum
    }