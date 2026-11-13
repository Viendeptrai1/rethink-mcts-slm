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

    # Check if we already have a mentsu (koutsu or shuntsu)
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

    # Check if we can form a mentsu by drawing 1 tile
    # We need to find if there exists a tile t such that hand + [t] contains a mentsu.
    # This happens if:
    # 1. Two identical tiles exist, and we draw the third (koutsu)
    # 2. Two tiles form a sequence with a gap of 1 (e.g., 1,3 -> draw 2) or gap of 2 (e.g., 1,2 -> draw 3) in same suit (shuntsu)
    
    def can_form_with_one(h):
        from collections import Counter
        counts = Counter(h)
        
        # Case 1: Koutsu
        for k, v in counts.items():
            if v >= 2:
                return True
        
        # Case 2: Shuntsu
        # Group by suit
        suits = {}
        for n, s in h:
            if s not in suits:
                suits[s] = []
            suits[s].append(n)
        
        for s in suits:
            nums = sorted(suits[s])
            # Check pairs that can form a sequence with one more tile
            # Pairs: (x, x+1) -> need x+2; (x, x+2) -> need x+1
            for i in range(len(nums) - 1):
                a, b = nums[i], nums[i+1]
                if b == a + 1:
                    # Need a+2 or a-1? Actually if we have a, a+1, we can complete with a+2 or a-1 (if valid)
                    # But we only need existence of one valid completion
                    if a + 2 <= 9:
                        return True
                    if a - 1 >= 1:
                        return True
                elif b == a + 2:
                    # Need a+1
                    if 1 <= a+1 <= 9:
                        return True
        return False

    if can_form_with_one(hand):
        print(1)
        return

    # Check if we can form a mentsu by drawing 2 tiles
    # We need to find if there exists a tile t1, t2 such that hand + [t1, t2] contains a mentsu.
    # This happens if:
    # 1. One identical tile exists, and we draw two more (koutsu)
    # 2. One tile exists, and we draw two others to form a sequence (shuntsu)
    # Note: If we have 0 matching tiles for any potential mentsu, we might still form one with 2 draws?
    # Actually, with 3 tiles initially, if we draw 2, we have 5 tiles. We just need one mentsu subset of 3.
    # Possibilities:
    # - Koutsu: Need 3 same. If we have 1, draw 2. If we have 0, draw 3 (not possible with 2 draws). So if count >= 1, possible with 2 draws.
    # - Shuntsu: Need 3 sequential. 
    #   - If we have 3 tiles in same suit that can form a sequence with 2 draws? 
    #     Actually, if we have 1 tile, we can draw 2 to make a sequence (e.g., have 5, draw 4,6 -> 4,5,6).
    #     If we have 2 tiles in same suit, can we always complete with 1 draw? Yes, checked above.
    #     So if we have 1 tile in a suit, we can complete with 2 draws.
    #     What if we have 0 tiles in a suit? Then we need 3 draws.
    
    # So logic:
    # If we have at least one pair (count >= 2) -> 1 draw (checked)
    # If we have at least one triplet (count >= 3) -> 0 draws (checked)
    # If we have at least one pair in same suit that is 1 apart or 2 apart -> 1 draw (checked)
    # If we have at least one single tile in some suit -> we can complete a shuntsu with 2 draws? 
    #   Yes: e.g., have 5s. Draw 4s, 6s -> 4,5,6. Or 3s,4s -> 3,4,5.
    #   So if there is any suit with at least 1 tile, we can form a shuntsu with 2 draws.
    #   Is it possible to have 0 tiles in all suits? No, we start with 3 tiles.
    #   Therefore, if we don't have 0 or 1 draw solution, the answer is 2.
    
    # Wait, is there any case where we need 2 draws but we have 0 tiles in a suit? 
    # No, because we have 3 tiles total, so at least one suit has tiles.
    # If we have 1 tile in a suit, we can always complete a sequence with 2 draws.
    # If we have 2 tiles in a suit, we can complete with 1 draw (if they are close enough) or 2 draws (if not close enough? e.g., 1 and 9).
    #   If we have 1m and 9m, can we form a sequence with 2 draws? 
    #   We can form 1,2,3 (draw 2,3) or 7,8,9 (draw 7,8). Yes.
    #   So if we have 2 tiles in same suit, even if far apart, we can form a sequence with 2 draws.
    #   But we already checked if 1 draw is sufficient. If not, then 2 is sufficient.
    # If we have 1 tile in a suit, we can form a sequence with 2 draws.
    # If we have 0 tiles in a suit? Impossible since we have 3 tiles.
    
    # What about koutsu?
    # If we have 1 tile of type X, we need 2 more to make a koutsu. So 2 draws.
    # If we have 0 tiles of type X, we need 3 draws.
    
    # So the only case for 2 draws is:
    # - We have at least one tile (which we always do) -> can form shuntsu with 2 draws.
    # - OR we have at least one tile of a specific type -> can form koutsu with 2 draws.
    # Since we have 3 tiles, we definitely have at least one tile, so answer is at most 2.
    # And we already checked 0 and 1.
    
    print(2)

if __name__ == "__main__":
    solve()