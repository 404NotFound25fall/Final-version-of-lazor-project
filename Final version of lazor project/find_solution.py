from pathlib import Path
from itertools import permutations
from lazor_solver import Board, Ray, parse_bff, trace_all_rays
from itertools import combinations

# Load the board from a BFF file
bff_file = Path('examples/official/mad_1.bff')
board, inventory, open_slots = parse_bff(bff_file)

print("Searching for solution manually...")
print(f"Open slots: {open_slots}")
print(f"Need to place: {inventory}")
print()

best_hit = 0
best_grid = None

A_count = inventory.get('A', 0)
C_count = inventory.get('C', 0)

# Try all combinations of placing A and C pieces in the open slots
for a_positions in combinations(open_slots, A_count):
    remaining_slots = [s for s in open_slots if s not in a_positions]
    for c_positions in combinations(remaining_slots, C_count):

        test_grid = [row[:] for row in board.grid]
        for pos in a_positions:
            test_grid[pos[0]][pos[1]] = 'A'
        for pos in c_positions:
            test_grid[pos[0]][pos[1]] = 'C'

        test_board = Board(grid=test_grid, lasers=board.lasers, targets=board.targets)
        hits = trace_all_rays(test_board)

        if len(hits) > best_hit:
            best_hit = len(hits)
            best_grid = [row[:] for row in test_grid]
            print(f"Better config found! Hits {len(hits)}/{len(board.targets)} targets")
            for r in best_grid:
                print(" ".join(r))
            if best_hit == len(board.targets):
                print("\n🎉 SOLUTION FOUND!")
                break
    if best_hit == len(board.targets):
        break

print(f"\nBest result: {best_hit}/{len(board.targets)} targets hit")
