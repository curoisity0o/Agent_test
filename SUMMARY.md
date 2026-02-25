# 项目总结

## 项目信息

- **项目名称**: Agent 助手
- **GitHub 地址**: https://github.com/curoisity0o/Agent_test
- **创建日期**: 2026-02-26

---

## 项目结构

```
Agent_test/
├── .env.example          # API Key 配置模板
├── .gitignore            # Git 忽略文件
├── README.md             # 项目文档
├── requirements.txt      # 依赖文件
├── config.py             # 配置管理
├── tools.py              # 工具集（7个工具）
├── agent.py              # 手写版本 Agent
├── agent_langchain.py    # LangChain 版本 Agent
├── main.py               # 主程序入口
├── compare_test.py       # 对比测试
├── test_agent.py         # Agent 测试
└── test_tools.py         # 工具测试
```

---

## 实现的功能

| 功能 | 说明 |
|------|------|
| **ReAct 推理** | Thought → Action → Observation 循环 |
| **网络搜索** | Tavily（推荐）/ DuckDuckGo（免费备用） |
| **天气查询** | 和风天气 API |
| **数学计算** | 支持加减乘除、括号、幂运算 |
| **时间查询** | 支持时区设置 |
| **Python 执行** | 执行 Python 代码片段 |
| **双版本实现** | 手写版本 + LangChain 版本对比学习 |

---

## 配置的 API

| API | 用途 | 获取地址 |
|-----|------|----------|
| DeepSeek | LLM 调用 | https://platform.deepseek.com/ |
| Tavily | 网络搜索 | https://tavily.com/ |
| 和风天气 | 天气查询 | https://dev.qweather.com/ |

---

## 使用方式

```bash
# 交互模式
python main.py

# 演示模式
python main.py --demo

# 对比测试
python compare_test.py
```

---

## 交互命令

| 命令 | 功能 |
|------|------|
| `/clear` | 清空对话记忆 |
| `/tools` | 显示工具详情 |
| `/switch` | 切换 Agent 类型（手写/LangChain） |
| `/exit` | 退出程序 |

---

## 两个版本对比

| 特性 | 手写版本 | LangChain 版本 |
|------|---------|---------------|
| 文件 | `agent.py` | `agent_langchain.py` |
| 代码量 | ~300 行 | ~200 行 |
| 依赖 | openai | langchain, langgraph |
| ReAct模板 | 手写实现 | 框架内置 |
| 记忆管理 | 手写实现 | 框架内置 |
| 学习价值 | 理解底层原理 | 学习框架使用 |

---

## 学习要点

1. **Agent 核心概念**: 感知 → 决策 → 行动
2. **ReAct 模式**: 推理与行动结合
3. **工具调用**: LLM 选择并执行工具
4. **LangChain 框架**: 现代化 Agent 开发方式
5. **提示工程**: 设计有效的 Agent 提示模板

---

## 后续可扩展方向

- [ ] 添加更多工具（邮件发送、数据库查询等）
- [ ] 实现多 Agent 协作
- [ ] 添加 Web UI 界面
- [ ] 支持流式输出
- [ ] 添加 Agent 记忆持久化
- [ ] 集成更多 LLM 模型

---

## 技术栈

- Python 3.10+
- OpenAI API (兼容 DeepSeek 等)
- LangChain / LangGraph
- Tavily Search API
- 和风天气 API
