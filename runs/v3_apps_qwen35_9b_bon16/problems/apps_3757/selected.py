import sys

def solve():
    input_data = sys.stdin.read().strip().split()
    if not input_data:
        return
    a00 = int(input_data[0])
    a01 = int(input_data[1])
    a10 = int(input_data[2])
    a11 = int(input_data[3])

    # Total number of pairs is (n choose 2) = a00+a01+a10+a11
    # Let n be the length of the string.
    # n*(n-1)/2 = total_pairs
    total = a00 + a01 + a10 + a11
    if total == 0:
        # We need a non-empty string. If all are 0, we can output "0" or "1".
        # But check constraints: if input is 0 0 0 0, then n=1 works (0 pairs).
        print("0")
        return

    # Solve n*(n-1)/2 = total for positive integer n
    # n^2 - n - 2*total = 0
    # n = (1 + sqrt(1 + 8*total)) / 2
    d = 1 + 8 * total
    s_d = int(d ** 0.5)
    if s_d * s_d != d:
        print("Impossible")
        return
    n = (1 + s_d) // 2
    if n * (n - 1) // 2 != total:
        print("Impossible")
        return
    if n < 1:
        print("Impossible")
        return

    # Count of 0s and 1s
    # Let z = count of '0', o = count of '1'
    # z + o = n
    # a00 = z*(z-1)/2  => z*(z-1) = 2*a00
    # a11 = o*(o-1)/2  => o*(o-1) = 2*a11
    # a01 = z*o - a00  (pairs 0 then 1)
    # a10 = z*o - a11  (pairs 1 then 0)
    # Note: a01 + a10 = z*o

    # Solve for z from a00
    if a00 == 0:
        z = 0 or 1
        # z*(z-1) = 0 => z=0 or z=1. Since n>=1, we will see later.
        # We need to determine uniquely if possible.
        # Actually, if a00=0, z can be 0 or 1.
        pass
    else:
        # z*(z-1) = 2*a00
        val = 2 * a00
        z = 0
        found_z = False
        # Since z <= n <= 1000000 approx (sqrt(2*10^9) ~ 45000), we can iterate or solve quadratic.
        # Quadratic: z^2 - z - val = 0
        # d_z = 1 + 4*val
        d_z = 1 + 4 * val
        s_d_z = int(d_z ** 0.5)
        if s_d_z * s_d_z != d_z:
            print("Impossible")
            return
        z = (1 + s_d_z) // 2
        if z * (z - 1) // 2 != a00:
            print("Impossible")
            return
        # Check if z is integer (it is by construction if perfect square)
        # But we need to ensure z is consistent with n later.
        # Also, a00=0 could mean z=0 or z=1. The formula gives z=1 if val=0? 
        # If val=0, d_z=1, s_d_z=1, z=(1+1)//2=1. So it picks 1.
        # What if actual z=0? Then a00=0. Our formula gives z=1. 
        # If z=1, a00=0 holds. So z=1 is a valid solution for a00=0.
        # But we also have constraint z+o=n.
        # We might have ambiguity if a00=0 and we pick z=1, but maybe z=0 is required?
        # Let's solve for o similarly and check consistency.

    # Solve for o from a11
    if a11 == 0:
        # o=0 or o=1
        # We'll compute candidate o using same logic as z
        val_o = 2 * a11
        d_o = 1 + 4 * val_o
        s_d_o = int(d_o ** 0.5)
        if s_d_o * s_d_o != d_o:
            print("Impossible")
            return
        o = (1 + s_d_o) // 2
        if o * (o - 1) // 2 != a11:
            print("Impossible")
            return
    else:
        val_o = 2 * a11
        d_o = 1 + 4 * val_o
        s_d_o = int(d_o ** 0.5)
        if s_d_o * s_d_o != d_o:
            print("Impossible")
            return
        o = (1 + s_d_o) // 2
        if o * (o - 1) // 2 != a11:
            print("Impossible")
            return

    # Now we have candidates for z and o.
    # However, if a00=0, the quadratic gives z=1. But z could be 0.
    # Similarly for a11=0, o could be 0 or 1.
    # We need z + o = n.
    # Let's collect possible values for z and o.
    possible_z = set()
    if a00 == 0:
        possible_z.add(0)
        possible_z.add(1)
    else:
        val = 2 * a00
        d_z = 1 + 4 * val
        s_d_z = int(d_z ** 0.5)
        if s_d_z * s_d_z == d_z:
            z_cand = (1 + s_d_z) // 2
            if z_cand * (z_cand - 1) // 2 == a00:
                possible_z.add(z_cand)

    possible_o = set()
    if a11 == 0:
        possible_o.add(0)
        possible_o.add(1)
    else:
        val = 2 * a11
        d_o = 1 + 4 * val
        s_d_o = int(d_o ** 0.5)
        if s_d_o * s_d_o == d_o:
            o_cand = (1 + s_d_o) // 2
            if o_cand * (o_cand - 1) // 2 == a11:
                possible_o.add(o_cand)

    found = False
    target_n = n
    for z in possible_z:
        if z > n: continue
        for o in possible_o:
            if o > n: continue
            if z + o == n:
                # Check cross terms
                # Total pairs of (0,1) or (1,0) must equal z*o
                total_cross = a01 + a10
                if z * o != total_cross:
                    continue
                
                # Check individual cross terms
                # a01 is number of 0...1 subsequences
                # a10 is number of 1...0 subsequences
                # We need to construct the string.
                # If a01 == 0 and a10 == 0, then either all 0s or all 1s or separated such that no 0..1 and no 1..0?
                # Actually if both are 0, then no 0 before 1 and no 1 before 0.
                # This implies all 0s come after all 1s? No, if all 0s come after all 1s, we have 1...0 pairs (a10 > 0) unless one count is 0.
                # If a01=0 and a10=0, then either z=0 or o=0 (impossible since z+o=n>=1 and if both>0 we have some order).
                # Wait, if string is "0011", we have 0..1 pairs (a01 > 0).
                # If string is "1100", we have 1..0 pairs (a10 > 0).
                # To have both 0, we must have all 0s or all 1s (so one count is 0).
                # Or maybe n=1? If n=1, z+o=1. If z=1, o=0 => a01=0, a10=0. Correct.
                # So if z>0 and o>0, we must have at least one cross pair.
                # Thus if z>0 and o>0 and (a01==0 or a10==0), impossible?
                # Actually a01 + a10 = z*o. If z>0 and o>0, then z*o >= 1. So a01+a10 >= 1.
                # So if a01+a10 != z*o, we skip. We already checked that.
                # Now we need to check if specific a01 and a10 are achievable with SOME arrangement of z zeros and o ones.
                
                # Strategy to construct:
                # We want exactly a01 pairs of (0,1).
                # We have z zeros and o ones.
                # Let the positions of zeros be p_1, p_2, ..., p_z.
                # Let the positions of ones be q_1, q_2, ..., q_o.
                # A 0 at p_i and 1 at q_j contributes to a01 if p_i < q_j.
                # A 1 at q_j and 0 at p_i contributes to a10 if q_j < p_i.
                # Note that for any pair of indices (one zero, one one), exactly one of these conditions holds.
                # So a01 + a10 = z * o. This is always true if we arrange them.
                # We just need to ensure we can get exactly a01.
                # Consider arranging all zeros first then all ones: "00...011...1".
                # Then every zero is before every one.
                # Number of 0..1 pairs = z * o.
                # Number of 1..0 pairs = 0.
                # So max a01 = z*o, min a01 = 0.
                # Can we achieve any value between 0 and z*o?
                # Yes. We can move ones to the left.
                # Start with all zeros then all ones (a01 = z*o, a10 = 0).
                # Move one '1' from the far right to the far left.
                # Originally: 0...0 1...1 (z zeros, o ones).
                # Move one '1' to front: 1 0...0 1...1-1.
                # The moved '1' is now before all z zeros. So it creates z new 1..0 pairs.
                # It was before no zeros (since it was after all zeros). So a10 increases by z.
                # Conversely, a01 decreases by z (since this '1' was contributing z to a01, now it contributes 0).
                # So by moving k ones to the front, we get:
                # a10 = k * z
                # a01 = z * o - k * z = z * (o - k)
                # Here k is the number of ones placed before all zeros.
                # But we can have ones interleaved.
                # General construction:
                # Place some number of ones (say k) at the beginning.
                # Then place all z zeros.
                # Then place the remaining o-k ones.
                # String: "1"*k + "0"*z + "1"*(o-k)
                # Count a10: Each of the k leading ones is before all z zeros. So k*z.
                # Count a01: Each of the (o-k) trailing ones is after all z zeros. So z*(o-k).
                # Total cross: k*z + z*(o-k) = z*o. Correct.
                # So we need to find integer k such that:
                # k * z = a10  AND  z * (o - k) = a01
                # From first eq: k = a10 / z.
                # This requires z > 0.
                # If z == 0:
                #   Then a00 must be 0 (ok), a01 must be 0 (since z*o=0), a10 must be 0.
                #   We have a11 = o*(o-1)/2.
                #   If a01=0 and a10=0, and z=0, then any arrangement of ones works (only 1s).
                #   So if z=0, we just need a01==0, a10==0. And we output "1"*o.
                # If z > 0:
                #   k must be integer, so a10 % z == 0.
                #   k = a10 // z.
                #   Then we must have 0 <= k <= o.
                #   And check if z * (o - k) == a01.
                
                if z == 0:
                    if a01 != 0 or a10 != 0:
                        continue
                    # Valid
                    res = "1" * o
                    if len(res) <= 1000000:
                        print(res)
                        found = True
                        break
                else:
                    if a10 % z != 0:
                        continue
                    k = a10 // z
                    if k < 0 or k > o:
                        continue
                    if z * (o - k) != a01:
                        continue
                    # Valid
                    # Construct: k ones, z zeros, o-k ones
                    # Check length
                    length = k + z + (o - k)
                    if length > 1000000:
                        continue
                    res = "1" * k + "0" * z + "1" * (o - k)
                    print(res)
                    found = True
                    break
            if found:
                break
        if found:
            break

    if not found:
        print("Impossible")

if __name__ == '__main__':
    solve()