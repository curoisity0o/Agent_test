"""
对比测试：手写 Agent vs LangChain Agent

运行方式：
  python compare_test.py          # 交互模式
  python compare_test.py --demo   # 演示模式
"""

import sys
import time
from config import OPENAI_API_KEY, OPENAI_MODEL, VERBOSE
from agent import ReActAgent
from agent_langchain import LangChainAgent


def print_banner():
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║              🔄 Agent 对比测试                                 ║
║                                                               ║
║   手写版本 (agent.py)          vs      LangChain 版本         ║
║   - 完全自主实现                       - 框架封装              ║
║   - 理解底层原理                       - 快速开发              ║
║   - 约 300 行代码                      - 约 100 行代码         ║
║                                                               ║
║   命令: /compare /demo /exit                                  ║
╚═══════════════════════════════════════════════════════════════╝
"""
    print(banner)


def compare_single_question(question: str):
    """对比单个问题的回答"""
    print(f"\n{'='*70}")
    print(f"📝 问题: {question}")
    print("="*70)
    
    print("\n" + "─"*35 + " 手写版本 " + "─"*35)
    start_time = time.time()
    
    hand_agent = ReActAgent(verbose=False)
    hand_result = hand_agent.run(question)
    hand_time = time.time() - start_time
    
    print(f"\n✅ 回答: {hand_result}")
    print(f"⏱️  耗时: {hand_time:.2f}秒")
    
    print("\n" + "─"*35 + " LangChain版本 " + "─"*33)
    start_time = time.time()
    
    lc_agent = LangChainAgent(verbose=False)
    lc_result = lc_agent.run(question)
    lc_time = time.time() - start_time
    
    print(f"\n✅ 回答: {lc_result}")
    print(f"⏱️  耗时: {lc_time:.2f}秒")
    
    print("\n" + "="*70)
    print(f"📊 对比结果:")
    print(f"   手写版本耗时: {hand_time:.2f}秒")
    print(f"   LangChain版本耗时: {lc_time:.2f}秒")
    print(f"   差异: {abs(hand_time - lc_time):.2f}秒")
    print("="*70)


def run_demo():
    """演示模式"""
    print_banner()
    
    if not OPENAI_API_KEY:
        print("⚠️  请先配置 OPENAI_API_KEY")
        return
    
    demo_questions = [
        "现在几点了？",
        "北京今天天气怎么样？",
        "计算 123 乘以 456 等于多少",
        "搜索一下 Python 是什么",
    ]
    
    for question in demo_questions:
        compare_single_question(question)
        print("\n按回车继续下一个问题...")
        input()


def run_interactive():
    """交互模式"""
    print_banner()
    
    if not OPENAI_API_KEY:
        print("⚠️  请先配置 OPENAI_API_KEY")
        return
    
    print(f"✅ 当前模型: {OPENAI_MODEL}")
    print("💬 输入问题进行对比测试\n")
    
    hand_agent = ReActAgent(verbose=VERBOSE)
    lc_agent = LangChainAgent(verbose=VERBOSE)
    
    while True:
        try:
            user_input = input("👤 你: ").strip()
            
            if not user_input:
                continue
            
            if user_input == "/exit":
                print("\n👋 再见！")
                break
            
            if user_input == "/demo":
                run_demo()
                continue
            
            if user_input == "/compare":
                print("\n📊 两个版本对比:")
                print("   手写版本: 完全自主实现，理解底层原理")
                print("   LangChain: 框架封装，快速开发")
                continue
            
            compare_single_question(user_input)
            
        except KeyboardInterrupt:
            print("\n\n👋 再见！")
            break


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        run_demo()
    else:
        run_interactive()


if __name__ == "__main__":
    main()
