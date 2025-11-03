## Course Info

**Course:** EN.540.635 - Software Carpentry  
**Assignment:** Lazor Group Project  
**Due Date:** November 4, 2025  
**Institution:** Johns Hopkins University, ChemBE

**Group number** Yuan Ma, Junjia Zeng, Jiaming Wen

# Lazor Puzzle Solver

A Python solver for the Lazor mobile game that automatically finds solutions by placing reflective, opaque, and refractive blocks to guide lasers to target points.

## What This Does

This program solves Lazor puzzles by:
- Reading puzzle configurations from `.bff` files
- Testing all valid block placements
- Tracing laser paths through the grid
- Finding configurations where all target points are hit

## Features

1. Handles all three block types:
- **A (Reflect)**: Mirrors that bounce lasers
- **B (Opaque)**: Blocks that absorb lasers  
- **C (Refract)**: Prisms that split lasers into two beams
2. Supports fixed blocks in puzzle definitions  
3. Fast combinatorial search algorithm
4. Solves all official test boards in under 2 minutes  
5. Diagnostic mode for debugging  

## Quick Start

### Installation

No external dependencies needed - just Python 3.7+

```bash
cd "Final version of lazor project"
```

### Basic Usage

```bash
python3 lazor_solver.py -i INPUT.bff -o OUTPUT.txt
```

### Example

```bash
# Solve tiny_5 puzzle
python3 lazor_solver.py -i examples/official/tiny_5.bff -o out/tiny5.txt

# Solve mad_1 with diagnostics
python3 lazor_solver.py -i examples/official/mad_1.bff -o out/mad1.txt --diagnose
```

##  Command Line Options

| Option | Description |
|--------|-------------|
| `-i INPUT` | Input `.bff` puzzle file (required) |
| `-o OUTPUT` | Output solution file (required) |
| `--diagnose` | Show best partial solution if no complete solution found |

## Project Structure

```
Final version of lazor project/
├── lazor_solver.py          # Main solver program
├── README.md                # This file
├── examples/
│   ├── official/            # Official test puzzles
│   │   ├── tiny_5.bff
│   │   ├── mad_1.bff
│   │   ├── mad_4.bff
│   │   ├── mad_7.bff
│   │   ├── dark_1.bff
│   │   ├── yarn_5.bff
│   │   ├── showstopper_4.bff
│   │   └── numbered_6.bff
│   └── solutions/           # Expected solutions
├── out/                     # Generated solutions
└── scripts/
    └── run all.py          # Batch test all puzzles
```

##  Testing All Puzzles

Run the batch test script:

```bash
python scripts/"run all.py"
```

This will solve all puzzles in `examples/official/` and save solutions to `out/`.

##  Performance

| Puzzle | Grid | Blocks | Time | Status |
|--------|------|--------|------|--------|
| tiny_5 | 3×3 | 4 | <5s | ✅ |
| mad_1 | 4×4 | 3 | <5s | ✅ |
| mad_4 | 4×5 | 5 | <10s | ✅ |
| mad_7 | 5×5 | 6 | <30s | ✅ |
| dark_1 | 3×3 | 3 | <5s | ✅ |
| yarn_5 | 6×5 | 8 | <60s | ✅ |
| showstopper_4 | 3×3 | 6 | <10s | ✅ |
| numbered_6 | 3×5 | 6 | <20s | ✅ |

All puzzles solve in under 2 minutes as required.

##  How It Works

### Algorithm Overview

1. **Parse** the `.bff` file to extract grid, blocks, lasers, and targets
2. **Generate** all valid combinations of block placements
3. **Trace** laser paths through each configuration using ray tracing
4. **Check** if all target points are hit
5. **Return** first valid solution found

### Ray Tracing

The solver uses a doubled-grid coordinate system where each grid cell occupies 2×2 units. This allows precise edge detection:

- When a laser crosses a vertical edge (x is even), check for horizontal blocks
- When a laser crosses a horizontal edge (y is even), check for vertical blocks  
- Handle corner collisions when both coordinates are even

### Block Interactions

- **Reflect (A)**: Reverses laser direction on the axis perpendicular to the edge
- **Opaque (B)**: Absorbs the laser completely
- **Refract (C)**: Splits into two beams - one continues, one reflects

## Troubleshooting

### "No solution found"

```bash
# Use diagnostic mode to see best attempt
python3 lazor_solver.py -i INPUT.bff -o OUTPUT.txt --diagnose
```

### "Input not found"

```bash
# Use absolute path or run from project root
cd "Final version of lazor project"
python3 lazor_solver.py -i examples/official/tiny_5.bff -o out/tiny5.txt
```
