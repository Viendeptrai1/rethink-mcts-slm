import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = []
    for i in range(n):
        a.append(int(data[i+1]))
    
    a.sort(reverse=True)
    
    alice_score = 0
    bob_score = 0
    
    for i in range(n):
        if i % 2 == 0:
            alice_score += a[i]
        else:
            bob_score += a[i]
            
    print(alice_score - bob_score)

if __name__ == "__main__":
    solve()