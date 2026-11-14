import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    A = int(input_data[0])
    B_str = input_data[1]
    B_int = int(B_str.replace('.', ''))
    result = (A * B_int) // 100
    print(result)

if __name__ == '__main__':
    solve()