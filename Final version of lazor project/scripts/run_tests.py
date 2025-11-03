#!/usr/bin/env python3
"""批量测试不同的场景"""
from lazor_core import parse_bff, Board, simulate_board

test_files = [
    ("test_reflect.bff", "反射测试"),
    ("test_opaque.bff", "遮挡测试"),
    ("test_refract.bff", "分束测试"),
    ("mini_test.bff", "综合测试"),
]

for filename, description in test_files:
    print(f"\n{'='*50}")
    print(f"测试: {description} ({filename})")
    print('='*50)
    
    try:
        spec = parse_bff(filename)
        board = Board.from_bffspec(spec)
        
        print(f"棋盘大小: {board.nrows}x{board.ncols}")
        print(f"激光数量: {len(board.lasers)}")
        print(f"目标点数量: {len(board.points)}")
        
        hit_points = simulate_board(board)
        
        print(f"\n击中的点: {sorted(hit_points)}")
        print(f"期望的点: {sorted(board.points)}")
        print(f"匹配: {'✓' if hit_points == board.points else '✗'}")
        
    except FileNotFoundError:
        print(f"未找到文件: {filename}")
    except Exception as e:
        print(f"错误: {e}")

print(f"\n{'='*50}")
print("测试完成！")
print('='*50)

