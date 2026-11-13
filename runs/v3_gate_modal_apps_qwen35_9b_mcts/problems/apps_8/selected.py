import sys

def solve():
    try:
        line = sys.stdin.read().strip()
        if not line:
            return
        tiles = line.split()
    except Exception:
        return

    # Parse tiles into (number, suit) tuples
    def parse(t):
        num = int(t[0])
        suit = t[1]
        return (num, suit)

    hand = [parse(t) for t in tiles]

    # Check for existing mentsu (koutsu or shuntsu)
    def has_mentsu(h):
        # Check koutsu: three identical tiles
        from collections import Counter
        counts = Counter(h)
        for k, v in counts.items():
            if v >= 3:
                return True
        # Check shuntsu: three sequential tiles in same suit
        # Group by suit
        suits = {}
        for n, s in h:
            if s not in suits:
                suits[s] = []
            suits[s].append(n)
        for s in suits:
            nums = sorted(suits[s])
            for i in range(len(nums) - 2):
                if nums[i+1] == nums[i] + 1 and nums[i+2] == nums[i] + 2:
                    return True
        return False

    if has_mentsu(hand):
        print(0)
        return

    # Check if we can form a mentsu by adding 1 tile
    # We need to see if there exists a tile t such that hand + [t] contains a mentsu.
    # A mentsu in hand+[t] must use at least 2 tiles from hand (since we only add 1).
    # Possibilities:
    # 1. Koutsu: We have 2 identical tiles in hand. Adding the 3rd makes a koutsu.
    # 2. Shuntsu: We have 2 tiles in the same suit that can form a sequence with one missing number.
    
    def can_form_with_one_add(h):
        from collections import Counter
        # Check for koutsu potential: any tile appearing >= 2 times
        counts = Counter(h)
        for k, v in counts.items():
            if v >= 2:
                return True
        
        # Check for shuntsu potential: any suit with 2 tiles that are 1 apart or same (but same won't help for sequence unless we consider duplicates which don't help sequence directly)
        # Actually for sequence we need two numbers that are either (x, x+1) or (x, x+2)
        # Group by suit
        suits = {}
        for n, s in h:
            if s not in suits:
                suits[s] = set()
            suits[s].add(n)
        
        for s in suits:
            nums = sorted(suits[s])
            # Check pairs
            for i in range(len(nums)):
                for j in range(i+1, len(nums)):
                    a, b = nums[i], nums[j]
                    if b == a + 1:
                        # Missing a-1 or b+1
                        return True
                    elif b == a + 2:
                        # Missing a+1
                        return True
        return False

    if can_form_with_one_add(hand):
        print(1)
        return

    # Check if we can form a mentsu by adding 2 tiles
    # If we don't have 2 identical tiles and no two tiles can form a sequence with 1 addition,
    # then we need to add 2 tiles to form a new mentsu from scratch (e.g., add 2 tiles to make a triplet or sequence with the existing 1 tile, or just ignore existing and make a new one? 
    # Actually, with 3 tiles initially, if we add 2, we have 5 tiles. We just need to find if there exists a subset of 3 that forms a mentsu.
    # But logically:
    # - If we have 0 pairs and 0 potential sequences, the best we can do is pick one tile and add 2 more to make a triplet or sequence. That takes 2 adds.
    # Is it possible to need more than 2? No, because we can always pick one tile and add 2 identical ones to make a koutsu, or add the two missing numbers to make a shuntsu.
    # So if not 0 and not 1, answer is 2.
    
    print(2)

if __name__ == "__main__":
    solve()