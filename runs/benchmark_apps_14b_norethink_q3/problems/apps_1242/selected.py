import sys

def get_reversals(s):
    n = len(s)
    result = [0] * n
    s = list(s)
    
    for i in range(n):
        if s[i] == 'b':
            # Try to bring 'a' to the front by reversing the prefix
            j = i
            while j >= 0 and s[j] == 'b':
                j -= 1
            if j >= 0:
                # Reverse the prefix from 0 to j+1
                s[:j+2] = reversed(s[:j+2])
                result[j+1] = 1
    
    return result

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().strip()
    result = get_reversals(data)
    print(" ".join(map(str, result)))