import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    a = [int(x) for x in input_data[1:]]
    
    a.sort(reverse=True)
    
    alice_score = 0
    bob_score = 0
    
    for i in range(n):
        if i % 2 == 0:
            alice_score += a[i]
        else:
            bob_score += a[i]
    
    print(alice_score - bob_score)

if __name__ == '__main__':
    solve()