"""
Python 执行技能模块

执行 Python 代码片段
"""


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


SKILL_INFO = {
    "name": "python_repl",
    "description": "执行 Python 代码片段",
    "args": {"code": "Python 代码"},
    "example": '{"code": "result = sum(range(1, 101))"}'
}
