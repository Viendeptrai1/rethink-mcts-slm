import sys

def can_sort_with_ravioli(n, arr):
    def simulate_ravioli_sort(arr):
        while len(arr) > 1:
            max_height = max(arr)
            max_index = arr.index(max_height)
            if max_index > 0 and arr[max_index] - arr[max_index - 1] >= 2:
                return False
            if max_index < len(arr) - 1 and arr[max_index] - arr[max_index + 1] >= 2:
                return False
            arr.pop(max_index)
        return True

    if simulate_ravioli_sort(arr[:]):
        return "YES"
    else:
        return "NO"

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    arr = list(map(int, data[1:]))
    result = can_sort_with_ravioli(n, arr)
    print(result)

if __name__ == "__main__":
    main()