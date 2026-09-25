import sys

def can_sort_with_ravioli(n, arr):
    def simulate_sliding(arr):
        while True:
            changed = False
            for i in range(len(arr) - 1):
                if arr[i] >= arr[i + 1] + 2:
                    arr[i] -= 1
                    arr[i + 1] += 1
                    changed = True
            if not changed:
                break
        return arr

    def is_sorted(arr):
        return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))

    original_arr = arr[:]
    arr = simulate_sliding(arr)
    sorted_arr = sorted(original_arr)

    return "YES" if arr == sorted_arr else "NO"

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