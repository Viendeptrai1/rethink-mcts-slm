import sys
from itertools import product

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    M = int(data[1])
    
    index = 2
    connections = []
    for _ in range(M):
        k_i = int(data[index])
        switches = list(map(int, data[index+1:index+1+k_i]))
        connections.append(switches)
        index += 1 + k_i
    
    parities = list(map(int, data[index:]))
    
    count = 0
    for switch_states in product([0, 1], repeat=N):
        all_lit = True
        for i in range(M):
            on_count = sum(switch_states[j-1] for j in connections[i])
            if on_count % 2 != parities[i]:
                all_lit = False
                break
        if all_lit:
            count += 1
    
    print(count)

if __name__ == "__main__":
    main()