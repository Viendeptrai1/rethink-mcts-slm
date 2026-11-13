def reconstruct_ring():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    ring = list(map(int, data[1:]))
    
    original_ring = [0] * N
    
    for i in range(N):
        original_ring[i] = ring[i] - ring[(i - 1) % N] - ring[(i + 1) % N]
    
    for number in original_ring:
        print(number)