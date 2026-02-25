import requests
import json
import re
from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo

from config import TAVILY_API_KEY, QWEATHER_API_KEY


def tavily_search(query: str, count: int = 5) -> str:
    """
    使用 Tavily API 搜索网络信息（推荐用于 Agent）
    
    Args:
        query: 搜索关键词
        count: 返回结果数量
    
    Returns:
        搜索结果摘要
    """
    if not TAVILY_API_KEY:
        return "错误: 未配置 TAVILY_API_KEY，请在环境变量中设置"
    
    url = "https://api.tavily.com/search"
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "search_depth": "basic",
        "max_results": count
    }
    
    try:
        response = requests.post(url, json=payload, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        results = []
        for i, item in enumerate(data.get("results", [])[:count], 1):
            results.append(f"{i}. {item['title']}\n   {item['content'][:200]}...\n   链接: {item['url']}")
        
        if not results:
            return f"未找到关于 '{query}' 的搜索结果"
        
        return f"搜索 '{query}' 的结果:\n\n" + "\n\n".join(results)
    
    except requests.exceptions.RequestException as e:
        return f"搜索出错: {str(e)}"


def duckduckgo_search(query: str, count: int = 5) -> str:
    """
    使用 DuckDuckGo 搜索网络信息（免费，无需 API Key）
    
    Args:
        query: 搜索关键词
        count: 返回结果数量
    
    Returns:
        搜索结果摘要
    """
    try:
        from ddgs import DDGS
        
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=count))
        
        if not results:
            return f"未找到关于 '{query}' 的搜索结果"
        
        output = []
        for i, r in enumerate(results, 1):
            output.append(f"{i}. {r['title']}\n   {r['body'][:200]}...\n   链接: {r['href']}")
        
        return f"搜索 '{query}' 的结果:\n\n" + "\n\n".join(output)
    
    except ImportError:
        return "错误: 未安装 ddgs，请运行: pip install ddgs"
    except Exception as e:
        return f"搜索出错: {str(e)}"


def web_search(query: str, count: int = 5) -> str:
    """
    网络搜索（优先使用 Tavily，失败则使用 DuckDuckGo）
    
    Args:
        query: 搜索关键词
        count: 返回结果数量
    
    Returns:
        搜索结果摘要
    """
    if TAVILY_API_KEY:
        return tavily_search(query, count)
    else:
        return duckduckgo_search(query, count)


def get_weather(city: str) -> str:
    """
    使用和风天气 API 获取城市天气信息
    
    Args:
        city: 城市名称，如 "北京"
    
    Returns:
        天气信息描述
    """
    if not QWEATHER_API_KEY:
        return "错误: 未配置 QWEATHER_API_KEY，请在环境变量中设置"
    
    try:
        geo_url = "https://geoapi.qweather.com/v2/city/lookup"
        geo_params = {"location": city, "key": QWEATHER_API_KEY}
        geo_response = requests.get(geo_url, params=geo_params, timeout=10)
        geo_data = geo_response.json()
        
        if geo_data.get("code") != "200":
            return f"未找到城市 '{city}'，请检查城市名称"
        
        location_id = geo_data["location"][0]["id"]
        location_name = geo_data["location"][0]["name"]
        
        weather_url = "https://devapi.qweather.com/v7/weather/now"
        weather_params = {"location": location_id, "key": QWEATHER_API_KEY}
        weather_response = requests.get(weather_url, params=weather_params, timeout=10)
        weather_data = weather_response.json()
        
        if weather_data.get("code") != "200":
            return f"获取天气信息失败"
        
        now = weather_data["now"]
        
        result = f"""{location_name} 当前天气:
天气: {now['text']}
温度: {now['temp']}°C
体感温度: {now['feelsLike']}°C
风向: {now['windDir']} {now['windScale']}级
湿度: {now['humidity']}%
能见度: {now['vis']}公里
更新时间: {weather_data['updateTime']}"""
        
        return result
    
    except requests.exceptions.RequestException as e:
        return f"获取天气出错: {str(e)}"


def calculator(expression: str) -> str:
    """
    计算数学表达式
    
    Args:
        expression: 数学表达式，如 "123 * 456"
    
    Returns:
        计算结果
    """
    try:
        allowed_chars = r'[\d\+\-\*\/\(\)\.\s\%\*\*]'
        if not re.match(f'^{allowed_chars}+$', expression):
            return "错误: 表达式包含不允许的字符"
        
        result = eval(expression)
        return f"计算结果: {expression} = {result}"
    except Exception as e:
        return f"计算错误: {str(e)}"


def get_time(timezone: str = "Asia/Shanghai") -> str:
    """
    获取当前时间
    
    Args:
        timezone: 时区，默认 "Asia/Shanghai"
    
    Returns:
        当前时间字符串
    """
    try:
        now = datetime.now(ZoneInfo(timezone))
        return f"当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')} ({timezone})"
    except Exception as e:
        return f"获取时间出错: {str(e)}"


def python_repl(code: str) -> str:
    """
    执行 Python 代码
    
    Args:
        code: Python 代码字符串
    
    Returns:
        执行结果
    """
    try:
        local_vars = {}
        exec(code, {"__builtins__": __builtins__}, local_vars)
        
        if "result" in local_vars:
            return f"执行结果: {local_vars['result']}"
        return "代码执行成功（无返回值）"
    except Exception as e:
        return f"执行错误: {str(e)}"


TOOLS = {
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


def get_tools_description() -> str:
    """生成工具描述文本"""
    descriptions = []
    for name, tool in TOOLS.items():
        desc = f"""{name}: {tool['description']}
  参数: {tool['args']}
  示例: {tool['example']}"""
        descriptions.append(desc)
    return "\n\n".join(descriptions)


def execute_tool(tool_name: str, tool_input: str) -> str:
    """执行指定工具"""
    if tool_name not in TOOLS:
        return f"错误: 未知工具 '{tool_name}'"
    
    tool = TOOLS[tool_name]
    
    try:
        if isinstance(tool_input, str):
            try:
                args = json.loads(tool_input)
            except json.JSONDecodeError:
                args = {"query": tool_input, "city": tool_input, "expression": tool_input, 
                        "timezone": tool_input, "code": tool_input}
        else:
            args = tool_input
        
        return tool["func"](**args)
    except Exception as e:
        return f"工具执行错误: {str(e)}"
