import sys

def reconstruct_ring(N, sums):
    # Initialize the original ring with zeros
    original = [0] * N
    
    # Set the first element to an arbitrary value
    original[0] = sums[0] - sums[N-1] - sums[1]
    
    # Reconstruct the rest of the elements
    for i in range(1, N):
        original[i] = sums[i] - sums[i-1] - original[i-1]
    
    return original

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    sums = list(map(int, data[1:]))
    
    original = reconstruct_ring(N, sums)
    
    for num in original:
        print(num)

if __name__ == "__main__":
    main()