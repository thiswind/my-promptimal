# Promptimal 示例代码

本目录包含 promptimal 的使用示例，适合学习和参考。

## 示例列表

### hello_world.py

最简单的入门示例，展示如何使用 promptimal 优化提示词。

**运行方法**：
```bash
cd promptimal
conda activate base
export OPENAI_API_KEY="your_api_key"
export OPENAI_API_BASE="https://apinexus.net/v1"
export OPENAI_MODEL="gpt-5.2"
python examples/hello_world.py
```

**特点**：
- 代码简单清晰，有详细的中文注释
- 使用 apinexus.net API
- 适合初学者学习

**预期输出**：
- 显示 API 配置信息
- 显示优化过程的每个步骤
- 显示最佳提示词和得分

## 注意事项

1. **环境变量**：运行前需要设置正确的环境变量
2. **Python 路径**：如果从 examples 目录运行，代码会自动处理路径问题
3. **API 费用**：每次运行会进行多次 API 调用，请注意费用

## 更多示例

更多示例代码正在开发中，敬请期待。

