def convert_to_int(value, default: int = 0):
    try:
        return int(value)
    except TypeError:
        return default
