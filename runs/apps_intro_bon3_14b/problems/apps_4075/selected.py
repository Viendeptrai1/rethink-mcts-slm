import sys
from itertools import product

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    M = int(data[1])
    
    index = 2
    bulbs = []
    for _ in range(M):
        k_i = int(data[index])
        switches = list(map(int, data[index+1:index+1+k_i]))
        index += 1 + k_i
        bulbs.append((switches, int(data[index])))
        index += 1
    
    count = 0
    for switch_states in product([0, 1], repeat=N):
        all_lit = True
        for switches, p_i in bulbs:
            on_count = sum(switch_states[s-1] for s in switches)
            if on_count % 2 != p_i:
                all_lit = False
                break
        if all_lit:
            count += 1
    
    print(count)

if __name__ == "__main__":
    main()