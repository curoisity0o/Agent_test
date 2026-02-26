"""
技能模块

提供 Agent 可用的各种技能（工具）
"""

from skills.search import web_search, tavily_search, duckduckgo_search
from skills.weather import get_weather
from skills.calculator import calculator
from skills.time import get_time
from skills.python_repl import python_repl


ALL_SKILLS = {
    "web_search": {
        "func": web_search,
        "description": "搜索网络获取信息（自动选择 Tavily 或 DuckDuckGo）",
        "args": {"query": "搜索关键词"},
        "example": '{"query": "Python 教程"}'
    },
    "tavily_search": {
        "func": tavily_search,
        "description": "使用 Tavily 搜索网络（AI优化，需要 API Key）",
        "args": {"query": "搜索关键词"},
        "example": '{"query": "Python 教程"}'
    },
    "duckduckgo_search": {
        "func": duckduckgo_search,
        "description": "使用 DuckDuckGo 搜索网络（免费，无需 API Key）",
        "args": {"query": "搜索关键词"},
        "example": '{"query": "Python 教程"}'
    },
    "get_weather": {
        "func": get_weather,
        "description": "获取指定城市的实时天气信息",
        "args": {"city": "城市名称"},
        "example": '{"city": "北京"}'
    },
    "calculator": {
        "func": calculator,
        "description": "计算数学表达式，支持加减乘除和括号",
        "args": {"expression": "数学表达式"},
        "example": '{"expression": "123 * 456"}'
    },
    "get_time": {
        "func": get_time,
        "description": "获取当前时间",
        "args": {"timezone": "时区（可选，默认 Asia/Shanghai）"},
        "example": '{"timezone": "Asia/Shanghai"}'
    },
    "python_repl": {
        "func": python_repl,
        "description": "执行 Python 代码片段",
        "args": {"code": "Python 代码"},
        "example": '{"code": "result = sum(range(1, 101))"}'
    }
}


def get_skills_description() -> str:
    """生成技能描述文本"""
    descriptions = []
    for name, skill in ALL_SKILLS.items():
        desc = f"""{name}: {skill['description']}
  参数: {skill['args']}
  示例: {skill['example']}"""
        descriptions.append(desc)
    return "\n\n".join(descriptions)


def get_skill(name: str):
    """获取指定技能"""
    return ALL_SKILLS.get(name)
