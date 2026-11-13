def make_a_pile(n):
    pile = [n]
    for i in range(1, n):
        if pile[-1] % 2 == 0:
            pile.append(pile[-1] + 2)
        else:
            pile.append(pile[-1] + 2)
    return pile