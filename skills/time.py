"""
时间技能模块

获取当前时间
"""

from datetime import datetime
from zoneinfo import ZoneInfo


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


SKILL_INFO = {
    "name": "get_time",
    "description": "获取当前时间",
    "args": {"timezone": "时区（可选，默认 Asia/Shanghai）"},
    "example": '{"timezone": "Asia/Shanghai"}'
}
