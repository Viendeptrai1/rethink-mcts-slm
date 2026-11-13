import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    s = input_data[1]
    
    # There are 3! = 6 possible nice patterns based on the permutation of colors assigned to positions mod 3.
    # The pattern is determined by which color goes to index % 3 == 0, which to 1, which to 2.
    colors = ['R', 'G', 'B']
    perms = [
        (colors[0], colors[1], colors[2]),
        (colors[0], colors[2], colors[1]),
        (colors[1], colors[0], colors[2]),
        (colors[1], colors[2], colors[0]),
        (colors[2], colors[0], colors[1]),
        (colors[2], colors[1], colors[0])
    ]
    
    min_recolors = n + 1
    best_pattern = None
    best_res = ""
    
    for p in perms:
        # p[0] is color for i % 3 == 0
        # p[1] is color for i % 3 == 1
        # p[2] is color for i % 3 == 2
        
        current_res = []
        recolors = 0
        
        for i in range(n):
            rem = i % 3
            target_color = p[rem]
            if s[i] != target_color:
                recolors += 1
            current_res.append(target_color)
        
        if recolors < min_recolors:
            min_recolors = recolors
            best_pattern = p
            best_res = "".join(current_res)
    
    print(min_recolors)
    print(best_res)

if __name__ == "__main__":
    solve()