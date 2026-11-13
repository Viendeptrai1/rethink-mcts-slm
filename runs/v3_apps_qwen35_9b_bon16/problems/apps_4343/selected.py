import sys

def solve():
    input = sys.stdin.read().split()
    k = int(input[0])
    s = input[1]
    t = input[2]

    base = ord('a')
    top = base + 25

    # Convert strings to integer values in base 26
    val_s = 0
    for ch in s:
        val_s = val_s * 26 + (ord(ch) - base)

    val_t = 0
    for ch in t:
        val_t = val_t * 26 + (ord(ch) - base)

    # Calculate median value
    # Number of elements = val_t - val_s + 1
    # Median index (0-based) = (count - 1) // 2
    # Median value = val_s + index
    count = val_t - val_s + 1
    median_val = val_s + (count - 1) // 2

    # Convert median value back to string
    result = []
    temp = median_val
    for _ in range(k):
        result.append(chr(temp % 26 + base))
        temp //= 26
    result.reverse()
    print("".join(result))

if __name__ == "__main__":
    solve()