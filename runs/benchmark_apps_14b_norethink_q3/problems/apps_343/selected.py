import sys
import bisect

def main():
    import sys
    import bisect
    
    def solve(n, k, p, x, y, a):
        remaining_tests = n - k
        current_sum = sum(a)
        max_possible_sum = current_sum + remaining_tests * p
        
        if max_possible_sum < x:
            return "-1"
        
        a.sort()
        median_position = (n + 1) // 2
        
        # Check if we can meet the median requirement
        if a[median_position - 1] >= y:
            # We already have enough high marks
            remaining_marks = [y] * remaining_tests
            if sum(remaining_marks) + current_sum <= x:
                return " ".join(map(str, remaining_marks))
            else:
                return "-1"
        
        # We need to increase some marks to meet the median requirement
        needed_high_marks = median_position - bisect.bisect_left(a, y)
        if needed_high_marks > remaining_tests:
            return "-1"
        
        remaining_marks = [y] * needed_high_marks + [1] * (remaining_tests - needed_high_marks)
        if sum(remaining_marks) + current_sum <= x:
            return " ".join(map(str, remaining_marks))
        else:
            return "-1"
    
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    p = int(data[2])
    x = int(data[3])
    y = int(data[4])
    a = list(map(int, data[5:5+k]))
    
    result = solve(n, k, p, x, y, a)
    print(result)

if __name__ == "__main__":
    main()