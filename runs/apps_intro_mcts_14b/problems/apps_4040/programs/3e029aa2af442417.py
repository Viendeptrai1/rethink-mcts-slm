import sys

def can_reach_end(n, m, d, c):
    if d >= n:
        return "YES", [0] * n
    
    total_length = sum(c)
    if total_length < n:
        return "NO", []
    
    # Try to place platforms in a way that allows reaching the end
    platforms = [0] * n
    current_position = 0
    platform_index = 0
    
    while current_position < n:
        if platform_index >= m:
            return "NO", []
        
        if current_position + c[platform_index] > n:
            return "NO", []
        
        for i in range(current_position, current_position + c[platform_index]):
            platforms[i] = platform_index + 1
        
        current_position += c[platform_index]
        platform_index += 1
    
    # Check if we can jump from one platform to another
    current_position = 0
    while current_position < n:
        if platforms[current_position] == 0:
            return "NO", []
        
        found_jump = False
        for next_position in range(current_position + 1, min(current_position + d + 1, n)):
            if platforms[next_position] != 0:
                current_position = next_position
                found_jump = True
                break
        
        if not found_jump:
            return "NO", []
    
    return "YES", platforms

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    d = int(data[2])
    c = list(map(int, data[3:3+m]))
    
    result, platforms = can_reach_end(n, m, d, c)
    print(result)
    if result == "YES":
        print(" ".join(map(str, platforms)))

if __name__ == "__main__":
    main()