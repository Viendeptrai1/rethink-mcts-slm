def any_int(x, y, z):
    if not (isinstance(x, int) and isinstance(y, int) and isinstance(z, int)):
        return False
    if x == y + z:
        return True
    if y == x + z:
        return True
    if z == x + y:
        return True
    return False