import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    a = [int(x) for x in input_data[1:]]
    
    # We can simulate the process efficiently by observing the pattern:
    # Instead of actually reversing a list (which is O(n) per operation leading to O(n^2)),
    # we can use a deque and decide whether to append to the left or right.
    # 
    # Let's trace the position of elements:
    # Operation 1: append a[0], reverse -> [a[0]]
    # Operation 2: append a[1] to end, reverse -> [a[1], a[0]]
    # Operation 3: append a[2] to end, reverse -> [a[2], a[0], a[1]]
    # Operation 4: append a[3] to end, reverse -> [a[3], a[1], a[0], a[2]]
    #
    # Pattern for even n (e.g., n=4):
    # Result: a[3], a[1], a[0], a[2]
    # Indices: 3, 1, 0, 2
    #
    # Pattern for odd n (e.g., n=3):
    # Op 1: [a0]
    # Op 2: [a1, a0]
    # Op 3: [a1, a0, a2] -> reverse -> [a2, a0, a1]
    # Result: a[2], a[0], a[1]
    # Indices: 2, 0, 1
    #
    # General construction using a deque:
    # We maintain a deque representing the current state of b.
    # However, since we always reverse at the end of each step, we can avoid actual reversal.
    # 
    # Let's think about the direction.
    # Initially, the "front" of our logical list is the left side.
    # Step 1: Append a[0]. List: [a0]. Reverse. List: [a0].
    # Step 2: Append a[1] to the "end". But the list is reversed. 
    # If we consider the list as having a "current end" pointer:
    # Initially, we are building the list.
    # After step 1, the list is [a0]. The "end" is the right side.
    # Step 2: We append a[1] to the end -> [a0, a1]. Then reverse -> [a1, a0].
    # Now the "end" is the left side.
    # Step 3: We append a[2] to the end (which is now the left) -> [a2, a1, a0]. Then reverse -> [a0, a1, a2].
    # Wait, the sample says:
    # Step 3: b was [2, 1]. Append 3 -> [2, 1, 3]. Reverse -> [3, 1, 2].
    # My manual trace above for n=3 with a=[1,2,3]:
    # Start: []
    # i=1 (val=1): append 1 -> [1], reverse -> [1]
    # i=2 (val=2): append 2 -> [1, 2], reverse -> [2, 1]
    # i=3 (val=3): append 3 -> [2, 1, 3], reverse -> [3, 1, 2]
    #
    # Let's re-evaluate the "append to end then reverse" logic with a deque.
    # Instead of physically reversing, we can toggle the side we append to.
    # Let `is_reversed` be a boolean indicating if the current logical list is reversed relative to our deque storage.
    # Actually, simpler approach:
    # Maintain a deque `d`.
    # Maintain a boolean `rev` which is False initially.
    # For each element x in a:
    #   If `rev` is False:
    #     Append x to the right of d.
    #     Then logically reverse the whole list. Instead of doing it, we set `rev = True`.
    #     But wait, the operation is: Append to end, THEN reverse.
    #     If we are in state `rev=False` (meaning d represents the list normally):
    #       Append x to right: d = [..., x]
    #       Reverse: d becomes [x, ..., old_first]
    #       Now the list is reversed. So next time, "end" means left side of d.
    #   If `rev` is True:
    #     The list is currently reversed. The "end" of the list corresponds to the LEFT of d.
    #     Append x to the "end" -> Append x to the LEFT of d.
    #     d = [x, ...]
    #     Then reverse the list. Reversing a reversed list makes it normal.
    #     So set `rev = False`.
    #
    # Let's trace with a = [1, 2, 3, 4]
    # d = deque(), rev = False
    # i=1, x=1: rev=False -> append right -> d=[1], rev=True
    # i=2, x=2: rev=True -> append left -> d=[2, 1], rev=False
    # i=3, x=3: rev=False -> append right -> d=[2, 1, 3], rev=True
    # i=4, x=4: rev=True -> append left -> d=[4, 2, 1, 3], rev=False
    # Final d: [4, 2, 1, 3]. Matches sample output.
    #
    # Trace with a = [1, 2, 3]
    # d = deque(), rev = False
    # i=1, x=1: rev=False -> append right -> d=[1], rev=True
    # i=2, x=2: rev=True -> append left -> d=[2, 1], rev=False
    # i=3, x=3: rev=False -> append right -> d=[2, 1, 3], rev=True
    # Final d: [2, 1, 3].
    # Let's verify manually:
    # Start []
    # 1: [1] -> rev -> [1]
    # 2: [1, 2] -> rev -> [2, 1]
    # 3: [2, 1, 3] -> rev -> [3, 1, 2]
    # My deque result [2, 1, 3] is NOT [3, 1, 2].
    # Where is the error?
    #
    # Re-trace logic:
    # State: (deque content, is_list_reversed)
    # Initially: d=[], rev=False. List is [].
    # Op 1 (x=1):
    #   List is not reversed. End is right.
    #   Append 1 to right: d=[1].
    #   Reverse list: List becomes [1]. d should represent [1] but with rev=True?
    #   If rev=True, d=[1] means list is [1] (since reversing [1] is [1]).
    #   So after op 1: d=[1], rev=True.
    # Op 2 (x=2):
    #   List is reversed (rev=True). End is left.
    #   Append 2 to left: d=[2, 1].
    #   Reverse list: List becomes [1, 2].
    #   If rev=False, d=[2, 1] means list is [1, 2] (reverse of [2, 1]).
    #   So after op 2: d=[2, 1], rev=False.
    # Op 3 (x=3):
    #   List is not reversed (rev=False). End is right.
    #   Append 3 to right: d=[2, 1, 3].
    #   Reverse list: List becomes [3, 1, 2].
    #   If rev=True, d=[2, 1, 3] means list is [3, 1, 2] (reverse of [2, 1, 3]).
    #   So after op 3: d=[2, 1, 3], rev=True.
    #
    # Final result should be the list represented by (d, rev).
    # If rev is False, result is d.
    # If rev is True, result is reversed(d).
    #
    # For n=3, a=[1,2,3]:
    # Final state: d=[2, 1, 3], rev=True.
    # Result = reverse([2, 1, 3]) = [3, 1, 2]. Correct.
    #
    # For n=4, a=[1,2,3,4]:
    # Op 4 (x=4):
    #   Current: d=[2, 1, 3], rev=True.
    #   List is reversed. End is left.
    #   Append 4 to left: d=[4, 2, 1, 3].
    #   Reverse list: List becomes [3, 1, 2, 4].
    #   If rev=False, d=[4, 2, 1, 3] means list is [3, 1, 2, 4] (reverse of [4, 2, 1, 3]).
    #   So after op 4: d=[4, 2, 1, 3], rev=False.
    # Final result: d = [4, 2, 1, 3]. Correct.
    #
    # Algorithm:
    # 1. Initialize deque d.
    # 2. Initialize rev = False.
    # 3. For x in a:
    #      if not rev:
    #          d.append(x)
    #      else:
    #          d.appendleft(x)
    #      rev = not rev
    # 4. If rev is True, output reversed(d). Else output d.
    
    from collections import deque
    d = deque()
    rev = False
    
    for x in a:
        if not rev:
            d.append(x)
        else:
            d.appendleft(x)
        rev = not rev
    
    if rev:
        # If rev is True, the actual list is the reverse of d
        result = list(reversed(d))
    else:
        result = list(d)
    
    print(*(result))

if __name__ == '__main__':
    solve()