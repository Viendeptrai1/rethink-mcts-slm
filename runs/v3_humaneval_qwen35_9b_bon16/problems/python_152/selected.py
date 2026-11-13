def compare(game, guess):
    return [abs(g - s) for s, g in zip(game, guess)]