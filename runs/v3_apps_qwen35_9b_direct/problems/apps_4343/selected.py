import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    k = int(input_data[0])
    s = input_data[1]
    t = input_data[2]
    
    # Convert strings to integer values where 'a' -> 0, 'b' -> 1, ..., 'z' -> 25
    # The total number of strings of length k is 26^k.
    # We can treat each string as a base-26 number.
    
    def str_to_int(st):
        res = 0
        for char in st:
            res = res * 26 + (ord(char) - ord('a'))
        return res
    
    def int_to_str(val, length):
        chars = []
        for _ in range(length):
            chars.append(chr((val % 26) + ord('a')))
            val //= 26
        return ''.join(reversed(chars))
    
    val_s = str_to_int(s)
    val_t = str_to_int(t)
    
    # The median is the average of the two endpoints since the count is odd.
    # median = (s + t) / 2
    median_val = (val_s + val_t) // 2
    
    print(int_to_str(median_val, k))

if __name__ == "__main__":
    solve()