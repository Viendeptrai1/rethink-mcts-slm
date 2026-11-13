def max_increasing_sequence(n, a):
    stack = []
    result = []
    left = 0
    right = n - 1
    
    while left <= right:
        if not stack or (a[left] < stack[-1] and a[right] < stack[-1]):
            if left <= right and a[left] < a[right]:
                result.append('L')
                stack.append(a[left])
                left += 1
            else:
                result.append('R')
                stack.append(a[right])
                right -= 1
        elif a[left] < stack[-1]:
            result.append('L')
            stack.append(a[left])
            left += 1
        else:
            result.append('R')
            stack.append(a[right])
            right -= 1
    
    return len(stack), ''.join(result)

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    k, s = max_increasing_sequence(n, a)
    print(k)
    print(s)