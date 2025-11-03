#!/usr/bin/env python3

from __future__ import annotations
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import List, Tuple, Dict, Optional, Set
import argparse
import sys

Cell = str
Point = Tuple[int, int]

@dataclass(frozen=True)
class Ray:
    '''
    Represents a laser ray with position and velocity.
    '''
    x: int
    y: int
    vx: int
    vy: int

@dataclass
class Board:
    '''
    Represents the lazor board with grid, lasers, and targets.
    '''
    grid: List[List[Cell]]
    lasers: List[Ray]
    targets: List[Point]

    @property
    def H(self) -> int:
        return len(self.grid)

    @property
    def W(self) -> int:
        return len(self.grid[0]) if self.grid else 0

    def cell_at(self, r: int, c: int) -> Optional[Cell]:
        if 0 <= r < self.H and 0 <= c < self.W:
            return self.grid[r][c]
        return None

# ---------------------------
# Parsing
# ---------------------------

def _tok_int(s: str) -> int:
    '''
    Parse an integer token, stripping '=' if present.
    input: "5" or "=5"
    output: 5
    '''
    return int(s.replace("=", ""))

def parse_bff(path: Path) -> Tuple[Board, Dict[str, int], List[Tuple[int, int]]]:
    '''
    Parse a .bff file into a Board, inventory, and open slots.
    input: Path to .bff file
    output: (Board, inventory dict, list of open slot coordinates)
    '''
    lines = []
    for raw in path.read_text().splitlines():
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        lines.append(s)

    grid: List[List[Cell]] = []
    lasers: List[Ray] = []
    targets: List[Point] = []
    inv = {"A": 0, "B": 0, "C": 0}

    i = 0
    while i < len(lines):
        tok = lines[i]
        up = tok.upper()
        if up == "GRID START":
            i += 1
            buf: List[List[Cell]] = []
            while i < len(lines) and lines[i].upper() != "GRID STOP":
                row = list(lines[i].replace(" ", ""))
                if any(ch not in {"o", "x", "A", "B", "C"} for ch in row):
                    raise ValueError(f"Invalid GRID line: {lines[i]}")
                buf.append(row)
                i += 1
            if i == len(lines) or lines[i].upper() != "GRID STOP":
                raise ValueError("Missing GRID STOP")
            grid = buf
        elif tok[0] in {"A", "B", "C"} and tok[1:].strip():
            parts = tok.split()
            if len(parts) != 2:
                raise ValueError(f"Bad inventory line: {tok}")
            kind, num = parts[0], _tok_int(parts[1])
            if kind not in inv:
                raise ValueError(f"Unknown inventory key: {kind}")
            inv[kind] = num
        elif tok.startswith("L"):
            parts = tok.split()
            if len(parts) != 5:
                raise ValueError(f"Bad laser line: {tok}")
            _, sx, sy, vx, vy = parts
            lasers.append(Ray(_tok_int(sx), _tok_int(sy),
                              1 if _tok_int(vx) > 0 else -1,
                              1 if _tok_int(vy) > 0 else -1))
        elif tok.startswith("P"):
            parts = tok.split()
            if len(parts) != 3:
                raise ValueError(f"Bad target line: {tok}")
            _, px, py = parts
            targets.append((_tok_int(px), _tok_int(py)))
        i += 1

    if not grid:
        raise ValueError("GRID not found")

    w = len(grid[0])
    if any(len(r) != w for r in grid):
        raise ValueError("GRID is not rectangular")

    open_slots: List[Tuple[int, int]] = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == "o":
                open_slots.append((r, c))

    return Board(grid=grid, lasers=lasers, targets=targets), inv, open_slots

# ---------------------------
# Physics 
# ---------------------------

def trace_all_rays(board: Board, step_cap: int = 10000) -> Set[Point]:
    """
    Trace all rays on the board and return the set of hit target points.
    input: Board, optional step cap to prevent infinite loops
    output: Set of Points that were hit by lasers
    """
    hit: Set[Point] = set()
    rays: List[Ray] = list(board.lasers)
    seen: Set[Tuple[int, int, int, int]] = set()

    xmax, ymax = board.W * 2, board.H * 2

    while rays:
        r = rays.pop()
        x, y = r.x, r.y
        vx = 1 if r.vx > 0 else -1
        vy = 1 if r.vy > 0 else -1
        steps = 0

        while 0 <= x <= xmax and 0 <= y <= ymax:
            if steps > step_cap:
                break
            state = (x, y, vx, vy)
            if state in seen:
                break
            seen.add(state)

            nx, ny = x + vx, y + vy
            
            if nx < 0 or nx > xmax or ny < 0 or ny > ymax:
                break

            orig_vx, orig_vy = vx, vy
            blocked = False

            mx = (x + nx) // 2
            my = (y + ny) // 2

            crossed_vertical = (nx % 2 == 0)
            crossed_horizontal = (ny % 2 == 0)

            if crossed_vertical and crossed_horizontal:
                c_edge = nx // 2
                r_edge = ny // 2
                
                check_col = c_edge if orig_vx > 0 else c_edge - 1
                check_row = r_edge if orig_vy > 0 else r_edge - 1
                
                check_col = max(0, min(check_col, board.W - 1))
                check_row = max(0, min(check_row, board.H - 1))
                
                cell = board.cell_at(check_row, check_col)
                
                if cell == "A":
                    vx, vy = -vx, -vy
                elif cell == "B":
                    blocked = True
                elif cell == "C":
                    rays.append(Ray(nx, ny, -orig_vx, -orig_vy))

            elif crossed_vertical:
                c_edge = nx // 2
                check_row = my // 2
                check_col = c_edge if orig_vx > 0 else c_edge - 1
                
                check_col = max(0, min(check_col, board.W - 1))
                check_row = max(0, min(check_row, board.H - 1))
                
                cell = board.cell_at(check_row, check_col)
                
                if cell == "A":
                    vx = -vx
                elif cell == "B":
                    blocked = True
                elif cell == "C":
                    rays.append(Ray(nx, ny, -orig_vx, orig_vy))

            elif crossed_horizontal:
                r_edge = ny // 2
                check_col = mx // 2
                check_row = r_edge if orig_vy > 0 else r_edge - 1
                
                check_col = max(0, min(check_col, board.W - 1))
                check_row = max(0, min(check_row, board.H - 1))
                
                cell = board.cell_at(check_row, check_col)
                
                if cell == "A":
                    vy = -vy
                elif cell == "B":
                    blocked = True
                elif cell == "C":
                    rays.append(Ray(nx, ny, orig_vx, -orig_vy))

            if blocked:
                break

            x, y = nx, ny
            steps += 1

            if (x, y) in board.targets:
                hit.add((x, y))

    return hit

