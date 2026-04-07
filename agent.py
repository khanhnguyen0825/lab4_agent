import os
from typing import Annotated
from typing_extensions import TypedDict
from dotenv import load_dotenv

# Import LangGraph & LangChain
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver # QUAN TRỌNG: Dùng để nhớ lịch sử chat
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# Import tools từ file tools.py của bạn
from tools import search_flights, search_hotels, calculate_budget

load_dotenv()

# 1. Đọc System Prompt
with open("system_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

# 2. Khai báo State
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# 3. Khởi tạo LLM và Tools
tools_list = [search_flights, search_hotels, calculate_budget]
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm_with_tools = llm.bind_tools(tools_list)

# 4. Agent Node
def agent_node(state: AgentState):
    messages = state["messages"]
    # Đảm bảo System Prompt luôn nằm đầu danh sách tin nhắn
    if not any(isinstance(m, SystemMessage) for m in messages):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
    
    response = llm_with_tools.invoke(messages)
    
    # Logging
    if response.tool_calls:
        for tc in response.tool_calls:
            print(f"\n[Hệ thống] Gọi tool: {tc['name']}({tc['args']})")
    else:
        print("\n[Hệ thống] Trả lời trực tiếp")
        
    return {"messages": [response]}

# 5. Xây dựng Graph (Định nghĩa builder TRƯỚC khi compile)
builder = StateGraph(AgentState)

builder.add_node("agent", agent_node)
builder.add_node("tools", ToolNode(tools_list))

builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")

# KHỞI TẠO BỘ NHỚ VÀ BIÊN DỊCH
memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

# 6. Chat loop
if __name__ == "__main__":
    print("=" * 60)
    print("TravelBuddy – Trợ lý Du lịch Thông minh (Đã kích hoạt Bộ nhớ)")
    print(" Gõ 'quit', 'exit' hoặc 'q' để thoát")
    print("=" * 60)

    # config chứa thread_id để Agent phân biệt các cuộc hội thoại khác nhau
    config = {"configurable": {"thread_id": "session_1"}}

    while True:
        user_input = input("\nBạn: ").strip()
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Tạm biệt!")
            break
        
        if not user_input:
            continue

        print("\nTravelBuddy đang suy nghĩ...")
        
        # Truyền config vào invoke để Agent nhớ được context
        result = graph.invoke(
            {"messages": [HumanMessage(content=user_input)]}, 
            config=config
        )
        
        final_response = result["messages"][-1]
        print(f"\nTravelBuddy: {final_response.content}")