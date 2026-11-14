import sys

def solve():
    s = sys.stdin.readline().strip()
    n = len(s)
    
    # We need to determine for each k if Ann wins.
    # Ann wins if there exists an index i <= k such that s[i] < s[k].
    # If no such i exists, then for all i <= k, s[i] >= s[k].
    # In that case, any move (l', r') with l' <= k <= r' results in a substring
    # starting with a character >= s[k].
    # - If s[l'] > s[k], the new substring is lexicographically larger.
    # - If s[l'] == s[k], the new substring starts with the same char. Since the current
    #   substring is s[k...k] (length 1), the new substring s[l'...r'] has length >= 2.
    #   A string of length 1 is always lexicographically smaller than a longer string
    #   starting with the same character (e.g., "a" < "aa").
    # Therefore, if no s[i] < s[k] for i <= k, Ann has no valid moves and loses immediately.
    # If there is at least one s[i] < s[k] for i <= k, Ann can choose l'=i, r'=k (or just l'=i, r'=i)
    # to make a valid move. The problem asks for the winner assuming optimal play.
    # However, the condition "lexicographically less" is the only constraint.
    # If a move exists, Ann makes it. Does she always win?
    # Actually, the game is finite and impartial. But the key insight from the examples and logic
    # is that if a move exists, Ann can move to a state where the condition "no smaller char to left"
    # might hold for the new k? Not necessarily.
    # Let's re-evaluate based on the examples.
    # Example 1: abba
    # k=0 ('a'): min('a') = 'a'. No char < 'a'. Mike wins.
    # k=1 ('b'): min('a','b') = 'a' < 'b'. Ann wins.
    # k=2 ('b'): min('a','b','b') = 'a' < 'b'. Ann wins.
    # k=3 ('a'): min('a','b','b','a') = 'a'. No char < 'a'. Mike wins.
    # Example 2: cba
    # k=0 ('c'): min('c') = 'c'. No char < 'c'. Mike.
    # k=1 ('b'): min('c','b') = 'b'. No char < 'b' (since 'c' > 'b'). Mike.
    # k=2 ('a'): min('c','b','a') = 'a'. No char < 'a'. Mike.
    
    # The pattern is strictly: Ann wins if min(s[0...k]) < s[k], else Mike wins.
    # Why? Because if min(s[0...k]) < s[k], let i be an index where s[i] is that minimum.
    # Ann can choose l'=i, r'=k. The new substring is s[i...k].
    # Since s[i] < s[k], s[i...k] < s[k...k] lexicographically.
    # The new state has left border i and right border k.
    # The game continues. But wait, if Ann can make a move, does she guarantee a win?
    # Consider the state where l=r=k. If there is ANY move, Ann makes it.
    # The game ends when no moves are possible.
    # The condition "no moves possible" from state (l, r) means for all l' <= l, r' >= r,
    # s[l'...r'] >= s[l...r].
    # Specifically, if we are at (k, k), no moves possible iff for all i <= k, s[i...k] >= s[k...k].
    # s[i...k] >= s[k...k] is true if s[i] > s[k] OR (s[i] == s[k] and len(s[i...k]) > 1).
    # Since len(s[i...k]) >= 1, if s[i] == s[k], then len > 1 implies s[i...k] > s[k...k].
    # So the only way s[i...k] < s[k...k] is if s[i] < s[k].
    # Thus, from state (k, k), a move exists IFF there exists i <= k such that s[i] < s[k].
    # If a move exists, Ann makes it. The new state is (l', r').
    # Is it possible that after Ann's move, Mike has a winning strategy?
    # The problem statement implies a simple condition based on the examples.
    # Let's assume the hypothesis: Ann wins iff exists i <= k with s[i] < s[k].
    # If this hypothesis holds, the logic is:
    # 1. If no such i exists, Ann has 0 moves -> Ann loses -> Mike wins.
    # 2. If such i exists, Ann has >= 1 move. Can Mike win?
    #    If Ann moves to (l', r'), the new "k" for the next turn is effectively l' (since the new
    #    substring starts at l' and ends at r', and the next player must expand further or stay).
    #    Actually, the game state is defined by (l, r). The next player must choose (l'', r'')
    #    such that l'' <= l, r'' >= r and s[l''...r''] < s[l...r].
    #    This looks like a game on a DAG.
    #    However, notice that if we are in a state where min(s[0...l]) < s[l], then a move exists.
    #    But the crucial observation from competitive programming problems of this type (Codeforces 1141C? No, this is likely a specific problem)
    #    is often that the game length is 1 or the condition is static.
    #    Let's re-read carefully: "The player, that can't make a move loses."
    #    If Ann can make a move, she moves to some (l', r'). Then it's Mike's turn.
    #    Mike needs to find (l'', r'') <= (l', r') such that s[l''...r''] < s[l'...r'].
    #    If the condition "exists i <= current_l such that s[i] < s[current_l]" is the ONLY condition for a move to exist from (l, l),
    #    what about (l, r) where l < r?
    #    Suppose current state is (l, r). A move exists if there is (l', r') with l' <= l, r' >= r and s[l'...r'] < s[l...r].
    #    If s[l] < s[l'], then s[l'...r'] > s[l...r] (since first char is larger).
    #    If s[l] == s[l'], then we compare subsequent chars.
    #    If s[l] > s[l'], then s[l'...r'] < s[l...r] regardless of the rest.
    #    So if there exists l' <= l such that s[l'] < s[l], then Ann can choose l'=l', r'=r (or r' larger) and win the move.
    #    What if s[l] is the minimum in s[0...l]? Then for all l' <= l, s[l'] >= s[l].
    #    If s[l'] > s[l], then s[l'...r'] > s[l...r].
    #    If s[l'] == s[l], then s[l'...r'] starts with same char. Since l' <= l, the length of s[l'...r'] is (r' - l' + 1) >= (r - l + 1).
    #    If lengths are equal (l'=l, r'=r), it's the same string.
    #    If length is greater, s[l'...r'] > s[l...r] (e.g., "a" < "aa").
    #    So if s[l] is the minimum in s[0...l], then NO move is possible from (l, r) for ANY r >= l.
    #    Proof: For any valid move (l', r'), we need s[l'...r'] < s[l...r].
    #    Since l' <= l, s[l'] >= s[l].
    #    Case 1: s[l'] > s[l]. Then s[l'...r'] > s[l...r]. Invalid.
    #    Case 2: s[l'] == s[l]. Then s[l'...r'] and s[l...r] start with same char.
    #       Compare index l'+1 vs l+1.
    #       Actually, simpler: s[l'...r'] has length >= s[l...r].
    #       If s[l'...r'] < s[l...r], then at the first differing position, s[l'...r'] must have smaller char.
    #       But since s[l'] == s[l], the first char is same.
    #       If l' < l, then s[l'...r'] has prefix s[l'...l-1] + s[l]...
    #       s[l...r] is just s[l]...
    #       This comparison is tricky.
    #       Example: s = "ba", state (1, 1) -> "a". l=1, r=1. s[1]='a'. min(s[0..1]) = 'a'. No smaller.
    #       Can we move? l' <= 1, r' >= 1.
    #       Try l'=0, r'=1 -> "ba". "ba" < "a"? No. 'b' > 'a'.
    #       Try l'=0, r'=0 -> "b". "b" < "a"? No.
    #       So no moves.
    #       Example: s = "ab", state (1, 1) -> "b". l=1, r=1. s[1]='b'. min(s[0..1]) = 'a' < 'b'.
    #       Move l'=0, r'=1 -> "ab". "ab" < "b"? Yes ('a' < 'b'). Valid move.
    #       Move l'=0, r'=0 -> "a". "a" < "b"? Yes. Valid move.
    #       So if min(s[0...l]) < s[l], moves exist.
    #       If min(s[0...l]) == s[l], then for all l' <= l, s[l'] >= s[l].
    #       If s[l'] > s[l], s[l'...r'] > s[l...r].
    #       If s[l'] == s[l], then s[l'...r'] starts with s[l].
    #       Is it possible that s[l'...r'] < s[l...r]?
    #       s[l'...r'] = s[l'] + ... = s[l] + ...
    #       s[l...r] = s[l] + ...
    #       If l' < l, s[l'...r'] has more characters before s[l] than s[l...r] (which has 0 chars before s[l]).
    #       Wait, s[l...r] starts at l. s[l'...r'] starts at l'.
    #       If l' < l, s[l'...r'] = s[l'] s[l'+1] ... s[l] ...
    #       s[l...r] = s[l] ...
    #       Compare s[l'] and s[l]. They are equal.
    #       Compare s[l'+1] and s[l].
    #       This depends on the string content.
    #       However, consider the case where s[l] is the minimum.
    #       If there is a move, Ann makes it.
    #       The key realization from similar problems (e.g., Codeforces 1140C? No, this is likely "Mike and Ann" from a contest) is that the game is determined solely by the existence of a smaller character to the left.
    #       Why? Because if a smaller character exists, Ann can move to a state (l', r') where l' is the index of that smaller character.
    #       In the new state, the left border is l'. The right border is r' >= r.
    #       Now it's Mike's turn. He needs to find (l'', r'') <= (l', r') such that s[l''...r''] < s[l'...r'].
    #       But s[l'] is the minimum in s[0...l] (by choice of l').
    #       Is s[l'] the minimum in s[0...l']? Yes, because l' <= l and s[l'] < s[l] and s[l] was min in s[0...l]?
    #       Not necessarily. s[l] was min in s[0...l]. If s[l'] < s[l], then s[l'] is even smaller.
    #       So s[l'] is the minimum in s[0...l'].
    #       Therefore, from state (l', r'), there are NO moves possible for Mike!
    #       Because for any l'' <= l', s[l''] >= s[l'] (since s[l'] is min in s[0...l']).
    #       If s[l''] > s[l'], then s[l''...r''] > s[l'...r'].
    #       If s[l''] == s[l'], then s[l''...r''] starts with s[l'].
    #       Similar logic: if l'' < l', s[l''...r''] has prefix before s[l']?
    #       Actually, if s[l'] is the minimum in s[0...l'], then for any l'' <= l', s[l''] >= s[l'].
    #       If s[l''] > s[l'], then s[l''...r''] > s[l'...r'].
    #       If s[l''] == s[l'], then s[l''...r'] starts with s[l'].
    #       Can s[l''...r''] < s[l'...r'']?
    #       s[l'...r''] starts with s[l']. s[l''...r''] starts with s[l''].
    #       If l'' < l', then s[l''...r''] = s[l''] ... s[l'] ...
    #       s[l'...r''] = s[l'] ...
    #       Since s[l''] == s[l'], we look at next char.
    #       But generally, if s[l'] is the minimum, it's very hard to find a smaller substring.
    #       Specifically, if s[l'] is the minimum in s[0...l'], then for any l'' <= l', s[l''] >= s[l'].
    #       If s[l''] > s[l'], impossible to be smaller.
    #       If s[l''] == s[l'], then s[l''...r''] has length >= s[l'...r''].
    #       If lengths are equal, strings are equal.
    #       If length of s[l''...r''] > length of s[l'...r''], then s[l''...r''] > s[l'...r''] (since prefix matches).
    #       So if s[l'] is the minimum in s[0...l'], then NO moves are possible from (l', r').
    #       Therefore, if Ann can move to a state where the new left border l' has s[l'] = min(s[0...l']), then Mike loses immediately.
    #       Can Ann always do this?
    #       If there exists i <= k such that s[i] < s[k], let i be the index of the minimum character in s[0...k].
    #       Then s[i] = min(s[0...k]).
    #       Ann can choose l' = i, r' = k.
    #       The new state is (i, k).
    #       Now, is s[i] the minimum in s[0...i]? Yes, because i <= k and s[i] is min in s[0...k], so it is definitely min in s[0...i].
    #       Therefore, from state (i, k), Mike has no moves.
    #       So Ann wins.
    #       Conclusion: Ann wins if and only if there exists i <= k such that s[i] < s[k].
    #       Otherwise, Mike wins.

    # Algorithm:
    # Iterate k from 0 to n-1.
    # Maintain the minimum character seen so far in s[0...k].
    # If min_char < s[k], Ann wins.
    # Else, Mike wins.

    min_char = s[0]
    results = []
    
    for k in range(n):
        if s[k] < min_char:
            min_char = s[k]
        
        # Check condition: exists i <= k such that s[i] < s[k]
        # This is equivalent to: min(s[0...k]) < s[k]
        # Note: min_char is min(s[0...k])
        if min_char < s[k]:
            results.append("Ann")
        else:
            results.append("Mike")
            
    print('\n'.join(results))

if __name__ == '__main__':
    solve()