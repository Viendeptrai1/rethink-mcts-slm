def make_a_pile(n):
    def next_number(x):
        return x + 1 + (x % 2)

    pile = []
    current_stones = n
    for _ in range(n):
        pile.append(current_stones)
        current_stones = next_number(current_stones)
    return pile