import sys

def main():
    import sys
    import bisect
    
    def solve(n, a):
        left = [0] * n
        right = [0] * n
        
        # Fill left array
        stack = []
        for i in range(n):
            while stack and a[stack[-1]] < a[i]:
                stack.pop()
            if stack:
                left[i] = stack[-1]
            stack.append(i)
        
        # Fill right array
        stack = []
        for i in range(n-1, -1, -1):
            while stack and a[stack[-1]] < a[i]:
                stack.pop()
            if stack:
                right[i] = stack[-1]
            stack.append(i)
        
        # Find the longest increasing subsequence
        lis = []
        for i in range(n):
            pos = bisect.bisect_left(lis, a[i])
            if pos == len(lis):
                lis.append(a[i])
            else:
                lis[pos] = a[i]
        
        k = len(lis)
        path = [''] * k
        j = k - 1
        for i in range(n-1, -1, -1):
            if lis[j] == a[i]:
                if right[i] == 0 or (left[i] != 0 and a[left[i]] < a[right[i]]):
                    path[j] = 'L'
                    i = left[i]
                else:
                    path[j] = 'R'
                    i = right[i]
                j -= 1
        
        return k, ''.join(path)
    
    n = int(sys.stdin.readline().strip())
    a = list(map(int, sys.stdin.readline().strip().split()))
    
    k, s = solve(n, a)
    print(k)
    print(s)

if __name__ == "__main__":
    main()