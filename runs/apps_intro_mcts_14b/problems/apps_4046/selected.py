import sys

def restore_permutation(n, q):
    # Try starting the permutation with each possible value from 1 to n
    for start in range(1, n + 1):
        p = [start]
        valid = True
        for i in range(n - 1):
            next_value = p[-1] + q[i]
            if next_value < 1 or next_value > n or next_value in p:
                valid = False
                break
            p.append(next_value)
        if valid:
            return p
    return None

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    q = list(map(int, data[1:]))
    
    result = restore_permutation(n, q)
    if result is None:
        print(-1)
    else:
        print(" ".join(map(str, result)))

if __name__ == "__main__":
    main()