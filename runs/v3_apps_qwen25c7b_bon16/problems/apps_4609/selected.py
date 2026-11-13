def count_numbers(N, A):
    sheet = set()
    for num in A:
        if num in sheet:
            sheet.remove(num)
        else:
            sheet.add(num)
    return len(sheet)

# Example usage
import sys
input = sys.stdin.read
data = input().split()
N = int(data[0])
A = list(map(int, data[1:]))

print(count_numbers(N, A))