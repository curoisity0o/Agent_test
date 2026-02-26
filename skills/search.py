"""
搜索技能模块

提供网络搜索功能，支持 Tavily 和 DuckDuckGo
"""

import requests
from config import TAVILY_API_KEY


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


SKILL_INFO = {
    "name": "web_search",
    "description": "搜索网络获取信息（自动选择 Tavily 或 DuckDuckGo）",
    "args": {"query": "搜索关键词"},
    "example": '{"query": "Python 教程"}'
}
