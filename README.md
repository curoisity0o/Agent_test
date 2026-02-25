# Agent 助手项目

一个基于 ReAct 模式的智能 Agent 项目，支持工具调用。提供**手写版本**和 **LangChain 版本**两种实现，方便对比学习。

## 项目结构

```
Agent_test/
├── requirements.txt       # 依赖文件
├── config.py              # 配置管理（API Key 等）
├── tools.py               # 工具集（搜索、天气、计算等）
├── agent.py               # 手写版本 Agent（ReAct 模式）
├── agent_langchain.py     # LangChain 版本 Agent
├── main.py                # 主程序入口
├── compare_test.py        # 对比测试程序
├── .env.example           # 环境变量示例
└── README.md              # 本文件
```

## 功能特性

- **ReAct 推理模式**: Thought → Action → Observation 循环
- **多种工具支持**: 网络搜索、天气查询、数学计算、时间查询、Python 执行
- **双版本实现**: 手写版本 vs LangChain 版本，对比学习
- **对话记忆**: 支持多轮对话上下文
- **交互式界面**: 命令行交互模式

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/your-username/Agent_test.git
cd Agent_test
```

### 2. 创建虚拟环境

```bash
conda create -n agent python=3.10
conda activate agent
```

### 3. 安装依赖

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 4. 配置 API Key

复制示例文件并填入你的 API Key：

```bash
copy .env.example .env
```

编辑 `.env` 文件：

```env
# LLM API 配置（必需）
# 支持 OpenAI、DeepSeek 等兼容 OpenAI API 的服务
OPENAI_API_KEY=sk-your-api-key
OPENAI_API_BASE=https://api.deepseek.com/v1
OPENAI_MODEL=deepseek-chat

# Tavily 搜索 API（推荐）
# 获取地址: https://tavily.com/
TAVILY_API_KEY=tvly-your-tavily-key

# 和风天气 API（可选）
# 获取地址: https://dev.qweather.com/
QWEATHER_API_KEY=your-qweather-key
```

### 5. 运行程序

```bash
# 交互模式
python main.py

# 演示模式
python main.py --demo

# 对比测试（手写 vs LangChain）
python compare_test.py
```

## 可用工具

| 工具名称 | 功能描述 | 需要 API Key |
|---------|---------|-------------|
| `web_search` | 网络搜索（自动选择 Tavily 或 DuckDuckGo） | Tavily 可选 |
| `tavily_search` | Tavily 搜索（AI 优化，推荐） | ✅ 需要 |
| `duckduckgo_search` | DuckDuckGo 搜索（免费备用） | ❌ 不需要 |
| `get_weather` | 和风天气查询 | ✅ 需要 |
| `calculator` | 数学计算 | ❌ 不需要 |
| `get_time` | 获取当前时间 | ❌ 不需要 |
| `python_repl` | 执行 Python 代码 | ❌ 不需要 |

## 交互命令

在交互模式下可使用以下命令：

| 命令 | 功能 |
|------|------|
| `/clear` | 清空对话记忆 |
| `/tools` | 显示工具详情 |
| `/switch` | 切换 Agent 类型（手写/LangChain） |
| `/exit` | 退出程序 |

## 两个版本对比

| 特性 | 手写版本 | LangChain 版本 |
|------|---------|---------------|
| 文件 | `agent.py` | `agent_langchain.py` |
| 代码量 | ~300 行 | ~200 行 |
| 依赖 | openai | langchain, langgraph |
| ReAct模板 | 手写实现 | 框架内置 |
| 记忆管理 | 手写实现 | 框架内置 |
| 学习价值 | 理解底层原理 | 学习框架使用 |

## API 获取方式

### LLM API（必需）

**DeepSeek（推荐，性价比高）**
1. 访问 https://platform.deepseek.com/
2. 注册账号并获取 API Key
3. 免费额度：每月 500 万 tokens

**OpenAI**
1. 访问 https://platform.openai.com/
2. 注册账号并获取 API Key

### Tavily 搜索 API（推荐）
1. 访问 https://tavily.com/
2. 注册账号
3. 免费额度：1000 次/月

### 和风天气 API（可选）
1. 访问 https://dev.qweather.com/
2. 注册开发者账号
3. 免费额度：1000 次/天

## 使用示例

```
👤 你: 现在几点了？

🤖 Agent: 
Thought: 用户想知道当前时间，我可以使用 get_time 工具
Action: get_time
Action Input: {"timezone": "Asia/Shanghai"}
Observation: 当前时间: 2026-02-26 00:35:31 (Asia/Shanghai)

Final Answer: 现在是北京时间 2026年2月26日 00:35:31。

👤 你: 搜索一下 Python 是什么

🤖 Agent: 
Thought: 用户想了解Python，需要搜索网络
Action: web_search
Action Input: {"query": "Python 是什么"}
Observation: [搜索结果...]

Final Answer: Python是一种高级编程语言...

👤 你: 计算 123 乘以 456

🤖 Agent: 
Thought: 这是一个数学计算问题
Action: calculator
Action Input: {"expression": "123*456"}
Observation: 计算结果: 123 * 456 = 56088

Final Answer: 123 乘以 456 等于 56088。
```

## 扩展开发

### 添加新工具

在 `tools.py` 中添加：

```python
def my_new_tool(param: str) -> str:
    """工具描述"""
    # 实现逻辑
    return "结果"

TOOLS["my_new_tool"] = {
    "func": my_new_tool,
    "description": "工具功能描述",
    "args": {"param": "参数说明"},
    "example": '{"param": "示例值"}'
}
```

### 切换模型

修改 `.env` 文件：

```env
# 使用 DeepSeek
OPENAI_API_KEY=sk-xxx
OPENAI_API_BASE=https://api.deepseek.com/v1
OPENAI_MODEL=deepseek-chat

# 使用 OpenAI
OPENAI_API_KEY=sk-xxx
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_MODEL=gpt-4

# 使用本地模型 (Ollama)
OPENAI_API_KEY=ollama
OPENAI_API_BASE=http://localhost:11434/v1
OPENAI_MODEL=llama2
```

## 常见问题

**Q: 提示未配置 API Key？**
A: 确保 `.env` 文件在项目根目录，或已正确设置环境变量。

**Q: 工具调用失败？**
A: 检查对应的 API Key 是否正确配置，网络是否通畅。

**Q: 如何使用本地模型？**
A: 使用 Ollama 启动本地模型服务，然后设置 `OPENAI_API_BASE` 指向本地地址。

**Q: 搜索功能不工作？**
A: 如果有 Tavily API Key 会自动使用 Tavily；否则使用 DuckDuckGo（免费，无需 Key）。

## 技术栈

- Python 3.10+
- OpenAI API (兼容 DeepSeek 等)
- LangChain / LangGraph
- Tavily Search API
- 和风天气 API

## License

MIT License
