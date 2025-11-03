#!/usr/bin/env python3
"""
批量运行 bff_files 目录下的测试文件
"""
import sys
import time
from pathlib import Path
from lazor_core import parse_bff, Board, solve_optimized, simulate_board

# bff 文件目录
BFF_DIR = Path("/Users/tommyboy/Downloads/bff_files")

# 按难度排序的测试文件
test_files = [
    ("tiny_5.bff", "简单测试"),
    ("mad_1.bff", "普通测试 1"),
    ("mad_4.bff", "普通测试 4"),
    ("yarn_5.bff", "中等测试"),
    ("showstopper_4.bff", "挑战测试"),
    ("dark_1.bff", "困难测试"),
    ("numbered_6.bff", "复杂测试"),
    ("mad_7.bff", "高级测试"),
]

def test_bff_file(filename: str, description: str):
    """测试单个 bff 文件"""
    filepath = BFF_DIR / filename
    
    if not filepath.exists():
        print(f"❌ 未找到文件: {filename}")
        return False
    
    print(f"\n{'='*60}")
    print(f"测试: {description} - {filename}")
    print('='*60)
    
    try:
        # 解析文件
        start_time = time.time()
        spec = parse_bff(str(filepath))
        board = Board.from_bffspec(spec)
        parse_time = time.time() - start_time
        
        print(f"解析时间: {parse_time:.3f}秒")
        print(f"棋盘大小: {board.nrows}x{board.ncols}")
        print(f"可放置方块: {sum(board.free_blocks.values())}")
        print(f"激光数量: {len(board.lasers)}")
        print(f"目标点数量: {len(board.points)}")
        
        # 尝试求解
        print("\n开始求解...")
        solve_start = time.time()
        solved_board = solve_optimized(board)
        solve_time = time.time() - solve_start
        
        if solved_board:
            print(f"✓ 找到解！ (耗时: {solve_time:.2f}秒)")
            
            # 验证解
            hit_points = simulate_board(solved_board)
            success = hit_points == board.points
            
            if success:
                print(f"✓ 解验证通过！")
                print(f"  目标点: {sorted(board.points)}")
                print(f"  击中点: {sorted(hit_points)}")
                return True
            else:
                print(f"✗ 解验证失败")
                print(f"  目标点: {sorted(board.points)}")
                print(f"  击中点: {sorted(hit_points)}")
                return False
        else:
            print(f"✗ 未找到解 (耗时: {solve_time:.2f}秒)")
            return False
            
    except Exception as e:
        print(f"✗ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("="*60)
    print("Lazor 求解器 - 批量测试")
    print("="*60)
    
    results = []
    
    for filename, description in test_files:
        success = test_bff_file(filename, description)
        results.append((filename, description, success))
    
    # 汇总结果
    print(f"\n{'='*60}")
    print("测试汇总")
    print('='*60)
    
    success_count = 0
    for filename, description, success in results:
        status = "✓ 通过" if success else "✗ 失败"
        print(f"{status}: {description} ({filename})")
        if success:
            success_count += 1
    
    print(f"\n总计: {success_count}/{len(results)} 个测试通过")
    
    if success_count == len(results):
        print("🎉 所有测试通过！")
    else:
        print("⚠️  部分测试失败，需要进一步调试")

if __name__ == "__main__":
    main()

