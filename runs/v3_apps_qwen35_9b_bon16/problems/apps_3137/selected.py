import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        K = int(next(iterator))
        
        trap_r = int(next(iterator))
        trap_c = int(next(iterator))
        
        bacteria = []
        for _ in range(K):
            br = int(next(iterator))
            bc = int(next(iterator))
            direction_char = next(iterator)
            bacteria.append({'r': br, 'c': bc, 'dir': direction_char})
        
        grid_str = []
        for _ in range(N):
            grid_str.append(next(iterator))
        
        # Direction mappings: U, R, D, L
        # 0: Up, 1: Right, 2: Down, 3: Left
        dir_map = {'U': 0, 'R': 1, 'D': 2, 'L': 3}
        rev_dir_map = {0: 'U', 1: 'R', 2: 'D', 3: 'L'}
        
        # Movement deltas for Up, Right, Down, Left
        # (row_change, col_change)
        deltas = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        
        def get_cell_val(r, c, b_idx):
            # The grid is given once, but the problem says "the digit in row x and column y represents the number ... dedicated to bacterium i"
            # This phrasing is slightly ambiguous. Does the same grid apply to all bacteria?
            # "N by M matrix of digits ... dedicated to bacterium i" appears after listing all bacteria.
            # Usually in such problems, the grid is global and applies to all. The phrase "dedicated to bacterium i" might mean "for the simulation of bacterium i".
            # Given the input format, there is only ONE matrix provided after listing all bacteria.
            # So the grid is the same for all bacteria.
            if 1 <= r <= N and 1 <= c <= M:
                return int(grid_str[r-1][c-1])
            return 0 # Should not happen as we check bounds before moving or turning logic handles it differently? 
            # Actually, the logic says "Reads the number X ... in the current cell". It implies the bacterium is ON the cell.
            # So we only read when inside bounds.

        def run_simulation():
            # State: list of (r, c, dir_idx)
            states = []
            for b in bacteria:
                states.append({'r': b['r'], 'c': b['c'], 'dir': dir_map[b['dir']]})
            
            max_steps = 1000000 # Safety break for infinite loops, though problem says output -1 if never ends.
            # However, with N, M <= 50 and K <= 5, state space is finite. If it doesn't hit trap within reasonable steps, it's likely a loop.
            # But we need to detect if they ALL step on trap in the same second.
            # If they never do, output -1.
            # Since state space is finite (50*50)^5 is large but reachable states might cycle.
            # We can simulate step by step. If step count exceeds a safe limit (e.g., N*M*K or something larger), assume -1?
            # Actually, if they enter a cycle without hitting the trap together, it will never end.
            # Given constraints and typical CP problems, simulation for a large number of steps is feasible if the loop isn't intended to be detected via cycle hashing.
            # But "If the game will never end, output -1" suggests we must detect non-termination.
            # Let's set a generous limit. Max cells = 2500. Max bacteria = 5.
            # If they don't meet in 2500 * some_factor steps, maybe they are in a loop.
            # Let's use a visited states set to detect cycles. State = tuple of (r,c,dir) for all bacteria.
            
            visited_states = set()
            step = 0
            
            while True:
                step += 1
                current_state = tuple(sorted((s['r'], s['c'], s['dir']) for s in states))
                # Wait, sorting is needed if order of bacteria doesn't matter for state definition, but bacteria are distinct entities.
                # Better: keep bacteria ordered by initial index.
                state_tuple = tuple((s['r'], s['c'], s['dir']) for s in states)
                
                if state_tuple in visited_states:
                    # Cycle detected and trap not hit yet -> never ends
                    return -1
                visited_states.add(state_tuple)
                
                # Check for trap kill
                # "The trap will activate and kill the bacteria as soon as they all step on that cell in the same second."
                # "step on that cell" happens after moving.
                # So we simulate movement, then check.
                
                # Process each bacterium
                new_states = []
                alive = True
                
                for s in states:
                    r, c, d = s['r'], s['c'], s['dir']
                    
                    # 1. Read X
                    val = get_cell_val(r, c, -1) # Index doesn't matter, grid is global
                    
                    # 2. Turn 90 degrees clockwise X times
                    # Clockwise: U->R->D->L->U (0->1->2->3->0)
                    d = (d + val) % 4
                    
                    # 3. If facing outside, turn 180 degrees
                    # Check where it is facing
                    nr, nc = r + deltas[d][0], c + deltas[d][1]
                    if not (1 <= nr <= N and 1 <= nc <= M):
                        # Turn 180
                        d = (d + 2) % 4
                    
                    # 4. Move
                    r, c = r + deltas[d][0], c + deltas[d][1]
                    
                    s['r'] = r
                    s['c'] = c
                    s['dir'] = d
                    new_states.append(s)
                
                states = new_states
                
                # Check if all are on trap
                all_on_trap = True
                for s in states:
                    if s['r'] != trap_r or s['c'] != trap_c:
                        all_on_trap = False
                        break
                
                if all_on_trap:
                    return step
                
                # Safety break if step count gets extremely high and we haven't seen a state repeat?
                # The visited set handles cycles. If we run out of memory (unlikely with 50^5 states? 2500^5 is huge)
                # We need a better cycle detection or rely on the fact that if they don't meet soon, it's -1.
                # However, state space can be up to 2500^5 which is too big for a set.
                # But N, M <= 50, K <= 5. Is the period small?
                # Maybe we don't need full state history. Just check if step exceeds N*M*K * some factor?
                # Let's reconsider the cycle detection. If the system is deterministic and finite state, it must cycle.
                # If the trap is not hit in the cycle, it never ends.
                # The only issue is storing too many states.
                # Given K=5, maybe we can just simulate up to a very large number? 
                # Or detect local cycles per bacterium? No, they must synchronize.
                # Alternative: Since N, M are small, maybe the LCM of periods is small? Not necessarily.
                # But in competitive programming with N=50, K=5, usually simulation limit is around 10^6 to 10^7 steps.
                # If it exceeds that, output -1.
                # Let's set a hard limit. 10^6 steps is safe for Python within 1-2 seconds if logic is O(K).
                # If not finished, return -1.
                if step > 1000000:
                    return -1

        print(run_simulation())

    except StopIteration:
        pass

if __name__ == '__main__':
    solve()