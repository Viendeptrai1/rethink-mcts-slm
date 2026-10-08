import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    N = int(data[index])
    Q = int(data[index + 1])
    index += 2
    
    boxes = [0] * min(10**6, N)  # We only need to keep track of up to 10^6 boxes due to memory constraints
    
    for _ in range(Q):
        query_type = int(data[index])
        index += 1
        
        if query_type == 1:
            L = int(data[index]) - 1
            R = int(data[index + 1]) - 1
            A = int(data[index + 2])
            B = int(data[index + 3])
            index += 4
            
            for X in range(L, R + 1):
                boxes[X % len(boxes)] = ((X - L + 1) * A) % B
        
        elif query_type == 2:
            L = int(data[index]) - 1
            R = int(data[index + 1]) - 1
            index += 2
            
            total_stones = 0
            for X in range(L, R + 1):
                total_stones += boxes[X % len(boxes)]
            
            print(total_stones)

if __name__ == "__main__":
    main()