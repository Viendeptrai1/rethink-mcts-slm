import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    n = int(input_data[0])
    s = input_data[1]
    
    # Convert string to list of characters for easier manipulation
    # We simulate the game where Slavko plays optimally
    # Mirko always picks the rightmost available letter
    # Slavko wants to maximize his word lexicographically (make it as small as possible)
    
    # We'll maintain two pointers: left and right
    # Initially, the sequence is s[0...n-1]
    # Turn 1 (Mirko): takes rightmost -> index n-1
    # Turn 2 (Slavko): takes rightmost from remaining -> index n-2
    # Turn 3 (Mirko): takes rightmost from remaining -> index n-3
    # ...
    # Pattern:
    # Mirko takes indices: n-1, n-3, n-5, ...
    # Slavko takes indices: n-2, n-4, n-6, ...
    
    # Since Mirko always takes the current rightmost, the set of indices Slavko gets
    # is fixed regardless of his choices? Wait, no.
    # The problem says: "Mirko ... always selecting the rightmost remaining letter"
    # But Slavko can choose ANY remaining letter.
    # However, Mirko's move depends on the current state.
    # If Slavko removes a letter in the middle, the "rightmost" for Mirko is still the original rightmost.
    # So the set of indices Mirko gets is always the ones at odd positions from the end (1st from end, 3rd from end, etc.)
    # And Slavko gets the even positions from the end (2nd from end, 4th from end, etc.)?
    # Let's trace:
    # Initial: 0 1 2 3 4 5 (n=6)
    # Mirko takes 5. Remaining: 0 1 2 3 4. Rightmost is 4.
    # Slavko can take any from 0..4.
    # If Slavko takes 4, then Mirko takes 3, Slavko takes 2, Mirko takes 1, Slavko takes 0.
    # If Slavko takes 0, then Mirko takes 4, Slavko takes 3, Mirko takes 2, Slavko takes 1.
    # So the set of indices Slavko gets is NOT fixed. He can choose which ones he gets.
    # But Mirko will always take the largest index currently available.
    # So if Slavko wants to get a specific set of indices, he must ensure that when it's his turn,
    # the indices he wants are still available, and the indices Mirko is forced to take are the large ones.
    # Actually, since Mirko always takes the largest available index, the indices Mirko takes are determined by the order of play
    # but Slavko can intercept the "good" ones.
    # Specifically, Slavko wants to pick the smallest possible characters for his word.
    # He can pick any character that is currently available.
    # But he must alternate.
    # Strategy for Slavko:
    # In his turns, he should greedily pick the smallest available character?
    # Not necessarily greedy in the moment, because picking a small character now might force him to take a large one later,
    # or it might be better to leave a small character for a later turn when he has a better option?
    # Actually, since he wants the lexicographically smallest word, he should try to put the smallest available characters as early as possible in his word.
    # However, the relative order of his picked characters in the final word is the order he picked them.
    # So he wants to pick the smallest available character at his first turn, then the smallest available at his second turn, etc.?
    # Is there any restriction? No, he can pick any available letter.
    # So the optimal strategy for Slavko is simply: at each of his turns, pick the smallest character currently available in the sequence.
    # Why? Because the final word is built by appending the picked letters in order of selection.
    # To make the resulting string lexicographically minimal, we want the first character to be as small as possible.
    # If there are multiple occurrences of the minimal character, does it matter which one we pick?
    # No, because they are identical.
    # So Slavko's strategy: always pick the minimum character currently in the pool.
    # But wait, we need to verify if this simple greedy works.
    # Example: s = "kava", n=4.
    # Indices: 0:k, 1:a, 2:v, 3:a
    # Turn 1 (Mirko): takes rightmost -> index 3 ('a'). Pool: {k, a, v}.
    # Turn 2 (Slavko): available {k, a, v}. Min is 'a'. He picks 'a'. Pool: {k, v}.
    # Turn 3 (Mirko): takes rightmost from original? No, "rightmost remaining".
    # The remaining sequence is effectively the subsequence of original indices {0, 1, 2}.
    # The rightmost remaining index is 2 ('v'). Mirko takes 'v'. Pool: {k}.
    # Turn 4 (Slavko): picks 'k'.
    # Slavko's word: "ak".
    # Mirko's word: "av".
    # "ak" < "av", so Slavko wins. Output: DA, ak. Matches sample 2.
    # Example 1: "ne", n=2.
    # Mirko takes 'e' (index 1). Pool {n}.
    # Slavko takes 'n'.
    # Words: Slavko "n", Mirko "e". "n" > "e", Slavko loses. Output NE, n. Matches sample 1.
    
    # So the algorithm is:
    # Simulate the game.
    # Maintain a data structure of available characters that supports:
    # 1. Find minimum character.
    # 2. Remove that character.
    # Also need to know which character Mirko takes.
    # Mirko always takes the character at the current largest index.
    # So we can just track the current largest index `r` starting at n-1.
    # Slavko takes the min from the available set.
    # But wait, removing a character changes the set, but does it change the "rightmost" index for Mirko?
    # "Rightmost remaining letter in the sequence".
    # If we have indices 0, 1, 2, 3. Mirko takes 3.
    # Remaining indices: 0, 1, 2. Rightmost is 2.
    # If Slavko takes index 1, remaining: 0, 2. Rightmost is still 2.
    # So yes, Mirko always takes the largest index that hasn't been taken yet.
    # Slavko takes the minimum character value among all indices that haven't been taken yet.
    
    # Implementation details:
    # We have N up to 100,000.
    # We need an efficient way to find and remove the minimum character.
    # Since characters are 'a'-'z', we can use a frequency array (bucket queue) or a heap.
    # Given the alphabet size is small (26), a frequency array is O(1) for finding min and O(1) amortized for removal.
    # However, we also need to know the specific index for Mirko? No, we just need the character.
    # But we need to know if that specific instance is still available.
    # Actually, since all 'a's are identical, we just need the count of 'a's.
    # But wait, Mirko takes a specific index. Does it matter which 'a' he takes?
    # No, because Slavko only cares about the counts.
    # BUT, there's a catch. Mirko takes the rightmost.
    # If there are multiple 'a's, and one is at index 0 and one at index 3.
    # Mirko might take index 3 ('a'). Then Slavko sees the remaining 'a' at index 0.
    # The counts approach works perfectly because the character value is all that matters for the min,
    # and the "rightmost" constraint only determines WHICH instance Mirko takes, but since instances of same char are identical,
    # the count of that char decreases by 1.
    # So Slavko's optimal strategy is simply: at each of his turns, pick the smallest char that has count > 0.
    # Mirko's move: decrement count of char at current `r`, then decrement `r`.
    # Slavko's move: find smallest char with count > 0, decrement its count, append to his word.
    
    # Let's double check if there's any scenario where picking the global minimum now is bad.
    # Suppose s = "baac". n=4.
    # r=3 ('c'). Mirko takes 'c'. Counts: b:1, a:2, c:0. r=2.
    # Slavko turn: min is 'a'. Takes 'a'. Counts: b:1, a:1. r=2 (unchanged for Mirko's next).
    # Mirko turn: r=2 ('a'). Takes 'a'. Counts: b:1, a:0. r=1.
    # Slavko turn: min is 'b'. Takes 'b'.
    # Slavko word: "ab".
    # Mirko word: "ca". "ab" < "ca". Win.
    # What if Slavko didn't pick 'a' first? Say he picked 'b' (worse). Then word starts with 'b', definitely worse.
    # Is there a case where picking the min now forces a bad later pick?
    # Since the set of available characters for Slavko in turn k is a subset of the initial characters minus what Mirko took,
    # and Mirko's moves are deterministic based on index, the only choice Slavko has is which character to take.
    # Taking the smallest available character at the earliest possible position in his word is always optimal for lexicographical comparison.
    # Because if word A < word B, then at the first differing position, A has a smaller char.
    # To maximize the chance of winning (or minimize the word), we want the first char to be min, then the second to be min, etc.
    # Any deviation from picking the current min would result in a larger char at the current position, making the word lexicographically larger immediately,
    # which cannot be compensated by smaller chars later.
    # So the greedy strategy is correct.
    
    # Algorithm:
    # 1. Count frequencies of each char in s.
    # 2. Initialize r = n - 1.
    # 3. Initialize slavo_word = [].
    # 4. Loop n/2 times (for Slavko's turns):
    #    a. Mirko's turn: 
    #       - Get char at s[r]. Decrement its count.
    #       - r -= 1.
    #    b. Slavko's turn:
    #       - Find smallest char with count > 0.
    #       - Append to slavo_word.
    #       - Decrement its count.
    # 5. Compare slavo_word and mirko_word?
    #    Wait, the problem says "The player who has the more beautiful word at the end of the game wins."
    #    More beautiful = comes first alphabetically.
    #    So we need to construct Mirko's word too to compare.
    #    Mirko's word is built by the order he picks.
    #    He picks indices n-1, n-3, n-5...
    #    So we can just store Mirko's picks in a list too.
    # 6. Compare the two strings. If slavo_word < mirko_word, output "DA", else "NE".
    #    Also output slavo_word.
    
    # Wait, constructing Mirko's word is straightforward: just read s[r] for r = n-1, n-3, ...
    
    # Complexity: O(N) because finding min in 26-sized array is O(1).
    
    from collections import Counter
    
    counts = [0] * 26
    for char in s:
        counts[ord(char) - ord('a')] += 1
        
    mirko_word = []
    slavo_word = []
    
    r = n - 1
    # Total turns = n. Slavko moves on turns 2, 4, ..., n. (n/2 moves)
    # Mirko moves on turns 1, 3, ..., n-1. (n/2 moves)
    
    for i in range(n):
        if i % 2 == 0:
            # Mirko's turn (0-indexed: 0, 2, 4...)
            # But problem says Mirko first.
            # Let's iterate total turns 1 to n.
            # Turn 1: Mirko. Turn 2: Slavko.
            pass
        
    # Let's re-loop clearly
    for turn in range(1, n + 1):
        if turn % 2 == 1:
            # Mirko's turn
            if r >= 0:
                char_m = s[r]
                idx = ord(char_m) - ord('a')
                counts[idx] -= 1
                mirko_word.append(char_m)
                r -= 1
        else:
            # Slavko's turn
            # Find min char with count > 0
            chosen = None
            for c_code in range(26):
                if counts[c_code] > 0:
                    chosen = chr(c_code + ord('a'))
                    counts[c_code] -= 1
                    break
            slavo_word.append(chosen)
            
    # Compare
    if slavo_word < mirko_word:
        print("DA")
    else:
        print("NE")
    print("".join(slavo_word))

if __name__ == '__main__':
    solve()