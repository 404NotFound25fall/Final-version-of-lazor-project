#!/usr/bin/env python3
"""快速测试并显示输出"""
import sys
import traceback

try:
    from lazor_core import parse_bff, Board
    
    print("=== 测试解析 ===")
    spec = parse_bff("mini_test.bff")
    board = Board.from_bffspec(spec)
    
    print("✓ 解析成功")
    print(board.summary())
    
    print("\n=== 测试模拟器 ===")
    from lazor_core import simulate_board
    hit_points = simulate_board(board)
    
    print(f"击中的点: {sorted(hit_points)}")
    print(f"期望的点: {sorted(board.points)}")
    print(f"匹配: {hit_points == board.points}")
    
except Exception as e:
    print(f"错误: {e}")
    traceback.print_exc()

