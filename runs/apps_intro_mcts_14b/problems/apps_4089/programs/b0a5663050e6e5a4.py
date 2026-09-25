import sys

def get_dog_name(N):
    if N <= 26:
        return chr(ord('a') + N - 1)
    
    length = 1
    while True:
        num_names_of_length = 26 ** length
        if N <= num_names_of_length:
            break
        N -= num_names_of_length
        length += 1
    
    name = []
    for _ in range(length):
        N -= 1
        name.append(chr(ord('a') + N % 26))
        N //= 26
    
    return ''.join(reversed(name))

if __name__ == "__main__":
    N = int(sys.stdin.read().strip())
    print(get_dog_name(N))