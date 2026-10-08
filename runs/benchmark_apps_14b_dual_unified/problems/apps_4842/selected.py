import sys

def find_next_value_and_degree(n, values):
    def calculate_differences(seq):
        return [seq[i] - seq[i-1] for i in range(1, len(seq))]

    differences = values[:]
    degree = 0

    while True:
        differences = calculate_differences(differences)
        degree += 1
        if all(x == differences[0] for x in differences):
            break

    # Calculate the next value in the sequence
    next_value = values[-1] + differences[0]
    return degree, next_value

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    values = list(map(int, data[1:]))
    degree, next_value = find_next_value_and_degree(n, values)
    print(degree, next_value)

if __name__ == "__main__":
    main()