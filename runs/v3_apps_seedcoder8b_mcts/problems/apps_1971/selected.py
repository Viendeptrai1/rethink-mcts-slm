def find_permutation_q(n, p):
    # Create a list to store the position of each element in p
    position = [0] * (n + 1)
    for i in range(n):
        position[p[i]] = i + 1

    # Create the permutation q
    q = [0] * n
    for i in range(1, n + 1):
        q[i - 1] = position[position[i]]

    # Verify if q^2 == p
    if square_permutation(q) == p:
        return q
    else:
        return [-1]

def square_permutation(q):
    n = len(q)
    p = [0] * n
    for i in range(n):
        p[i] = q[q[i] - 1]
    return p

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    p = list(map(int, data[1:n+1]))
    
    result = find_permutation_q(n, p)
    if result == [-1]:
        print(-1)
    else:
        print(" ".join(map(str, result)))

if __name__ == "__main__":
    main()