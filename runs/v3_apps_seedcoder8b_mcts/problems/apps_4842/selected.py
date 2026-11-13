def find_degree_and_next_value(n, values):
    def compute_differences(vals):
        return [vals[i + 1] - vals[i] for i in range(len(vals) - 1)]

    def is_constant(lst):
        return all(x == lst[0] for x in lst)

    differences = values
    degree = 0

    while not is_constant(differences) and len(differences) > 1:
        differences = compute_differences(differences)
        degree += 1

    # Calculate the next value
    if degree == 0:
        # Linear case, constant difference
        next_value = values[-1] + (values[-1] - values[-2])
    else:
        # Use the difference table to predict the next value
        next_value = values[-1]
        for i in range(degree):
            next_value += differences[i]

    return degree, next_value

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    n = int(data[0])
    values = list(map(int, data[1:n+1]))
    degree, next_value = find_degree_and_next_value(n, values)
    print(degree, next_value)