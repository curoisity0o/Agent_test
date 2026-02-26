from agent_langchain import LangChainAgent

print("=" * 50)
print("LangChain 版本 Agent")
print("=" * 50)

agent = LangChainAgent(verbose=True)

while True:
    try:
        user_input = input("\n👤 你: ").strip()
        
        if not user_input:
            continue
        
        if user_input in ["/exit", "exit", "quit"]:
            print("👋 再见！")
            break
        
        if user_input == "/clear":
            agent.clear_memory()
            print("✅ 对话记忆已清空")
            continue
        
        print("\n🤖 Agent: ", end="")
        response = agent.chat(user_input)
        print(response)
        
    except KeyboardInterrupt:
        print("\n👋 再见！")
        break
    except Exception as e:
        print(f"\n❌ 错误: {e}")
