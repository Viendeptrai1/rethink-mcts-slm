import sys

def find_first_multiple_of_k(K):
    current_number = 7
    remainder_set = set()
    position = 1
    
    while True:
        if current_number % K == 0:
            return position
        remainder = current_number % K
        if remainder in remainder_set:
            return -1
        remainder_set.add(remainder)
        current_number = current_number * 10 + 7
        position += 1

if __name__ == "__main__":
    K = int(sys.stdin.read().strip())
    result = find_first_multiple_of_k(K)
    sys.stdout.write(str(result))