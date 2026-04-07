# TravelBuddy - Trợ lý Du lịch Thông minh

TravelBuddy là một chatbot thông minh dựa trên AI được phát triển bằng **LangChain**, **LangGraph** (Agentic AI) và **FastAPI**. Ứng dụng hoạt động như một tư vấn viên du lịch cá nhân, giúp bạn tìm vé máy bay, khách sạn và tính toán ngân sách tối ưu cho chuyến du lịch của mình.


---

## Tính năng 

- **Agentic Architecture:** Xây dựng với LangGraph, cho phép AI tự động phân tích và gọi chuỗi các công cụ (Tool Chaining) theo logic phức tạp.
- **Bộ nhớ thông minh:** Duy trì ngữ cảnh đoạn hội thoại liên tục nhờ LangGraph Memory.
- **Tích hợp Real-time Tools (Kết nối Internet):**
  - `search_flights` & `search_hotels`: Tạm biệt mô hình dữ liệu giả (mock data), dự án nay đã được tích hợp thuật toán **Google Search (thông qua SerpAPI)** để lấy kết quả vé máy bay thật và check phòng khách sạn kèm Rating của Google Local theo thời gian thực.
  - `get_current_weather`: Kết nối `wttr.in` xử lý thông tin thời tiết điểm đến và đưa lời khuyên lịch trình.
  - `calculate_budget`: Tính toán ngân sách tổng quát cho chuyến đi, ước lượng thuế phí cho vé máy bay (nếu có) và phân bổ ngân sách riêng cho các hoạt động vui chơi trước khi gợi ý phòng khách sạn để người dùng có mức giá hợp lý.
- **Web UI:** Giao diện AI Chatbot với Glassmorphism, Dark Mode.

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
pip install langchain langchain-openai langgraph fastapi uvicorn pydantic python-dotenv requests google-search-results
```

Tạo cấu hình môi trường `.env`: Đổi tên file hoặc tạo file `.env` chứa API keys của bạn:
```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
SERPAPI_API_KEY=dán-key-serpapi-của-bạn-vào-đây # Đăng ký tài khoản free tại serpapi.com
```

## Công nghệ sử dụng
- [LangChain](https://python.langchain.com/) / [LangGraph](https://langchain-ai.github.io/langgraph/) - Quản trị và triển khai framework AI.
- [FastAPI](https://fastapi.tiangolo.com/) - Xây dựng Backend tốc độ cao.
- Vanilla HTML/JS/CSS cho Frontend siêu mượt.
- OpenAI `gpt-4o-mini` cho phân tích ngôn ngữ tự nhiên.
