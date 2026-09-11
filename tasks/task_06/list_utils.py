def find_max(items):
    return max(items)


def remove_duplicates(items):
    return list(dict.fromkeys(items))


def count_positive(items):
    return sum(1 for item in items if item > 0)