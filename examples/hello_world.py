#!/usr/bin/env python3
"""
Promptimal Hello World 示例
使用 apinexus.net API 进行提示词优化

这个示例展示了如何使用 promptimal 优化提示词。
适合初学者学习和理解 promptimal 的基本用法。
"""

import os
import sys
import asyncio

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from promptimal.optimizer.main import optimize

async def hello_world():
    """Hello World 示例：优化一个简单的提示词"""
    
    # 步骤 1: 配置 API 环境变量
    # 这些环境变量告诉 promptimal 使用哪个 API 服务
    os.environ["OPENAI_API_KEY"] = "sk-hnOC1NXCUidvTpYGWK9TBWa1hU6E5zSNful4ohWIclaHBU66"
    os.environ["OPENAI_API_BASE"] = "https://apinexus.net/v1"
    os.environ["OPENAI_MODEL"] = "gpt-5.2"
    
    print("=" * 60)
    print("Promptimal Hello World 示例")
    print("=" * 60)
    print(f"API 服务: {os.environ.get('OPENAI_API_BASE')}")
    print(f"使用模型: {os.environ.get('OPENAI_MODEL')}")
    print("=" * 60)
    print()
    
    # 步骤 2: 定义初始提示词和改进目标
    initial_prompt = "Hello, world!"
    improvement_request = "让这个提示词更加友好和吸引人"
    
    print(f"初始提示词: {initial_prompt}")
    print(f"改进目标: {improvement_request}")
    print()
    print("开始优化...")
    print("-" * 60)
    
    # 步骤 3: 运行优化
    # optimize() 函数会返回一个异步生成器，每次产生一个优化步骤
    step_count = 0
    best_prompt = None
    best_score = None
    
    try:
        async for step in optimize(
            prompt=initial_prompt,
            improvement_request=improvement_request,
            population_size=2,      # 每代生成 2 个候选提示词
            num_iters=1,            # 运行 1 次迭代
            threshold=0.5           # 如果得分超过 0.5 就停止
        ):
            step_count += 1
            print(f"\n步骤 {step_count}: {step.message}")
            
            # 显示当前最佳提示词
            if step.best_prompt:
                best_prompt = step.best_prompt
                print(f"  当前最佳提示词: {best_prompt}")
            
            # 显示当前最佳得分
            if step.best_score is not None:
                best_score = step.best_score
                print(f"  当前最佳得分: {best_score:.2f}")
            
            # 如果优化完成，显示最终结果
            if step.is_terminal:
                print("\n" + "=" * 60)
                print("优化完成！🎉")
                print("=" * 60)
                if best_prompt:
                    print(f"\n最终优化后的提示词:\n{best_prompt}")
                if best_score is not None:
                    print(f"\n最终得分: {best_score:.2f}")
                break
            
            # 为了教学示例，我们限制只显示前几步
            if step_count >= 5:
                print("\n(为了演示，这里只显示前 5 步)")
                break
                
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("\n" + "=" * 60)
    print("示例运行完成！")
    print("=" * 60)

if __name__ == "__main__":
    # 运行异步函数
    asyncio.run(hello_world())

