import sys

def main():
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    a = list(map(int, data[1:]))
    
    # Sort the array in descending order
    a.sort(reverse=True)
    
    # Calculate the difference between the sum of elements at even indices and the sum of elements at odd indices
    alice_score = sum(a[i] for i in range(0, N, 2))
    bob_score = sum(a[i] for i in range(1, N, 2))
    
    # Print Alice's score minus Bob's score
    print(alice_score - bob_score)

if __name__ == "__main__":
    main()