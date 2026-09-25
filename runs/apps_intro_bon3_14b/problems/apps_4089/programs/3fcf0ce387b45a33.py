import sys

def get_dog_name(N):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    length = 1
    while True:
        count = 26 ** length
        if N <= count:
            return ''.join(alphabet[(N - 1) // (26 ** i) % 26] for i in range(length - 1, -1, -1))
        N -= count
        length += 1

if __name__ == "__main__":
    N = int(sys.stdin.read().strip())
    print(get_dog_name(N))