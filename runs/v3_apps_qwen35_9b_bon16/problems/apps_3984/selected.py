import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    s = input_data[0]
    n = len(s)
    first_char = s[0]
    min_char = first_char
    
    # Determine if the game starts with a move possible or not
    # If s[0] is already the smallest character in the string, then no player can choose a lexicographically smaller substring
    # because any substring starting at index > 0 will be >= s[0] + ... which is lexicographically >= s[0]... if s[0] is min.
    # Actually, the condition is: can we find l' <= l and r' >= r such that s[l':r'+1] < s[l:r+1]?
    # Initially l=r=k. So we need a substring containing index k that is lexicographically smaller than s[k:k+1].
    # This is possible if and only if there exists a character smaller than s[k] at some position p <= k?
    # No, the substring must contain k. So the new substring s[l':r'] must have l' <= k <= r'.
    # For s[l':r'] < s[k:k+1], since s[k:k+1] has length 1, and s[l':r'] has length >= 1.
    # If s[l':r'] has length > 1, it is compared char by char.
    # Key insight: The first character of the new substring s[l'] determines the comparison largely.
    # If s[l'] < s[k], then s[l':r'] < s[k:k+1] regardless of the rest (since s[k:k+1] starts with s[k]).
    # If s[l'] == s[k], then we look at the next characters.
    # However, note that the initial string is just a single character s[k].
    # Any substring s[l':r'] with l' <= k <= r' has s[l'] as its first character.
    # If there is any index l' <= k such that s[l'] < s[k], then Ann can choose l'=l', r'=k.
    # Then s[l':k] starts with s[l'] < s[k], so it is smaller. Ann wins immediately.
    # If there is no l' <= k with s[l'] < s[k], then for all l' <= k, s[l'] >= s[k].
    # In this case, can Ann make a move?
    # If s[l'] > s[k], then s[l':r'] > s[k:k+1] (since first char is bigger). No.
    # If s[l'] == s[k], then we compare s[l':r'] with s[k].
    # s[l':r'] = s[l'] + s[l'+1]... + s[r']. s[k] = s[k].
    # Since s[l'] == s[k], we compare the rest. But s[k] has no rest.
    # So s[l':r'] > s[k] because it is longer and prefix matches?
    # Lexicographical comparison: "a" < "aa". Yes.
    # So if s[l'] == s[k], then s[l':r'] > s[k] (since length > 1).
    # Thus, if there is no l' <= k with s[l'] < s[k], Ann cannot make the first move.
    # Therefore, the winner is determined solely by whether there exists a character smaller than s[k] in s[0...k].
    
    # Let's verify with examples.
    # s = "abba", k=0 ('a'). Range [0,0]. Is there l'<=0 with s[l'] < 'a'? No. Ann loses -> Mike.
    # s = "abba", k=1 ('b'). Range [1,1]. Is there l'<=1 with s[l'] < 'b'? Yes, s[0]='a'. Ann chooses l'=0, r'=1 ("ab").
    # "ab" < "b"? Yes. Ann moves to [0,1]. Now state is l=0, r=1.
    # Next player (Mike) needs l''<=0, r''>=1 such that s[l'':r''] < "ab".
    # l'' must be 0. r'' >= 1.
    # Substrings starting at 0 with length >= 2: "ab", "abb", "abba".
    # "ab" is current. "abb" > "ab". "abba" > "ab".
    # So Mike cannot move. Mike loses -> Ann wins.
    # Output for k=1 is Ann. Correct.
    
    # s = "abba", k=2 ('b'). Range [2,2]. Is there l'<=2 with s[l'] < 'b'? Yes, s[0]='a', s[1]='b' (not <), s[2]='b'.
    # Smallest is 'a' at 0. Ann chooses l'=0, r'=2 ("abb").
    # "abb" < "b"? Yes. State becomes [0,2].
    # Mike needs l''<=0, r''>=2. Only l''=0. r'' >= 2.
    # Substrings: "abb", "abba". Both >= "abb". Mike loses -> Ann wins.
    # Output for k=2 is Ann. Correct.
    
    # s = "abba", k=3 ('a'). Range [3,3]. Is there l'<=3 with s[l'] < 'a'? No.
    # Ann loses -> Mike wins.
    # Output for k=3 is Mike. Correct.
    
    # s = "cba", k=0 ('c'). l'<=0? No smaller. Mike.
    # k=1 ('b'). l'<=1? s[0]='c' > 'b'. No smaller. Mike.
    # k=2 ('a'). l'<=2? s[0]='c', s[1]='b', s[2]='a'. No smaller than 'a'. Mike.
    # Output: Mike, Mike, Mike. Correct.
    
    # So the logic holds:
    # If there exists any character in s[0...k] strictly less than s[k], then Ann wins.
    # Otherwise, Mike wins.
    
    # We need to output for all k from 0 to n-1.
    # We can maintain the minimum character seen so far in the prefix.
    
    min_so_far = s[0]
    results = []
    
    for k in range(n):
        # Check if min_so_far < s[k]
        # Note: min_so_far is the minimum in s[0...k-1] before update?
        # Wait, the range is 0 to k inclusive for the check?
        # The condition is: exists l' <= k such that s[l'] < s[k].
        # So we need to check s[0]...s[k].
        # But min_so_far currently holds min(s[0]...s[k-1]) if we update after check.
        # Let's adjust.
        
        if min_so_far < s[k]:
            results.append("Ann")
        else:
            results.append("Mike")
        
        # Update min_so_far to include s[k] for the next iteration
        if s[k] < min_so_far:
            min_so_far = s[k]
            
    print('\n'.join(results))

if __name__ == "__main__":
    solve()