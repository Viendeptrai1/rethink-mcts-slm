def any_int(x, y, z):
    if not isinstance(x, int) or not isinstance(y, int) or not isinstance(z, int):
        return False
    if x + y == z or x + z == y or y + z == x:
        return True
    return False