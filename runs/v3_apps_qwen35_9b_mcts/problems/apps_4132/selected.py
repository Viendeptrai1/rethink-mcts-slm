import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    a = []
    for i in range(n):
        a.append(int(input_data[i+1]))
    
    a.sort()
    
    # We simulate the process where the smallest alive monster attacks the largest alive monster.
    # However, since N can be up to 10^5 and values up to 10^9, a direct simulation of every attack
    # might be too slow if the number of attacks is huge. But note:
    # In the optimal strategy to minimize the final health, we want the smallest number to keep reducing the largest.
    # Actually, the known solution for this problem (AtCoder ABC 178 F? No, this is ABC 178 E? Actually it's ABC 178 Problem F is different.
    # This problem is actually from AtCoder Beginner Contest 178, Problem F is not it. 
    # Wait, this is ABC 178 Problem ... actually it's ABC 178 Problem D? No.
    # Let me recall: This is ABC 178 Problem F? No.
    # Actually, this is a known problem: "Monster Battle" or similar.
    # The correct logic: To minimize the final health, we should always have the smallest monster attack the largest.
    # But note: the problem says "random", but we are to find the MINIMUM possible. So we choose the best sequence.
    # The best strategy is: repeatedly take the smallest available monster and use it to attack the largest available monster.
    # However, if the smallest monster's health is less than the largest, the largest becomes (largest - smallest).
    # If the smallest monster's health is greater than or equal to the largest, then the largest becomes 0 (dies) and the smallest remains.
    # But wait: if the smallest attacks the largest and the largest dies, then the smallest is still alive and we continue.
    # However, the problem states: "Until there is only one alive monster".
    # So we simulate:
    #   While there is more than one alive monster:
    #       Pick the smallest alive monster (say x) and the largest alive monster (say y).
    #       y = y - x
    #       If y becomes 0, it dies.
    #       But note: we want to minimize the final health. The final health will be the health of the last survivor.
    #       However, if we let the smallest attack the largest repeatedly, the largest might become small, but then we have to consider that the smallest might die?
    #       Actually, the smallest monster will never die if it is attacking, because it only reduces the other's health.
    #       But if the smallest monster is attacked, it might die. However, in our strategy, we are choosing who attacks whom.
    #       To minimize the final health, we want the last survivor to have as little health as possible.
    #       The known solution for this problem is:
    #         Sort the array. Then, the answer is the result of repeatedly doing:
    #           a[0] = a[0] % a[1]   ??? Not exactly.
    #       Actually, let's think:
    #         We have a set of numbers. We can choose any two: (x, y) and replace y with y-x (if y-x>0) or remove y (if y-x<=0).
    #         We want the last remaining number to be minimized.
    #         This is equivalent to: we can subtract any number from any other number as long as the subtrahend is positive.
    #         The minimal possible value is the GCD of all numbers? No, because we can only subtract the current health of the attacker.
    #         But note: the attacker's health does not change when it attacks. Only the victim's health changes.
    #         So if we have [2, 10, 8, 40]:
    #           Option: 2 attacks 40 -> 40 becomes 38. Then 2 attacks 38 -> 36, ... until 40 becomes 0? But 40 becomes 0 only after 20 attacks.
    #           However, we can also have 2 attack 10 -> 8, then 2 attacks 8 -> 6, ... until 8 becomes 0? 
    #         Actually, the optimal strategy is to use the smallest number to reduce the largest number until the largest number becomes less than the smallest, then swap roles?
    #         But note: the problem is known and the solution is:
    #           Sort the array. Then, the answer is the last element after simulating:
    #             while len(a) > 1:
    #                 a[0] = a[0] % a[1]   ??? No, because if a[0] >= a[1], then a[1] becomes 0 and we remove it, and then we have a[0] and the rest.
    #         Actually, the correct simulation is:
    #           We always let the smallest element attack the largest element.
    #           But if the smallest element is very small, it will take many attacks to reduce the largest. However, we can do modulo?
    #           But note: the problem does not require us to simulate every single attack. We can use modulo for efficiency.
    #           However, the catch: when the largest element becomes less than the smallest, then the smallest is no longer the smallest? 
    #           Actually, after reducing the largest by the smallest multiple times, the largest becomes (largest % smallest). 
    #           But if the largest % smallest is 0, then the largest dies and we are left with the smallest and the rest.
    #           Then the smallest becomes the new smallest (it remains) and we continue with the next largest.
    #           However, if the largest % smallest is not 0, then the new value is (largest % smallest) and we insert it back into the sorted list?
    #           But note: the problem says "random", but we are to find the minimum possible. So we choose the best moves.
    #           The best moves: always use the smallest to attack the largest. And if the largest becomes less than the smallest, then we have a new set of numbers.
    #           Actually, the process is:
    #             Sort the array: a[0] <= a[1] <= ... <= a[n-1]
    #             We take a[0] and a[n-1]. 
    #             If a[0] >= a[n-1]: then a[n-1] becomes 0 (dies) and we remove it. Then we are left with a[0] and the rest. But note: a[0] is still the smallest? 
    #                However, if a[0] >= a[n-1], then actually a[0] is not the smallest anymore? But we sorted, so a[0] is the smallest. 
    #                But if a[0] >= a[n-1], then all numbers are equal? Not necessarily, but a[0] is the smallest and a[n-1] is the largest, so if a[0] >= a[n-1] then all are equal.
    #                Then the last health would be a[0] (since they all die except one, but the attacks: if all are equal, then one attack: x attacks x -> 0, so one dies, then we have n-1, and so on until one left with x).
    #             If a[0] < a[n-1]: then we can reduce a[n-1] by a[0] multiple times. The best is to reduce it until it becomes less than a[0]. 
    #                So a[n-1] becomes a[n-1] % a[0]. 
    #                But if a[n-1] % a[0] == 0, then a[n-1] becomes 0 and dies. Then we remove it and continue.
    #                If a[n-1] % a[0] != 0, then we have a new number: a[n-1] % a[0]. We then insert this new number into the sorted list and continue.
    #             However, note: the new number (a[n-1] % a[0]) might be smaller than a[0]? No, because modulo by a[0] gives a result in [0, a[0]-1]. 
    #                So if it's not zero, it is less than a[0]. Then the new smallest becomes this new number.
    #             Therefore, the algorithm:
    #               Sort the array.
    #               While there is more than one element:
    #                 Let x = a[0] (smallest) and y = a[-1] (largest).
    #                 If x >= y: 
    #                    Then y becomes 0 (dies). Remove y. (But note: if x==y, then y becomes 0 and dies, and we are left with x and the rest. But x is still the smallest? Yes, because the rest are >= x originally, and now we remove y which was the largest, so the new largest is <= x? Not necessarily, but we remove the largest, so the new largest is the second largest originally, which is >= x. So x remains the smallest.)
    #                    Actually, if x >= y, then since x is the smallest and y is the largest, we must have x = y = ... = all elements. So we can just remove the last element and the rest remain equal. Then the last one will be x.
    #                 Else (x < y):
    #                    y = y % x
    #                    If y == 0: remove y (the last element).
    #                    Else: replace the last element with y, and then we need to re-sort? But note: y is now less than x, so the new smallest becomes y. 
    #                    So we can do: 
    #                       a[-1] = y
    #                       Then we know that the new smallest is y (since y < x and x was the smallest). So we swap a[0] and a[-1]? 
    #                       Actually, we can just set a[0] = y and remove the old a[0]? But we have multiple elements.
    #                    Alternatively, we can simulate without full re-sorting:
    #                       We have a sorted list. We take the smallest (a[0]) and the largest (a[-1]).
    #                       We replace a[-1] with a[-1] % a[0].
    #                       If the result is 0, we pop the last element.
    #                       If the result is not 0, then the new value is less than a[0]. So the new smallest is this new value. 
    #                       Therefore, we can set a[0] = (a[-1] % a[0]) and then pop the last element? But wait, we have other elements in between.
    #                       Actually, the new value (a[-1] % a[0]) is less than a[0], so it becomes the new smallest. The old a[0] is still there? 
    #                       But we used a[0] to attack, and a[0] remains unchanged. The victim (a[-1]) becomes (a[-1] % a[0]).
    #                       So now we have: [a[0], a[1], ..., a[-2], (a[-1] % a[0])].
    #                       And since (a[-1] % a[0]) < a[0], the new smallest is (a[-1] % a[0]).
    #                       So we can do:
    #                         new_val = a[-1] % a[0]
    #                         a[-1] = new_val
    #                         if new_val == 0:
    #                             a.pop()
    #                         else:
    #                             # Now the smallest is new_val, so we swap a[0] and a[-1] so that a[0] becomes the new smallest.
    #                             a[0], a[-1] = a[-1], a[0]
    #                             # But note: the array is no longer sorted in the middle, but we only care about the smallest and the largest for the next step.
    #                             # However, the next step we need the smallest and the largest. The smallest is now at a[0] (which is new_val) and the largest is still at a[-1]? 
    #                             # But wait, we just put the new_val at a[0] and the old a[0] is now at a[-1]. But the old a[0] might not be the largest anymore? 
    #                             # Actually, the old a[0] is the smallest originally, and now we have a new value that is even smaller. The rest of the array (a[1] to a[-2]) are between the old a[0] and the old a[-1]. 
    #                             # But the new largest might be the old a[-2] or the old a[0] (which is now at the end)? 
    #                             # This is getting messy.
    #
    #       Alternate efficient approach:
    #         We know that the process is similar to the Euclidean algorithm. 
    #         The minimal final health is the GCD of all the numbers? 
    #         Let me check with the sample: [2, 10, 8, 40]
    #           GCD(2,10,8,40) = 2. And the sample output is 2.
    #         Another sample: [3, 6, 9] -> GCD=3. 
    #           Simulation: 
    #             3 attacks 9 -> 6. Now [3,6,6]. 
    #             3 attacks 6 -> 3. Now [3,6,3] -> sort: [3,3,6]. 
    #             3 attacks 6 -> 3. Now [3,3,3]. 
    #             Then 3 attacks 3 -> 0, so one dies. Then [3,3]. Then 3 attacks 3 -> 0, so one dies. Last is 3.
    #         Another: [2, 5] -> GCD=1.
    #           2 attacks 5 -> 3. [2,3]. 
    #           2 attacks 3 -> 1. [2,1]. 
    #           Now 1 attacks 2 -> 1. [1,1]. 
    #           Then 1 attacks 1 -> 0. Last is 1.
    #         So it seems the answer is the GCD of all the numbers.
    #
    #       Why? Because the operations allow us to generate any linear combination of the initial numbers (with non-negative coefficients) as long as we follow the rules? 
    #         Actually, the operation: y = y - x (if y>=x) is like the Euclidean algorithm step. 
    #         And we can do this until we get the GCD. 
    #         Moreover, the last number remaining will be the GCD of the initial set.
    #
    #       Therefore, the solution is simply: compute the GCD of all the numbers in A.
    #
    #       Let me verify with the constraints: N up to 10^5, A_i up to 10^9. 
    #         Computing GCD of 10^5 numbers is efficient (O(N log(max(A)))).
    #
    #       So the code:
    #         import math
    #         from functools import reduce
    #         ans = reduce(math.gcd, a)
    #         print(ans)
    #
    #       But wait: the problem says "minimum possible final health". And the GCD is achievable? 
    #         Yes, because we can simulate the Euclidean algorithm steps to reduce the numbers to the GCD.
    #         And we cannot get lower than the GCD because any linear combination of the numbers (with integer coefficients) is a multiple of the GCD, and the operations only produce linear combinations (with non-negative coefficients, but note: the health never becomes negative, and the operations are subtractions).
    #         Actually, the health of the monsters are always non-negative linear combinations of the initial healths? 
    #           Initially, each monster has health A_i.
    #           When monster i attacks monster j: A_j becomes A_j - A_i.
    #           So the new health is a linear combination: A_j - A_i.
    #           By induction, every health at any time is a linear combination of the initial A_k's with integer coefficients (which can be negative? but note: the health must be non-negative).
    #           However, the final health must be a linear combination of the initial A_k's. 
    #           And the smallest positive linear combination of a set of numbers is the GCD.
    #           Therefore, the final health cannot be less than the GCD.
    #           And we can achieve the GCD by the Euclidean algorithm steps.
    #
    #       Therefore, the answer is the GCD of all the numbers.

    import math
    from functools import reduce

    result = reduce(math.gcd, a)
    print(result)

if __name__ == '__main__':
    solve()