Here's the Python solution to the problem:

import sys

def solve():
    n = int(input())
    cards = list(map(int, input().split()))
    
    left = 0
    while left < n - 1 and cards[left] <= cards[left + 1]:
        left += 1
    
    if left == n - 1:
        print("impossible")
        return
    
    right = n - 1
    while right > 0 and cards[right] >= cards[right - 1]:
        right -= 1
    
    reversed_subarray = cards[left:right+1][::-1]
    
    new_cards = cards[:left] + reversed_subarray + cards[right+1:]
    
    if new_cards == sorted(cards):
        print(f"{left + 1} {right + 1}")
    else:
        print("impossible")

if __name__ == "__main__":
    solve()