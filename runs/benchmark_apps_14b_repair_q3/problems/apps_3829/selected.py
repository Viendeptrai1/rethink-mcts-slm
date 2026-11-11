def expected_max(m, n):
    total_probability = 0.0
    for k in range(1, m + 1):
        prob_k = (k / m) ** n
        prob_k_minus_1 = ((k - 1) / m) ** n
        total_probability += (prob_k - prob_k_minus_1) * k
    return total_probability

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    m = int(data[0])
    n = int(data[1])
    result = expected_max(m, n)
    print(f"{result:.12f}")

if __name__ == "__main__":
    main()