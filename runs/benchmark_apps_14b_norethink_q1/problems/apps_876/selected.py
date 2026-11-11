import sys

def find_minimum_i(n, k, A0):
    current_array = A0
    i = 0
    
    while True:
        if any(x >= k for x in current_array):
            return i
        
        # Compute the next array in the sequence
        next_array = [0] * (n + 1)
        for j in range(1, n + 1):
            next_array[j] = next_array[j - 1] + current_array[j - 1]
        
        current_array = next_array
        i += 1

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    A0 = list(map(int, data[2:2+n]))
    
    result = find_minimum_i(n, k, A0)
    print(result)

if __name__ == "__main__":
    main()