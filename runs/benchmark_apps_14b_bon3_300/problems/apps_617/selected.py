import sys

def max_expression_value(s):
    n = len(s)
    nums = [int(s[i]) for i in range(0, n, 2)]
    ops = [s[i] for i in range(1, n, 2)]
    
    def evaluate(i, j, k):
        if k == -1:
            return nums[i] if ops[i] == '+' else nums[i] * nums[j]
        if ops[k] == '+':
            return evaluate(i, k, k-1) + evaluate(k+1, j, k)
        else:
            return evaluate(i, k, k-1) * evaluate(k+1, j, k)
    
    max_value = 0
    for k in range(1, n-1, 2):
        value = evaluate(0, n//2, k)
        max_value = max(max_value, value)
    
    return max_value

if __name__ == "__main__":
    s = sys.stdin.read().strip()
    print(max_expression_value(s))