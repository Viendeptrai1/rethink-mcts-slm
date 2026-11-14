import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = [int(data[i+1]) for i in range(n)]
    
    left = 0
    right = n - 1
    last_val = 0
    res = []
    
    while left <= right:
        l_val = a[left]
        r_val = a[right]
        
        if l_val > last_val and r_val > last_val:
            if l_val < r_val:
                res.append('L')
                last_val = l_val
                left += 1
            elif r_val < l_val:
                res.append('R')
                last_val = r_val
                right -= 1
            else:
                # Values are equal
                # We need to check which side allows for a longer increasing sequence
                # Since values are distinct in C1, this case only happens if we are looking at the same element?
                # No, left and right are different indices. But values are distinct, so l_val == r_val is impossible unless left == right.
                # If left == right, then l_val == r_val, and we just pick it.
                if left == right:
                    res.append('L')
                    last_val = l_val
                    left += 1
                    break
                else:
                    # This branch should theoretically not be reached with distinct values unless logic error
                    # But to be safe, if values are equal and distinct indices, it's a contradiction for distinct values problem.
                    # However, let's assume standard distinct logic: this block is unreachable for distinct values.
                    # If it were reachable (e.g. non-distinct), we would need DP.
                    # Given the problem statement says distinct, we can treat this as an error or handle left==right.
                    # Let's re-verify: distinct values means a[left] != a[right] for left != right.
                    # So this else block is only for left == right.
                    res.append('L')
                    last_val = l_val
                    left += 1
                    break
        elif l_val > last_val:
            res.append('L')
            last_val = l_val
            left += 1
        elif r_val > last_val:
            res.append('R')
            last_val = r_val
            right -= 1
        else:
            break
            
    print(len(res))
    print("".join(res))

if __name__ == "__main__":
    solve()