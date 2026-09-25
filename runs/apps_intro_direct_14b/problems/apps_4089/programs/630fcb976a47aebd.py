import sys

def get_dog_name(N):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    length = 1
    while True:
        count = 26 ** length
        if N <= count:
            break
        N -= count
        length += 1
    
    name = ''
    for _ in range(length):
        N -= 1
        name = alphabet[N % 26] + name
        N //= 26
    
    return name

if __name__ == "__main__":
    N = int(sys.stdin.read().strip())
    print(get_dog_name(N))