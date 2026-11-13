def max_victories(N, A, P, V):
    from collections import deque

    # Create a list of tuples (dwarf_strength, elf_strength, elf_index)
    dwarves = [(P[i], V[i], i) for i in range(N)]
    # Sort dwarves by strength in descending order
    dwarves.sort(reverse=True, key=lambda x: x[0])

    # Create a deque for the elves
    elf_queue = deque(sorted(range(N), key=lambda i: V[i], reverse=True))

    # Create a list to keep track of which elves are sitting
    sitting_elves = [None] * N

    # Create a list to keep track of the next available dwarf
    next_dwarf = list(range(N))

    victories = 0

    for _, _, elf_index in dwarves:
        adversary = A[elf_index] - 1  # Convert to 0-based index
        if sitting_elves[adversary] is None:
            # If the adversary is not sitting, sit the elf there
            sitting_elves[adversary] = elf_index
        else:
            # Otherwise, find the next available dwarf
            current = adversary
            while sitting_elves[next_dwarf[current]] is not None:
                current = (current + 1) % N
            sitting_elves[next_dwarf[current]] = elf_index

    # Count the number of victories
    for i in range(N):
        if sitting_elves[i] is not None and V[sitting_elves[i]] > P[i]:
            victories += 1

    return victories

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