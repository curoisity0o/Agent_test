"""
LangChain 版本的 Agent（使用 LangGraph）

LangChain 新版本推荐使用 LangGraph 构建 Agent
这是更现代、更灵活的实现方式
"""

from typing import Optional, List
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.prebuilt import create_react_agent
from langchain.memory import ConversationSummaryMemory

from config import OPENAI_API_KEY, OPENAI_API_BASE, OPENAI_MODEL, MAX_ITERATIONS, VERBOSE
from skills import web_search, get_weather, calculator, get_time, python_repl


@tool
def web_search_tool(query: str) -> str:
    """搜索网络获取信息。输入应该是搜索关键词。例如: 'Python 教程'"""
    return web_search(query)


@tool
def get_weather_tool(city: str) -> str:
    """获取指定城市的实时天气信息。输入应该是城市名称。例如: '北京'"""
    return get_weather(city)


@tool
def calculator_tool(expression: str) -> str:
    """计算数学表达式。输入应该是数学表达式。例如: '123 * 456'"""
    return calculator(expression)


@tool
def get_time_tool(timezone: str = "Asia/Shanghai") -> str:
    """获取当前时间。输入应该是时区名称，如 'Asia/Shanghai'，也可以不输入使用默认时区"""
    return get_time(timezone)


@tool
def python_repl_tool(code: str) -> str:
    """执行 Python 代码片段。输入应该是 Python 代码字符串"""
    return python_repl(code)


def create_tools() -> List:
    """创建工具列表"""
    return [
        web_search_tool,
        get_weather_tool,
        calculator_tool,
        get_time_tool,
        python_repl_tool
    ]


class LangChainAgent:
    """
    基于 LangGraph 的 ReAct Agent
    
    使用 LangGraph (LangChain 新版推荐方式) 构建 Agent
    使用 ConversationSummaryMemory 自动摘要长对话
    """
    
    SYSTEM_PROMPT = """你是一个智能助手，能够使用工具来帮助用户解决问题。
请始终用中文回答问题。
在回答之前，请仔细思考是否需要使用工具。"""
    
    MAX_MEMORY_TURNS = 10
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        model: Optional[str] = None,
        verbose: bool = VERBOSE
    ):
        self.api_key = api_key or OPENAI_API_KEY
        self.api_base = api_base or OPENAI_API_BASE
        self.model = model or OPENAI_MODEL
        self.verbose = verbose
        
        self.llm = ChatOpenAI(
            model=self.model,
            api_key=self.api_key,
            base_url=self.api_base,
            temperature=0.7
        )
        
        self.tools = create_tools()
        
        self.agent = create_react_agent(
            self.llm,
            self.tools
        )
        
        self.memory: List = []
        self.summary_memory = ConversationSummaryMemory(
            llm=self.llm,
            memory_key="chat_history",
            return_messages=True,
            human_prefix="用户",
            ai_prefix="助手"
        )
    
    def run(self, question: str) -> str:
        """运行 Agent 处理问题"""
        try:
            messages = [SystemMessage(content=self.SYSTEM_PROMPT)]
            
            if self.summary_memory.buffer:
                messages.append(SystemMessage(
                    content=f"之前的对话摘要: {self.summary_memory.buffer}"
                ))
            
            messages.extend(self.memory[-self.MAX_MEMORY_TURNS:])
            messages.append(HumanMessage(content=question))
            
            result = self.agent.invoke({"messages": messages})
            
            last_message = result["messages"][-1]
            
            self.memory.append(HumanMessage(content=question))
            self.memory.append(last_message)
            
            self.summary_memory.save_context(
                {"input": question},
                {"output": last_message.content}
            )
            
            if self.verbose and len(self.memory) > self.MAX_MEMORY_TURNS:
                print(f"[记忆管理] 已自动摘要对话历史")
            
            return last_message.content
        except Exception as e:
            return f"执行出错: {str(e)}"
    
    def chat(self, user_input: str) -> str:
        """对话接口"""
        return self.run(user_input)
    
    def clear_memory(self):
        """清空对话记忆"""
        self.memory = []
        self.summary_memory.clear()
    
    def get_memory_summary(self) -> str:
        """获取对话摘要"""
        return self.summary_memory.buffer


class LangChainAgentSimple:
    """
    简化版 LangChain Agent
    
    直接使用 LLM 绑定工具的方式，更简单直接
    使用滑动窗口管理记忆
    """
    
    SYSTEM_PROMPT = """你是一个智能助手，请使用中文回答问题。你可以使用工具来帮助解决问题。"""
    
    MAX_MEMORY_TURNS = 10
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        model: Optional[str] = None,
        verbose: bool = VERBOSE
    ):
        self.api_key = api_key or OPENAI_API_KEY
        self.api_base = api_base or OPENAI_API_BASE
        self.model = model or OPENAI_MODEL
        self.verbose = verbose
        
        self.llm = ChatOpenAI(
            model=self.model,
            api_key=self.api_key,
            base_url=self.api_base,
            temperature=0.7
        )
        
        self.tools = create_tools()
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        
        self.memory: List = []
    
    def run(self, question: str) -> str:
        """运行 Agent"""
        try:
            messages = [SystemMessage(content=self.SYSTEM_PROMPT)]
            messages.extend(self.memory[-self.MAX_MEMORY_TURNS:])
            messages.append(HumanMessage(content=question))
            
            response = self.llm_with_tools.invoke(messages)
            
            if response.tool_calls:
                messages.append(response)
                
                for tool_call in response.tool_calls:
                    tool_name = tool_call["name"]
                    tool_args = tool_call["args"]
                    
                    tool_func = {
                        "web_search_tool": web_search,
                        "get_weather_tool": get_weather,
                        "calculator_tool": calculator,
                        "get_time_tool": get_time,
                        "python_repl_tool": python_repl
                    }.get(tool_name)
                    
                    if tool_func:
                        if self.verbose:
                            print(f"[调用工具] {tool_name}({tool_args})")
                        
                        result = tool_func(**tool_args)
                        
                        from langchain_core.messages import ToolMessage
                        messages.append(ToolMessage(
                            content=result,
                            tool_call_id=tool_call["id"]
                        ))
                
                final_response = self.llm_with_tools.invoke(messages)
                
                self.memory.append(HumanMessage(content=question))
                self.memory.append(AIMessage(content=final_response.content))
                
                return final_response.content
            
            self.memory.append(HumanMessage(content=question))
            self.memory.append(AIMessage(content=response.content))
            
            return response.content
        except Exception as e:
            return f"执行出错: {str(e)}"
    
    def chat(self, user_input: str) -> str:
        """对话接口"""
        return self.run(user_input)
    
    def clear_memory(self):
        """清空记忆"""
        self.memory = []
