import json
import re
from typing import List, Dict, Optional, Callable
from openai import OpenAI

from config import OPENAI_API_KEY, OPENAI_API_BASE, OPENAI_MODEL, MAX_ITERATIONS, VERBOSE
from tools import TOOLS, get_tools_description, execute_tool


class ReActAgent:
    """
    基于 ReAct 模式的智能 Agent
    
    ReAct = Reasoning + Acting
    思考 -> 行动 -> 观察 -> 思考 -> ...
    """
    
    SYSTEM_PROMPT = """你是一个智能助手，能够使用工具来帮助用户解决问题。
请始终用中文回答问题。
在回答之前，请仔细思考是否需要使用工具。
如果需要使用工具，请严格按照指定格式输出。"""

    REACT_TEMPLATE = """你可以使用以下工具：

{tools_description}

请严格按照以下格式回答问题：

Question: 用户的问题
Thought: 你的思考过程，分析需要做什么
Action: 工具名称（必须是上述工具之一）
Action Input: 工具输入参数（JSON格式）
Observation: 工具返回结果
... (Thought/Action/Action Input/Observation 可以重复多次)
Thought: 我现在知道最终答案了
Final Answer: 对原始问题的最终回答

重要规则：
1. 每次只能使用一个工具
2. Action 必须是上面列出的工具名称之一：{tool_names}
3. Action Input 必须是有效的 JSON 格式
4. 如果不需要使用工具，直接给出 Final Answer
5. 不要编造信息，如果工具返回错误，请如实告知用户

开始！

Question: {input}
{agent_scratchpad}"""

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
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.api_base
        )
        
        self.memory: List[Dict[str, str]] = []
        self.tool_names = list(TOOLS.keys())
    
    def _build_prompt(self, question: str, scratchpad: str = "") -> str:
        """构建完整的提示词"""
        return self.REACT_TEMPLATE.format(
            tools_description=get_tools_description(),
            tool_names=", ".join(self.tool_names),
            input=question,
            agent_scratchpad=scratchpad
        )
    
    def _parse_response(self, response: str) -> Dict:
        """解析 LLM 响应，提取 Thought、Action、Action Input、Final Answer"""
        result = {
            "thought": "",
            "action": None,
            "action_input": None,
            "final_answer": None
        }
        
        thought_match = re.search(r"Thought:\s*(.+?)(?=\n(?:Action|Final)|$)", response, re.DOTALL)
        if thought_match:
            result["thought"] = thought_match.group(1).strip()
        
        action_match = re.search(r"Action:\s*(\w+)", response)
        if action_match:
            result["action"] = action_match.group(1).strip()
        
        action_input_match = re.search(r"Action Input:\s*(\{.+?\})", response, re.DOTALL)
        if action_input_match:
            try:
                result["action_input"] = json.loads(action_input_match.group(1))
            except json.JSONDecodeError:
                result["action_input"] = action_input_match.group(1).strip()
        
        final_answer_match = re.search(r"Final Answer:\s*(.+?)$", response, re.DOTALL)
        if final_answer_match:
            result["final_answer"] = final_answer_match.group(1).strip()
        
        return result
    
    def _call_llm(self, messages: List[Dict[str, str]]) -> str:
        """调用 LLM"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"LLM 调用错误: {str(e)}"
    
    def run(self, question: str, max_iterations: int = MAX_ITERATIONS) -> str:
        """
        运行 Agent 处理问题
        
        Args:
            question: 用户问题
            max_iterations: 最大迭代次数
        
        Returns:
            最终回答
        """
        scratchpad = ""
        
        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT}
        ]
        
        for memory in self.memory[-5:]:
            messages.append(memory)
        
        for iteration in range(max_iterations):
            prompt = self._build_prompt(question, scratchpad)
            
            current_messages = messages + [{"role": "user", "content": prompt}]
            
            if self.verbose:
                print(f"\n{'='*50}")
                print(f"[迭代 {iteration + 1}/{max_iterations}]")
            
            response = self._call_llm(current_messages)
            
            if self.verbose:
                print(f"[LLM 响应]\n{response}")
            
            parsed = self._parse_response(response)
            
            if parsed["final_answer"]:
                self.memory.append({"role": "user", "content": question})
                self.memory.append({"role": "assistant", "content": parsed["final_answer"]})
                return parsed["final_answer"]
            
            if parsed["action"] and parsed["action"] in TOOLS:
                if self.verbose:
                    print(f"\n[执行工具] {parsed['action']}")
                    print(f"[工具输入] {parsed['action_input']}")
                
                observation = execute_tool(parsed["action"], parsed["action_input"])
                
                if self.verbose:
                    print(f"[工具输出] {observation}")
                
                scratchpad += f"\nThought: {parsed['thought']}\n"
                scratchpad += f"Action: {parsed['action']}\n"
                scratchpad += f"Action Input: {json.dumps(parsed['action_input'], ensure_ascii=False)}\n"
                scratchpad += f"Observation: {observation}\n"
            else:
                scratchpad += f"\nThought: {parsed['thought']}\n"
                if parsed["action"]:
                    scratchpad += f"Action: {parsed['action']}\n"
                    scratchpad += f"Observation: 错误 - 未知工具 '{parsed['action']}'，可用工具: {', '.join(self.tool_names)}\n"
        
        return "抱歉，我无法在有限的步骤内完成这个任务。请尝试简化您的问题。"
    
    def chat(self, user_input: str) -> str:
        """
        对话接口，保持上下文记忆
        
        Args:
            user_input: 用户输入
        
        Returns:
            Agent 回复
        """
        return self.run(user_input)
    
    def clear_memory(self):
        """清空对话记忆"""
        self.memory = []


class SimpleAgent:
    """
    简化版 Agent，使用 Function Calling
    适用于支持 Function Calling 的模型
    """
    
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
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.api_base
        )
        
        self.memory: List[Dict[str, str]] = []
        self.tools_schema = self._build_tools_schema()
    
    def _build_tools_schema(self) -> List[Dict]:
        """构建 OpenAI Function Calling 格式的工具 schema"""
        return [
            {
                "type": "function",
                "function": {
                    "name": name,
                    "description": tool["description"],
                    "parameters": {
                        "type": "object",
                        "properties": {
                            k: {"type": "string", "description": v}
                            for k, v in tool["args"].items()
                        },
                        "required": list(tool["args"].keys())
                    }
                }
            }
            for name, tool in TOOLS.items()
        ]
    
    def run(self, question: str) -> str:
        """运行 Agent"""
        messages = [
            {"role": "system", "content": "你是一个智能助手，请使用中文回答问题。"}
        ] + self.memory[-10:] + [{"role": "user", "content": question}]
        
        for _ in range(MAX_ITERATIONS):
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools_schema,
                tool_choice="auto"
            )
            
            message = response.choices[0].message
            
            if message.content:
                if self.verbose:
                    print(f"[回复] {message.content}")
            
            if message.tool_calls:
                messages.append(message)
                
                for tool_call in message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)
                    
                    if self.verbose:
                        print(f"\n[调用工具] {tool_name}({tool_args})")
                    
                    result = execute_tool(tool_name, tool_args)
                    
                    if self.verbose:
                        print(f"[工具结果] {result}")
                    
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result
                    })
            else:
                self.memory.append({"role": "user", "content": question})
                self.memory.append({"role": "assistant", "content": message.content})
                return message.content or "抱歉，我无法回答这个问题。"
        
        return "抱歉，处理超时。"
    
    def chat(self, user_input: str) -> str:
        """对话接口"""
        return self.run(user_input)
    
    def clear_memory(self):
        """清空记忆"""
        self.memory = []
