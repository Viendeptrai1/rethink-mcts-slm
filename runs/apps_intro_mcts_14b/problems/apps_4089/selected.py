import sys

def number_to_name(N):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    name = []
    
    while N > 0:
        N -= 1
        name.append(alphabet[N % 26])
        N //= 26
    
    return ''.join(reversed(name))

if __name__ == "__main__":
    N = int(sys.stdin.read().strip())
    print(number_to_name(N))