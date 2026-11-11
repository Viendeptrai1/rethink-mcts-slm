def fib4(n: int) -> int:
    if n == 0:
        return 0
    elif n == 1:
        return 0
    elif n == 2:
        return 2
    elif n == 3:
        return 0

    # Initialize the first four numbers of the sequence
    fib4_values = [0, 0, 2, 0]

    # Compute the sequence iteratively
    for i in range(4, n + 1):
        next_value = sum(fib4_values)
        # Update the list to hold the last four values
        fib4_values = fib4_values[1:] + [next_value]

    return fib4_values[-1]