#!/usr/bin/env python3
"""Test script for promptimal with apinexus.net API"""

import os
import asyncio
from promptimal.optimizer.main import optimize

async def test_optimize():
    """Test prompt optimization with custom API"""
    # Set environment variables
    os.environ["OPENAI_API_KEY"] = "sk-hnOC1NXCUidvTpYGWK9TBWa1hU6E5zSNful4ohWIclaHBU66"
    os.environ["OPENAI_API_BASE"] = "https://apinexus.net/v1"
    os.environ["OPENAI_MODEL"] = "gpt-5.2"
    
    print("Starting prompt optimization test...")
    print(f"API Base: {os.environ.get('OPENAI_API_BASE')}")
    print(f"Model: {os.environ.get('OPENAI_MODEL')}")
    print()
    
    try:
        step_count = 0
        async for step in optimize(
            prompt="You will be provided with a piece of code, and your task is to explain it in a concise way.",
            improvement_request="Summaries need to include less code references and be more high-level.",
            population_size=2,
            num_iters=1,
            threshold=0.5
        ):
            step_count += 1
            print(f"Step {step_count}: {step.message}")
            if step.best_prompt:
                print(f"  Best prompt: {step.best_prompt[:100]}...")
            if step.best_score:
                print(f"  Best score: {step.best_score}")
            if step.is_terminal:
                print("  Optimization complete!")
                break
            # Limit to first few steps for testing
            if step_count >= 3:
                print("  (Stopping after 3 steps for testing)")
                break
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_optimize())

