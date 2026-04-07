from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn
import os

from agent import graph
from langchain_core.messages import HumanMessage

app = FastAPI(title="TravelBuddy Chatbot API")

# Serve the static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_index():
    """Tự động trả về file index.html khi truy cập trang chủ."""
    index_path = os.path.join("static", "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        return f.read()

class ChatRequest(BaseModel):
    message: str
    thread_id: str

class ChatResponse(BaseModel):
    response: str

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Xử lý hội thoại từ frontend chuyển đến LangGraph Agent"""
    config = {"configurable": {"thread_id": request.thread_id}}
    
    # Kích hoạt đồ thị agent
    result = graph.invoke(
        {"messages": [HumanMessage(content=request.message)]}, 
        config=config
    )
    
    # Lấy tin nhắn kết quả cuối cùng từ AI
    final_response = result["messages"][-1]
    return ChatResponse(response=final_response.content)

if __name__ == "__main__":
    print("🚀 Khởi chạy Web Server tại http://127.0.0.1:8000")
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
