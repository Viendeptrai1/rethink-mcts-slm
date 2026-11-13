def is_real_puzzle(n, active_tooth_sequence):
    for start in range(n):
        sequence = []
        current = start
        for i in range(n):
            sequence.append(current)
            if i % 2 == 0:
                current = (current + 1) % n
            else:
                current = (current - 1 + n) % n
        if sequence == list(range(n)):
            return "Yes"
    return "No"

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    active_tooth_sequence = list(map(int, data[1:]))
    print(is_real_puzzle(n, active_tooth_sequence))

if __name__ == "__main__":
    main()