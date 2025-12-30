# Promptimal 使用指南（基于 apinexus.net API）

> **教学文档** - 本指南专门为使用 apinexus.net API 配置 promptimal 而编写，适合初学者学习使用。

## 📖 简介

### 什么是 Promptimal？

Promptimal 是一个使用遗传算法优化 AI 提示词的命令行工具。它可以帮助你：
- **自动优化提示词**：通过遗传算法迭代改进提示词质量
- **无需数据集**：只需要提供初始提示词和改进目标
- **使用 LLM 评估**：利用大语言模型评估提示词质量

### 为什么使用 Promptimal？

- ✅ **提高提示词质量**：自动找到更好的提示词表达方式
- ✅ **节省时间**：不需要手动反复调试提示词
- ✅ **科学方法**：使用遗传算法，有理论基础
- ✅ **易于使用**：简单的命令行接口，Python 代码调用

### 本指南的适用范围

本指南专门针对：
- 使用 **apinexus.net API** 的用户
- 使用 **gpt-5.2** 模型的用户
- 需要在 **本地环境** 部署和使用的用户
- **初学者** 和 **学生** 学习使用

> **参考资源**：如需了解 promptimal 的更多信息，请参考[原始英文 README](./README_EN.md) 和 [GitHub 仓库](https://github.com/shobrook/promptimal)。

---

## 🚀 快速开始

### 前置要求

- Python 3.7+
- conda 环境（推荐使用 conda base）
- apinexus.net API 访问权限

### 步骤 1: 环境准备

确保你已经激活 conda base 环境：

```bash
conda activate base
python --version  # 应该显示 Python 3.x
```

### 步骤 2: 安装 Promptimal

如果你还没有安装，请先安装 promptimal：

```bash
cd promptimal
pip install -e .
```

### 步骤 3: 配置 API（重要！）

设置环境变量，告诉 promptimal 使用你的 API：

```bash
export OPENAI_API_KEY="sk-<your key>"
export OPENAI_API_BASE="https://apinexus.net/v1"
export OPENAI_MODEL="gpt-5.2"
```

**注意**：
- 这些环境变量需要在每次使用前设置
- 或者你可以将它们添加到你的 `~/.zshrc` 或 `~/.bashrc` 文件中
- API Key 请妥善保管，不要泄露

### 步骤 4: Hello World 示例

运行 Hello World 示例，快速体验 promptimal：

```bash
cd promptimal
python examples/hello_world.py
```

**实际运行输出示例**：

```
============================================================
Promptimal Hello World 示例
============================================================
API 服务: https://apinexus.net/v1
使用模型: gpt-5.2
============================================================

初始提示词: Hello, world!
改进目标: 让这个提示词更加友好和吸引人

开始优化...
------------------------------------------------------------

步骤 1: Starting optimization
  当前最佳提示词: Hello, world!

步骤 2: Starting optimization
  当前最佳提示词: Hello, world!

步骤 3: Starting optimization
  当前最佳提示词: Hello, world!

步骤 4: Starting optimization
  当前最佳提示词: Hello, world!

步骤 5: Starting optimization
  当前最佳提示词: Hello, world!
  当前最佳得分: 0.10

(为了演示，这里只显示前 5 步)

============================================================
示例运行完成！
============================================================
```

**说明**：
- 实际输出可能会因 API 响应和模型行为而略有不同
- 得分范围是 0-1，得分越高表示提示词质量越好
- 初始得分可能较低，这是正常现象
- 优化过程会进行多次 API 调用，请注意 API 费用

---

## 📚 详细使用

### 方法一：命令行使用

#### 基本用法

```bash
promptimal \
  --prompt "你的初始提示词" \
  --improve "你想要改进的方向"
```

#### 完整示例

```bash
promptimal \
  --prompt "You will be provided with a piece of code, and your task is to explain it in a concise way." \
  --improve "Summaries need to include less code references and be more high-level." \
  --num_iters=5 \
  --num_samples=10
```

#### 参数说明

- `--prompt`: 初始提示词（必需）
- `--improve`: 改进目标描述（必需）
- `--num_iters`: 优化迭代次数（默认 5）
- `--num_samples`: 每代生成的候选提示词数量（默认 10）
- `--threshold`: 终止阈值，得分超过此值则停止（默认 1.0）

### 方法二：Python 代码调用

#### 基本示例

```python
import os
import sys
import asyncio

# 添加项目根目录到 Python 路径（如果从 examples 目录运行）
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from promptimal.optimizer.main import optimize

async def optimize_prompt():
    # 1. 配置 API
    os.environ["OPENAI_API_KEY"] = "your_api_key"
    os.environ["OPENAI_API_BASE"] = "https://apinexus.net/v1"
    os.environ["OPENAI_MODEL"] = "gpt-5.2"
    
    # 2. 运行优化
    async for step in optimize(
        prompt="你的初始提示词",
        improvement_request="改进目标",
        population_size=5,
        num_iters=3
    ):
        print(f"{step.message}: {step.best_prompt}")
        if step.best_score is not None:
            print(f"  得分: {step.best_score:.2f}")
        if step.is_terminal:
            break

asyncio.run(optimize_prompt())
```

**实际运行时的注意事项**：
- 如果从 `examples/` 目录运行，需要添加路径设置（如示例代码所示）
- 如果从项目根目录运行，可以直接导入
- 得分不是每一步都显示，这是正常行为

#### 完整示例

参考 `examples/hello_world.py` 文件，里面有详细的注释说明。

### 参数详解

#### `population_size` (种群大小)
- **含义**：每代生成的候选提示词数量
- **建议值**：5-20
- **影响**：值越大，探索空间越大，但运行时间更长

#### `num_iters` (迭代次数)
- **含义**：优化循环运行的次数（相当于遗传算法的"代数"）
- **建议值**：3-10
- **影响**：值越大，优化越充分，但运行时间更长

#### `threshold` (终止阈值)
- **含义**：如果候选提示词得分超过此值，优化循环停止
- **默认值**：1.0
- **建议值**：0.7-1.0

---

## ❓ 常见问题

### Q1: API 连接失败怎么办？

**错误信息**：
```
Error: API connection failed
```

**解决方案**：
1. 检查环境变量是否正确设置：
   ```bash
   echo $OPENAI_API_KEY
   echo $OPENAI_API_BASE
   echo $OPENAI_MODEL
   ```
2. 验证 API Key 是否有效
3. 检查网络连接是否正常
4. 确认 API Base URL 是否正确（应该是 `https://apinexus.net/v1`）

### Q2: 模型名称错误怎么办？

**错误信息**：
```
Error: Model not found
```

**解决方案**：
1. 确认模型名称是否正确（应该是 `gpt-5.2`）
2. 检查环境变量 `OPENAI_MODEL` 是否设置
3. 如果使用其他模型，确保模型名称正确

### Q3: 如何永久设置环境变量？

**macOS/Linux**：
将以下内容添加到 `~/.zshrc` 或 `~/.bashrc`：

```bash
export OPENAI_API_KEY="your_api_key"
export OPENAI_API_BASE="https://apinexus.net/v1"
export OPENAI_MODEL="gpt-5.2"
```

然后执行：
```bash
source ~/.zshrc  # 或 source ~/.bashrc
```

### Q4: 运行时间太长怎么办？

**优化建议**：
- 减少 `num_iters`（迭代次数）：从 5 减到 2-3
- 减少 `population_size`（种群大小）：从 10 减到 3-5
- 提高 `threshold`（终止阈值）：从 1.0 降到 0.7，让优化提前停止

**实际测试**：
- Hello World 示例（1 次迭代，2 个候选）：约 10-30 秒
- 完整优化（5 次迭代，10 个候选）：约 1-3 分钟

### Q5: 如何查看详细的运行日志？

在代码中添加更多打印语句，或者使用 Python 的 logging 模块。

**示例**：
```python
async for step in optimize(...):
    print(f"步骤: {step.message}")
    print(f"最佳提示词: {step.best_prompt}")
    if step.best_score is not None:
        print(f"得分: {step.best_score:.2f}")
    if step.token_count:
        print(f"Token 使用: {step.token_count}")
```

### Q6: 为什么得分这么低？

**可能原因**：
1. 初始提示词太简单，改进空间有限
2. 迭代次数太少（建议增加 `num_iters`）
3. 改进目标不够具体

**解决方案**：
- 增加迭代次数：`num_iters=5` 或更多
- 使用更具体的改进目标
- 增加种群大小：`population_size=10` 或更多

### Q7: 运行时间大概多久？

**典型运行时间**：
- Hello World 示例（1 次迭代，2 个候选）：约 10-30 秒
- 完整优化（5 次迭代，10 个候选）：约 1-3 分钟

**影响因素**：
- API 响应速度
- 迭代次数
- 种群大小
- 网络状况

**注意**：每次优化会进行多次 API 调用，运行时间会相应增加。

---

## 🔧 高级用法

### 自定义评估函数

如果你想要使用自己的评估标准，可以创建自定义评估函数：

```python
# evaluator.py
import argparse

def evaluator(prompt: str) -> float:
    # 你的评估逻辑
    # 必须返回 0 到 1 之间的值
    score = your_evaluation_logic(prompt)
    return score

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True, type=str)
    args = parser.parse_args()
    
    score = evaluator(args.prompt)
    print(score)

if __name__ == "__main__":
    main()
```

然后使用：
```bash
promptimal --evaluator="path/to/evaluator.py" --prompt "..." --improve "..."
```

### 批量优化

你可以编写脚本批量优化多个提示词：

```python
prompts = [
    ("提示词1", "改进目标1"),
    ("提示词2", "改进目标2"),
    # ...
]

for prompt, improve in prompts:
    # 运行优化
    # ...
```

---

## 📝 代码修改说明

为了支持 apinexus.net API，我们对 promptimal 的源代码进行了以下修改：

### 修改 1: 支持自定义 API Base URL

**文件**: `promptimal/optimizer/main.py`

添加了对 `OPENAI_API_BASE` 环境变量的支持，允许使用自定义 API 服务。

### 修改 2: 支持自定义模型名称

**文件**: `promptimal/optimizer/utils.py`

添加了对 `OPENAI_MODEL` 环境变量的支持，允许使用自定义模型。

**注意**：这些修改是向后兼容的。如果不设置这些环境变量，promptimal 会使用默认的 OpenAI API 和 gpt-4o 模型。

**验证修改**：
运行 `examples/hello_world.py` 时，你应该看到：
- API 服务显示为 `https://apinexus.net/v1`
- 使用模型显示为 `gpt-5.2`
- 优化过程正常运行

---

## 📖 参考资源

### 官方文档

- **GitHub 仓库**: https://github.com/shobrook/promptimal
- **项目主页**: 查看官方文档了解更多信息

### 原始英文文档

- **Original English README**: [README_EN.md](./README_EN.md) - 原始官方文档，作为背景参考

### 相关概念

- **遗传算法**: 了解遗传算法的基本原理
- **提示词工程**: 学习如何编写高质量的提示词
- **LLM-as-Judge**: 了解如何使用 LLM 评估提示词质量

### 示例代码

- **Hello World**: `examples/hello_world.py` - 最简单的入门示例
- **测试脚本**: `test_promptimal.py` - 更完整的测试示例

---

## 🎓 学习建议

### 对于初学者

1. **从 Hello World 开始**：先运行 `examples/hello_world.py`，理解基本流程
   - 观察输出格式
   - 理解每个步骤的含义
   - 注意得分的变化

2. **理解参数**：尝试修改参数，观察结果变化
   - 修改 `num_iters`，观察迭代次数的影响
   - 修改 `population_size`，观察种群大小的影响
   - 修改 `threshold`，观察终止条件的影响

3. **阅读代码**：查看示例代码的注释，理解每一步的作用
   - 理解 API 配置
   - 理解优化流程
   - 理解输出格式

4. **实践练习**：尝试优化你自己的提示词
   - 使用更具体的改进目标
   - 尝试不同的参数组合
   - 观察优化结果

### 进阶学习

1. **理解遗传算法**：学习遗传算法的基本原理
2. **自定义评估函数**：创建自己的评估标准
3. **批量处理**：编写脚本批量优化提示词
4. **性能优化**：学习如何平衡优化质量和运行时间

---

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](./LICENSE) 文件。

---

## 🙏 致谢

- 感谢 [shobrook](https://github.com/shobrook) 创建了 promptimal 项目
- 感谢所有贡献者的努力

---

**最后更新**: 2025-12-30

**版本**: 基于 promptimal v2.0.0，适配 apinexus.net API

