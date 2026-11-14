import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    k = int(input_data[0])
    s = input_data[1]
    t = input_data[2]
    
    # Convert strings to integers (base 26)
    # 'a' -> 0, 'b' -> 1, ..., 'z' -> 25
    def str_to_int(st):
        res = 0
        for char in st:
            res = res * 26 + (ord(char) - ord('a'))
        return res
    
    def int_to_str(num, length):
        chars = []
        for _ in range(length):
            chars.append(chr((num % 26) + ord('a')))
            num //= 26
        return ''.join(reversed(chars))
    
    val_s = str_to_int(s)
    val_t = str_to_int(t)
    
    # Calculate median
    # Since the count is guaranteed to be odd, (val_s + val_t) is even
    median_val = (val_s + val_t) // 2
    
    result = int_to_str(median_val, k)
    print(result)

if __name__ == "__main__":
    solve()