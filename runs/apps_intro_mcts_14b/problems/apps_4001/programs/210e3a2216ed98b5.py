import sys
from collections import Counter

def get_divisors(n):
    divisors = set()
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            divisors.add(i)
            divisors.add(n // i)
    return divisors

def find_x_y(n, divisors_list):
    counter = Counter(divisors_list)
    total_divisors = set(divisors_list)
    
    for x in total_divisors:
        div_x = get_divisors(x)
        remaining_divs = total_divisors - div_x
        for y in remaining_divs:
            div_y = get_divisors(y)
            combined_divs = div_x.union(div_y)
            combined_counter = Counter()
            for d in combined_divs:
                if d in div_x and d in div_y:
                    combined_counter[d] += 2
                else:
                    combined_counter[d] += 1
            if combined_counter == counter:
                return x, y
    return None, None

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    divisors_list = list(map(int, data[1:]))
    
    x, y = find_x_y(n, divisors_list)
    print(x, y)

if __name__ == "__main__":
    main()