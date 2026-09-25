import sys

def can_sort_with_ravioli(n, arr):
    def will_slide(arr):
        for i in range(1, len(arr)):
            if abs(arr[i] - arr[i - 1]) >= 2:
                return True
        return False

    def sort_ravioli(arr):
        sorted_arr = []
        while arr:
            max_height = max(arr)
            max_index = arr.index(max_height)
            sorted_arr.append(max_height)
            arr.pop(max_index)
            arr = [x - 1 if x > 0 else 0 for x in arr]
            arr = [x for x in arr if x > 0]
        return sorted_arr

    if will_slide(arr):
        return "NO"
    
    sorted_arr = sort_ravioli(arr.copy())
    if sorted_arr == sorted(arr):
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