# ---------------------------
# Search
# ---------------------------

def place_and_solve(base: Board, inventory: Dict[str, int], open_slots: List[Tuple[int, int]], diagnose: bool = False) -> Optional[List[List[Cell]]]:
    '''
    Try to place blocks from inventory into open slots to hit all targets.
    input: Base Board, inventory dict, list of open slot coordinates, diagnose flag
    output: Solved grid layout or None if no solution
    '''
    if inventory["A"] + inventory["B"] + inventory["C"] > len(open_slots):
        if diagnose:
            print(f"[Diagnosis] Best hit = 0/{len(base.targets)}")
        return None

    targets = set(base.targets)
    grid0 = [row[:] for row in base.grid]

    def with_layout(posA, posB, posC):
        '''
        Return a new grid with blocks placed at specified positions.
        input: positions for A, B, C blocks
        output: new grid layout
        '''
        g = [row[:] for row in grid0]
        for r, c in posA: g[r][c] = "A"
        for r, c in posB: g[r][c] = "B"
        for r, c in posC: g[r][c] = "C"
        return g

    best_hit = 0
    best_layout: Optional[List[List[Cell]]] = None
    slots = open_slots
    nA, nB, nC = inventory["A"], inventory["B"], inventory["C"]

    count = 0
    for posC in combinations(slots, nC) if nC <= len(slots) else [()]:
        rem1 = [p for p in slots if p not in posC]
        for posA in combinations(rem1, nA) if nA <= len(rem1) else [()]:
            rem2 = [p for p in rem1 if p not in posA]
            for posB in combinations(rem2, nB) if nB <= len(rem2) else [()]:
                count += 1
                if count % 100 == 0:
                    print(f"  Tested {count} combinations (best: {best_hit}/{len(targets)})", end="\r")
                
                g = with_layout(posA, posB, posC)
                brd = Board(grid=g, lasers=base.lasers, targets=base.targets)
                got = trace_all_rays(brd)
                
                if len(got) > best_hit:
                    best_hit = len(got)
                    best_layout = g
                    print(f"\n  New best: {best_hit}/{len(targets)} targets hit")
                
                if got >= targets:
                    print(f"\n  Solution found after {count} attempts!")
                    return g

    if diagnose:
        print(f"\n[Diagnosis] Best hit = {best_hit}/{len(targets)}")
        if best_layout:
            print("[Diagnosis] Best partial layout:")
            print(grid_to_string(best_layout))
    
    return best_layout if best_hit > 0 else None

# ---------------------------
# IO
# ---------------------------

def grid_to_string(grid: List[List[Cell]]) -> str:
    '''
    Convert grid to string representation.
    input: grid as list of list of Cells
    output: string representation of the grid
    '''
    return "\n".join("".join(row) for row in grid)

def write_solution(path: Path, grid: List[List[Cell]]):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(grid_to_string(grid))

# ---------------------------
# CLI
# ---------------------------

def main(argv: Optional[List[str]] = None) -> int:
    '''
    Command-line interface for the lazor solver.
    input: argv list or None to use sys.argv
    output: exit code
    '''
    p = argparse.ArgumentParser(description="Lazor Unified Solver - Final Version")
    p.add_argument("-i", "--input", required=True, help=".bff file path")
    p.add_argument("-o", "--output", required=True, help="Where to write solution grid (.txt)")
    p.add_argument("--diagnose", action="store_true", help="Print best partial hit if no solution")
    args = p.parse_args(argv)

    bff = Path(args.input)
    if not bff.exists():
        root = Path(__file__).resolve().parent
        alt = root / args.input
        if alt.exists():
            bff = alt
        else:
            print(f"Input not found: {args.input}", file=sys.stderr)
            return 2

    board, inventory, open_slots = parse_bff(bff)
    print(f"\nProcessing {bff.name}...")
    print(f"Grid: {board.H}x{board.W} | Inventory: A={inventory['A']}, B={inventory['B']}, C={inventory['C']}")
    print(f"Open slots: {len(open_slots)} | Targets: {len(board.targets)}")
    
    solved = place_and_solve(board, inventory, open_slots, diagnose=args.diagnose)
    outp = Path(args.output)

    if solved is None:
        print("\nNo solution found." + (" (See diagnosis above)" if args.diagnose else ""))
        return 1

    write_solution(outp, solved)
    print(f"\nSolution written to {outp}")
    print("\n" + grid_to_string(solved))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())