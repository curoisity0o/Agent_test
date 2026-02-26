"""
计算技能模块

提供数学表达式计算功能
"""

import re


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


SKILL_INFO = {
    "name": "calculator",
    "description": "计算数学表达式，支持加减乘除和括号",
    "args": {"expression": "数学表达式"},
    "example": '{"expression": "123 * 456"}'
}
