import sys
input = sys.stdin.read

def solve():
    data = input().split()
    iterator = iter(data)
    
    N = int(next(iterator))
    A = []
    for _ in range(N + 1):
        A.append(int(next(iterator)))
    B = []
    for _ in range(N):
        B.append(int(next(iterator)))
    
    total_defeated = 0
    remaining = [0] * (N + 1)
    for i in range(N + 1):
        remaining[i] = A[i]
    
    for i in range(N):
        # Hero i can fight town i and town i+1
        # Priority: fight town i first, then town i+1
        
        # Fight town i
        can_fight_i = min(remaining[i], B[i])
        total_defeated += can_fight_i
        remaining[i] -= can_fight_i
        B[i] -= can_fight_i
        
        # Fight town i+1
        can_fight_next = min(remaining[i + 1], B[i])
        total_defeated += can_fight_next
        remaining[i + 1] -= can_fight_next
        B[i] -= can_fight_next
    
    print(total_defeated)

if __name__ == "__main__":
    solve()