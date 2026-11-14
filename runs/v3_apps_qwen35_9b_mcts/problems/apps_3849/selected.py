import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    s = data[2]
    
    # Count number of 0s and 1s
    cnt0 = s.count('0')
    cnt1 = s.count('1')
    
    # Check if Tokitsukaze can win in the first move
    # She wins if she can make the whole string '0' or '1'
    # To make it all '0', the segment of '1's must be coverable by one interval of length k
    # To make it all '1', the segment of '0's must be coverable by one interval of length k
    
    # Helper to check if a segment of identical chars can be covered by one flip of length k
    def can_cover(target_char):
        if target_char == '0':
            # We need to cover all '1's
            if cnt1 == 0:
                return True
            # Find the range of '1's
            first = s.find('1')
            last = s.rfind('1')
            if last - first + 1 <= k:
                return True
            return False
        else:
            # We need to cover all '0's
            if cnt0 == 0:
                return True
            first = s.find('0')
            last = s.rfind('0')
            if last - first + 1 <= k:
                return True
            return False
    
    if can_cover('0') or can_cover('1'):
        print("tokitsukaze")
        return
    
    # If Tokitsukaze cannot win in move 1, then Quailty can always restore the board
    # to its initial state after Tokitsukaze's move, leading to a draw.
    # Why? Because if Tokitsukaze flips a range [i, i+k-1] to make it all 0s or all 1s,
    # the board changes. But since she couldn't win, the board is not uniform.
    # Quailty can simply flip the same range [i, i+k-1] back to the original values.
    # Since the original state was not a winning state for Quailty (otherwise she would have won on move 1? 
    # Wait, the condition for Quailty winning on move 1 is if the initial state allows her to make it uniform.
    # But the problem says Tokitsukaze moves first.
    # If the initial state is already uniform, Tokitsukaze has already won? No, the game starts, then they take turns.
    # "If all the color sides ... face the same direction after one's move, the one who takes this move will win."
    # So if the initial string is already all 0s or all 1s, Tokitsukaze doesn't need to move? 
    # Actually, the problem implies the game starts with a non-uniform state usually, but let's check constraints.
    # If initial is uniform, Tokitsukaze cannot make a move to win because the condition is checked AFTER her move.
    # But if it's already uniform, does the game end before she moves? The problem says "after one's move".
    # So if initial is uniform, Tokitsukaze must make a move. She flips k cards. The board becomes non-uniform (unless k=n and she flips to same side, but she must flip to same side, so if she flips to 0, it stays 0? 
    # "flip them to the same side, which means to make their color sides all face up or all face down."
    # If the board is all 0s, and she flips a segment to 0s, the board remains all 0s. Then she wins immediately?
    # Yes. If the board is already uniform, Tokitsukaze can choose any k consecutive cards and set them to 0 (or 1). 
    # If she sets them to 0, the whole board is still 0. So she wins.
    # Therefore, if cnt0 == 0 or cnt1 == 0, Tokitsukaze wins immediately.
    
    if cnt0 == 0 or cnt1 == 0:
        print("tokitsukaze")
        return

    # If Tokitsukaze cannot win in move 1, then Quailty can always revert the board to the initial state.
    # Thus, the game will never end, resulting in a draw.
    print("once again")

if __name__ == "__main__":
    solve()