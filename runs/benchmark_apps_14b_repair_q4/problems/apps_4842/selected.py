import sys

def read_input():
    import sys
    return sys.stdin.read().strip()

def process_input(input_data):
    lines = input_data.splitlines()
    n = int(lines[0])
    values = list(map(int, lines[1].split()))
    return n, values

def calculate_differences(values):
    differences = []
    while len(values) > 1:
        diff = [values[i+1] - values[i] for i in range(len(values)-1)]
        differences.append(diff)
        values = diff
    return differences

def find_degree(differences):
    for i, diff in enumerate(differences):
        if len(set(diff)) != 1:
            return i
    return len(differences)

def predict_next_value(differences, last_value):
    if not differences:
        return last_value
    last_diff = differences[-1][0]
    return last_value + last_diff

def main():
    input_data = read_input()
    n, values = process_input(input_data)
    differences = calculate_differences(values)
    degree = find_degree(differences)
    next_value = predict_next_value(differences, values[-1])
    print(degree, next_value)

if __name__ == "__main__":
    main()