from typing import List

def compare(game: List[int], guess: List[int]) -> List[int]:
    return [abs(game[i] - guess[i]) for i in range(len(game))]