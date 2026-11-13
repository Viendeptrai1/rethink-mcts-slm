import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        n = int(next(iterator))
    except StopIteration:
        return

    citations = []
    for _ in range(n):
        citations.append(int(next(iterator)))

    citations.sort(reverse=True)

    h_index = 0
    for i, c in enumerate(citations):
        if c >= i + 1:
            h_index = i + 1
        else:
            break

    print(h_index)

if __name__ == "__main__":
    solve()