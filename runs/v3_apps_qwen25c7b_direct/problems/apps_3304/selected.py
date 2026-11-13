def max_victories(N, A, P, V):
    # Create a list of tuples (dwarf_strength, elf_strength, elf_index)
    combined = [(P[i], V[i], i) for i in range(N)]
    
    # Sort the list based on dwarf strength and then by elf strength in descending order
    combined.sort(key=lambda x: (x[0], -x[1]))
    
    # Initialize variables
    visited = [False] * N
    victories = 0
    
    # Iterate through the sorted list
    for _, _, elf_index in combined:
        # Find the target dwarf
        target_dwarf = A[elf_index]
        
        # Try to find an unvisited seat for the elf
        for i in range(N):
            if not visited[(target_dwarf + i - 1) % N]:
                visited[(target_dwarf + i - 1) % N] = True
                victories += 1
                break
    
    return victories

# Example usage
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    A = list(map(int, data[1:N+1]))
    P = list(map(int, data[N+1:2*N+1]))
    V = list(map(int, data[2*N+1:3*N+1]))
    
    result = max_victories(N, A, P, V)
    print(result)