import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    a = [int(x) for x in input_data[1:]]

    a.sort(reverse=True)

    first_pair = -1
    second_pair = -1

    for i in range(n - 1):
        if a[i] == a[i + 1]:
            if first_pair == -1:
                first_pair = a[i]
            else:
                second_pair = a[i]
                break

    if first_pair != -1 and second_pair != -1:
        print(first_pair * second_pair)
    else:
        print(0)

if __name__ == "__main__":
    solve()