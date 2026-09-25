import sys

def main():
    import sys
    import math
    
    def read_input():
        import sys
        return sys.stdin.read().split()
    
    data = read_input()
    n = int(data[0])
    k = int(data[1])
    s = data[2]
    
    max_subsequences = 2 ** n
    
    if k > max_subsequences:
        print(-1)
        return
    
    # Calculate the minimum cost
    cost = 0
    current_size = 1  # Start with the empty subsequence
    while current_size < k:
        next_size = min(k, current_size * 2)
        cost += (n * (next_size - current_size))
        current_size = next_size
    
    print(cost)

if __name__ == "__main__":
    main()