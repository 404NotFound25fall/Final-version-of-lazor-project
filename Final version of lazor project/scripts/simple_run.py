#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

try:
    print("开始测试...")
    from lazor_core import parse_bff, Board
    print("导入成功")
    
    spec = parse_bff("mini_test.bff")
    print("解析成功")
    
    board = Board.from_bffspec(spec)
    print("Board 创建成功")
    print(board.summary())
    
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()

