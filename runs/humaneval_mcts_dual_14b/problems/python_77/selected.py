def iscube(a):
    if a == 0:
        return True
    abs_a = abs(a)
    n = round(abs_a ** (1/3))
    return n**3 == abs_a

# Test cases
print(iscube(1))   # True
print(iscube(2))   # False
print(iscube(-1))  # True
print(iscube(64))  # True
print(iscube(0))   # True
print(iscube(180)) # False