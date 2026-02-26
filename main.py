import os
import sys

from config import OPENAI_API_KEY, OPENAI_MODEL, VERBOSE
from agent import ReActAgent, SimpleAgent
from agent_langchain import LangChainAgent
from skills import ALL_SKILLS


def print_banner():
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                    🤖 Agent 助手                          ║
║                                                           ║
║  可用技能:                                                 ║
║    • web_search       - 网络搜索（Tavily/DuckDuckGo）     ║
║    • get_weather      - 和风天气查询                      ║
║    • calculator       - 数学计算                          ║
║    • get_time         - 获取当前时间                      ║
║    • python_repl      - 执行 Python 代码                  ║
║                                                           ║
║  命令:                                                     ║
║    /clear  - 清空对话记忆                                  ║
║    /skills - 显示技能详情                                  ║
║    /switch - 切换 Agent 类型                               ║
║    /exit   - 退出程序                                      ║
╚═══════════════════════════════════════════════════════════╝
"""
    print(banner)


def print_skills():
    print("\n📋 可用技能详情:\n")
    for name, skill in ALL_SKILLS.items():
        print(f"  🔧 {name}")
        print(f"     描述: {skill['description']}")
        print(f"     参数: {skill['args']}")
        print(f"     示例: {skill['example']}")
        print()


def check_config():
    if not OPENAI_API_KEY:
        print("⚠️  警告: 未配置 OPENAI_API_KEY")
        print("   请设置环境变量或在 .env 文件中配置")
        print()
        return False
    return True


def run_interactive():
    print_banner()
    
    if not check_config():
        print("请先配置 API Key 后再运行。")
        print("\n配置方法:")
        print("  1. 创建 .env 文件")
        print("  2. 添加以下内容:")
        print("     OPENAI_API_KEY=your_key")
        print("     TAVILY_API_KEY=your_key")
        print("     QWEATHER_API_KEY=your_key")
        return
    
    print(f"✅ 当前模型: {OPENAI_MODEL}")
    print("💬 开始对话 (输入问题后按回车)\n")
    
    use_langchain = True
    agent = LangChainAgent(verbose=VERBOSE)
    print("📌 当前使用: LangChain 版本 Agent")
    print("   输入 /switch 切换到手写版本\n")
    
    while True:
        try:
            user_input = input("👤 你: ").strip()
            
            if not user_input:
                continue
            
            if user_input == "/exit":
                print("\n👋 再见！")
                break
            
            if user_input == "/clear":
                agent.clear_memory()
                print("✅ 对话记忆已清空\n")
                continue
            
            if user_input in ["/skills", "/tools"]:
                print_skills()
                continue
            
            if user_input == "/switch":
                use_langchain = not use_langchain
                if use_langchain:
                    agent = LangChainAgent(verbose=VERBOSE)
                    print("✅ 已切换到: LangChain 版本 Agent\n")
                else:
                    agent = ReActAgent(verbose=VERBOSE)
                    print("✅ 已切换到: 手写版本 Agent\n")
                continue
            
            print("\n🤖 Agent: ", end="")
            response = agent.chat(user_input)
            print(response)
            print()
            
        except KeyboardInterrupt:
            print("\n\n👋 再见！")
            break
        except Exception as e:
            print(f"\n❌ 错误: {e}\n")


def run_demo():
    print_banner()
    
    if not check_config():
        return
    
    print("🎬 演示模式\n")
    
    agent = ReActAgent(verbose=True)
    
    demo_questions = [
        "现在几点了？",
        "北京今天天气怎么样？",
        "计算 123 乘以 456 等于多少", 
        
    ]
    
    for question in demo_questions:
        print(f"\n{'='*60}")
        print(f"👤 问题: {question}")
        print("="*60)
        
        response = agent.run(question)
        
        print(f"\n✅ 最终回答: {response}\n")
        
        agent.clear_memory()


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        run_demo()
    else:
        run_interactive()


if __name__ == "__main__":
    main()
