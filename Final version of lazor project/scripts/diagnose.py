#!/usr/bin/env python3
"""诊断脚本 - 找出为什么求不出解"""
from lazor_core import parse_bff, Board, simulate_board, get_placeable_positions, get_blocks_to_place

# 解析
spec = parse_bff("mini_test.bff")
board = Board.from_bffspec(spec)

print("=== 1. 棋盘信息 ===")
print(board.summary())

print("\n=== 2. 分析当前配置 ===")
# 测试当前配置
hit_points = simulate_board(board)
print(f"当前击中点: {sorted(hit_points)}")
print(f"期望目标点: {sorted(board.points)}")
print(f"匹配: {hit_points == board.points}")

print("\n=== 3. 检查可放置位置 ===")
positions = get_placeable_positions(board)
print(f"可放置位置数量: {len(positions)}")
print(f"前5个位置: {positions[:5]}")

print("\n=== 4. 检查需要放置的方块 ===")
blocks = get_blocks_to_place(board)
print(f"需要放置的方块: {blocks}")

print("\n=== 5. 手动尝试第一个组合 ===")
if len(positions) >= len(blocks):
    import copy
    test_board = copy.deepcopy(board)
    
    # 尝试第一个位置组合
    from itertools import combinations, permutations
    first_combo = list(combinations(positions, len(blocks)))[0]
    print(f"尝试位置组合: {first_combo}")
    
    # 尝试第一种方块排列
    first_perm = list(permutations(blocks))[0]
    print(f"尝试方块排列: {first_perm}")
    
    try:
        for i, (r, c) in enumerate(first_combo):
            test_board.place_block(r, c, first_perm[i])
        
        hit = simulate_board(test_board)
        print(f"击中点: {sorted(hit)}")
        print(f"匹配: {hit == board.points}")
    except Exception as e:
        print(f"错误: {e}")

print("\n=== 6. 检查求解器统计 ===")
from itertools import combinations, permutations
num_pos = len(positions)
num_blocks = len(blocks)
num_combos = len(list(combinations(positions, num_blocks))) if num_pos >= num_blocks else 0
num_perms = len(list(permutations(blocks)))
total_tests = num_combos * num_perms
print(f"总共有 {total_tests} 个组合需要测试")
print(f"位置组合数: {num_combos}")
print(f"方块排列数: {num_perms}")

