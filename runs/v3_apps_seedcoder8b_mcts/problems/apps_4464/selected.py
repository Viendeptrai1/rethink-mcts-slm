import sys
import math

def main():
    input_data = sys.stdin.read().strip()
    A, B, C = map(int, input_data.split())
    
    # Check if C is congruent to 0 modulo B
    if C % B == 0:
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    main()