# TravelBuddy - Trợ lý Du lịch Thông minh

TravelBuddy là một chatbot thông minh dựa trên AI được phát triển bằng **LangChain**, **LangGraph** (Agentic AI) và **FastAPI**. Ứng dụng hoạt động như một tư vấn viên du lịch cá nhân, giúp bạn tìm vé máy bay, khách sạn và tính toán ngân sách tối ưu cho chuyến du lịch của mình.


---

## Tính năng 

- **Agentic Architecture:** Xây dựng với LangGraph, cho phép AI tự động phân tích và gọi chuỗi các công cụ (Tool Chaining) theo logic phức tạp.
- **Bộ nhớ thông minh:** Duy trì ngữ cảnh đoạn hội thoại liên tục nhờ LangGraph Memory.
- **Tích hợp Custom Tools:**
  - `search_flights`: Tìm kiếm vé máy bay nội địa theo ngày, giờ thật.
  - `search_hotels`: Check khách sạn cùng rating ở các điểm đến.
  - `calculate_budget`: Tự động cộng - trừ các khoản để cân đối ngân sách tổng quát cho từng người dùng.
- **Web UI:** Glassmorphism, Dark Mode.

---

## Cấu trúc thư mục

```text
├── .env                  # Tệp cấu hình chứa OPENAI_API_KEY
├── agent.py              # Xây dựng Logic LangGraph, Workflow Agent và chạy qua Terminal
├── app.py                # Server FastAPI cung cấp API và Render Frontend Web
├── tools.py              # Định nghĩa các Tools (hàm) xử lý cho Agent (chuyến bay, khách sạn, ngân sách)
├── system_prompt.txt     # Hệ thống System Instructions nghiêm ngặt dành cho Persona của TravelBuddy
├── test_results.md       # Lưu lại các Unit test/Use cases kiểm thử hiệu năng bot
└── static/
    ├── index.html        # Giao diện hộp thoại Frontend (HTML + JS)
    └── style.css         # Các rules Premium CSS để làm đẹp giao diện AI
```

---

## Hướng dẫn cài đặt

### 1. Yêu cầu hệ thống
- Python 3.9+
- Tài khoản OpenAI API Key có Credit.

### 2. Cài đặt chi tiết

Clone dự án về máy:
```bash
git clone https://github.com/your-username/lab4_agent.git
cd lab4_agent
```

Tạo và kích hoạt môi trường ảo (Virtual Environment):
```bash
python -m venv venv
# Kích hoạt trên Windows:
venv\Scripts\activate
# Kích hoạt trên Mac/Linux:
source venv/bin/activate
```

Cài đặt các gói thư viện cần thiết:
```bash
pip install langchain langchain-openai langgraph fastapi uvicorn pydantic python-dotenv
```

Tạo cấu hình môi trường `.env`: Đổi tên file hoặc tạo file `.env` chứa API keys của bạn:
```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## Công nghệ sử dụng
- [LangChain](https://python.langchain.com/) / [LangGraph](https://langchain-ai.github.io/langgraph/) - Quản trị và triển khai framework AI.
- [FastAPI](https://fastapi.tiangolo.com/) - Xây dựng Backend tốc độ cao.
- Vanilla HTML/JS/CSS cho Frontend siêu mượt.
- OpenAI `gpt-4o-mini` cho phân tích ngôn ngữ tự nhiên.
