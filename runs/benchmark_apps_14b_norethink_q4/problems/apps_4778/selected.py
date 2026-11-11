import sys

def main():
    import sys
    import math

    def read_ints():
        return list(map(int, sys.stdin.readline().split()))

    P, D = read_ints()
    districts = [[] for _ in range(D)]
    total_votes_A = 0
    total_votes_B = 0

    for _ in range(P):
        d, a, b = read_ints()
        districts[d-1].append((a, b))
        total_votes_A += a
        total_votes_B += b

    results = []
    total_wasted_A = 0
    total_wasted_B = 0

    for district_votes in districts:
        votes_A = sum(vote[0] for vote in district_votes)
        votes_B = sum(vote[1] for vote in district_votes)
        total_votes = votes_A + votes_B
        majority_votes = total_votes // 2 + 1

        if votes_A > votes_B:
            wasted_A = votes_A - majority_votes
            wasted_B = votes_B
        else:
            wasted_A = votes_A
            wasted_B = votes_B - majority_votes

        results.append(('A' if votes_A > votes_B else 'B', wasted_A, wasted_B))
        total_wasted_A += wasted_A
        total_wasted_B += wasted_B

    for result in results:
        print(result[0], result[1], result[2])

    efficiency_gap = abs(total_wasted_A - total_wasted_B) / (total_votes_A + total_votes_B)
    print(f"{efficiency_gap:.10f}")

if __name__ == "__main__":
    main()