def any_int(x, y, z):
    if not isinstance(x, int) or not isinstance(y, int) or not isinstance(z, int):
        return False
    return x == y + z or y == x + z or z == x + y