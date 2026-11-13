import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    a = []
    for i in range(n):
        a.append(int(input_data[1+i]))
    
    # We need to assign each element to either increasing (0) or decreasing (1)
    # such that the 0-sequence is strictly increasing and the 1-sequence is strictly decreasing.
    
    # Greedy strategy:
    # Maintain the last added value for the increasing sequence (inc_last) and decreasing sequence (dec_last).
    # Initialize them to -1 (since values are >= 0).
    # For each element x:
    #   If x > inc_last and x < dec_last: we can choose either, but we should pick the one that leaves more room for future elements.
    #     Actually, a better greedy approach:
    #     Try to put x into increasing if possible. If not, try decreasing. If neither, impossible.
    #     However, if both are possible, which one to pick?
    #     Consider future elements. If we put x in increasing, inc_last becomes x. If we put in decreasing, dec_last becomes x.
    #     To maximize chances for future elements:
    #       - We want inc_last to be as small as possible? No, we want it to be large to accept larger numbers? 
    #         Actually, strictly increasing means next must be > current. So smaller current is better for accepting more numbers.
    #         But we are forced to use x now. So if we assign to increasing, the next number must be > x.
    #         If we assign to decreasing, the next number must be < x.
    #       - Generally, if an element can go to both, we should put it in the sequence where it is "more extreme" relative to its constraints?
    #         Actually, standard solution for this problem:
    #         If x > inc_last AND x < dec_last:
    #             If x == inc_last + 1 is not required, just x > inc_last.
    #             Heuristic: If x is greater than inc_last, we can put it in increasing.
    #             If x is less than dec_last, we can put it in decreasing.
    #             If both are true:
    #                 We should put it in the sequence that is "tighter". 
    #                 Actually, if we put it in increasing, we raise the floor for the next increasing element.
    #                 If we put it in decreasing, we raise the ceiling for the next decreasing element (since decreasing sequence goes down, the next must be smaller, so a higher current is worse for decreasing? Wait.
    #                 Decreasing: y1 > y2 > ... . If current is x, next must be < x. So larger x makes it easier to find a smaller next element.
    #                 Increasing: x1 < x2 < ... . If current is x, next must be > x. So larger x makes it harder to find a larger next element.
    #                 Therefore, if we have a choice (x > inc_last and x < dec_last):
    #                     - Putting x in increasing makes inc_last = x (harder for future increasing).
    #                     - Putting x in decreasing makes dec_last = x (easier for future decreasing because next just needs to be < x, and x is large).
    #                 So if both are possible, we should prefer putting it in DECREASING (assign 1) because it keeps the increasing threshold lower (inc_last unchanged) and raises the decreasing ceiling (which is good for decreasing).
    #                 Wait, if we don't put it in decreasing, inc_last stays low. If we put it in decreasing, dec_last goes up.
    #                 Let's re-evaluate:
    #                 Option A (Assign 0): inc_new = x, dec remains dec_last.
    #                 Option B (Assign 1): inc remains inc_last, dec_new = x.
    #                 Future increasing needs > inc. If we choose A, future needs > x. If B, future needs > inc_last. Since inc_last <= x, B is better for increasing.
    #                 Future decreasing needs < dec. If we choose A, future needs < dec_last. If B, future needs < x. Since dec_last >= x, B is better for decreasing.
    #                 Conclusion: Option B (Assign 1) is strictly better or equal for both sequences if both are valid.
    #                 So priority: if x can go to decreasing, put it there. Else if x can go to increasing, put it there. Else NO.
    #                 Wait, is it possible that x can go to decreasing but NOT increasing? Yes if x <= inc_last.
    #                 Is it possible that x can go to increasing but NOT decreasing? Yes if x >= dec_last.
    #                 What if both are valid? Then pick decreasing (1).
    #                 What if only increasing is valid? Pick increasing (0).
    #                 What if only decreasing is valid? Pick decreasing (1).
    #                 What if neither? NO.
    
    inc_last = -1
    dec_last = 200001 # values are <= 200000
    res = []
    
    for x in a:
        can_inc = (x > inc_last)
        can_dec = (x < dec_last)
        
        if can_dec and can_inc:
            # Prefer decreasing as argued above
            res.append(1)
            dec_last = x
        elif can_dec:
            res.append(1)
            dec_last = x
        elif can_inc:
            res.append(0)
            inc_last = x
        else:
            print("NO")
            return
            
    print("YES")
    print(*(res))

if __name__ == "__main__":
    solve()