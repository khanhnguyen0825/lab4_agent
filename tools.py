import os
import requests
from langchain_core.tools import tool

# =================================================================
# MOCK DATA – Dữ liệu giả lập hệ thống du lịch
# =================================================================

FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1_450_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2_800_000, "class": "business"},
        {"airline": "VietJet Air", "departure": "08:30", "arrival": "09:50", "price": 890_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "11:00", "arrival": "12:20", "price": 1_200_000, "class": "economy"},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "10:00", "arrival": "12:15", "price": 1_350_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "16:00", "arrival": "18:15", "price": 1_100_000, "class": "economy"},
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1_600_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "07:30", "arrival": "09:40", "price": 950_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "12:00", "arrival": "14:10", "price": 1_300_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3_200_000, "class": "business"},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1_300_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "13:00", "arrival": "14:20", "price": 780_000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "15:00", "arrival": "16:00", "price": 650_000, "class": "economy"},
    ]
}

HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury", "stars": 5, "price_per_night": 1_800_000, "area": "Mỹ Khê", "rating": 4.5},
        {"name": "Sala Danang Beach", "stars": 4, "price_per_night": 1_200_000, "area": "Mỹ Khê", "rating": 4.3},
        {"name": "Fivitel Danang", "stars": 3, "price_per_night": 650_000, "area": "Sơn Trà", "rating": 4.1},
        {"name": "Memory Hostel", "stars": 2, "price_per_night": 250_000, "area": "Hải Châu", "rating": 4.6},
        {"name": "Christina's Homestay", "stars": 2, "price_per_night": 350_000, "area": "An Thượng", "rating": 4.7},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort", "stars": 5, "price_per_night": 3_500_000, "area": "Bãi Dài", "rating": 4.4},
        {"name": "Sol by Meliá", "stars": 4, "price_per_night": 1_500_000, "area": "Bãi Trường", "rating": 4.2},
        {"name": "Lahana Resort", "stars": 3, "price_per_night": 800_000, "area": "Dương Đông", "rating": 4.0},
        {"name": "9Station Hostel", "stars": 2, "price_per_night": 200_000, "area": "Dương Đông", "rating": 4.5},
    ],
    "Hồ Chí Minh": [
        {"name": "Rex Hotel", "stars": 5, "price_per_night": 2_800_000, "area": "Quận 1", "rating": 4.3},
        {"name": "Liberty Central", "stars": 4, "price_per_night": 1_400_000, "area": "Quận 1", "rating": 4.1},
        {"name": "Cochin Zen Hotel", "stars": 3, "price_per_night": 550_000, "area": "Quận 3", "rating": 4.4},
        {"name": "The Common Room", "stars": 2, "price_per_night": 180_000, "area": "Quận 1", "rating": 4.6},
    ]
}

# =================================================================
# LẬP TRÌNH CÔNG CỤ (TOOLS)
# =================================================================

# =================================================================
# CODE CŨ (Phiên bản MOCK DATA ban đầu của bài Lab)
# Đã comment lại theo yêu cầu cập nhật lên project real-time
# =================================================================
# @tool
# def search_flights(origin: str, destination: str) -> str:
#     """Tìm kiếm các chuyến bay giữa hai thành phố."""
#     flights = FLIGHTS_DB.get((origin, destination))
#     if not flights:
#         flights = FLIGHTS_DB.get((destination, origin))
#         if flights:
#             origin, destination = destination, origin 
#     if not flights: return f"Không tìm thấy chuyến bay từ {origin} đến {destination}."
#     result = f"Danh sách chuyến bay từ {origin} đến {destination}:\n"
#     for f in flights: result += f"- {f['airline']} ({f['class']}): {f['departure']} -> {f['arrival']} | Giá: {f['price']:,}đ\n"
#     return result

# =================================================================
# CODE MỚI: Phiên bản Tích hợp SERPAPI (Google Flights/Search thời gian thực)
# =================================================================
@tool
def search_flights(origin: str, destination: str) -> str:
    """Tìm kiếm vé máy bay ngoài đời thật giữa hai thành phố thông qua API Google."""
    api_key = os.getenv("SERPAPI_API_KEY")
    
    if not api_key or api_key.strip() == "":
        return "⚠️ CẢNH BÁO TỪ HỆ THỐNG: Tôi cần bạn cung cấp SERPAPI_API_KEY trong file .env để tra cứu vé máy bay thật trên mạng."
    
    try:
        import requests
        url = "https://serpapi.com/search"
        params = {
            "engine": "google",
            "q": f"giá vé máy bay từ {origin} đi {destination} hôm nay mới nhất",
            "hl": "vi",
            "gl": "vn",
            "api_key": api_key
        }
        res = requests.get(url, params=params, timeout=10)
        data = res.json()
        
        snippets = []
        if "answer_box" in data and "snippet" in data["answer_box"]:
            snippets.append(data["answer_box"]["snippet"])
            
        for item in data.get("organic_results", [])[:3]:
            title = item.get("title", "")
            snippet = item.get("snippet", "")
            if title or snippet:
                snippets.append(f"- Nguồn: {title} | Thông tin chi tiết: {snippet}")
                
        if not snippets:
            return f"Không tìm thấy thông tin vé máy bay từ {origin} đi {destination}. DỪNG TÌM KIẾM NGAY LẬP TỨC. Đừng gọi lại tool này nữa, hãy báo thẳng cho người dùng biết lỗi này!"
            
        return "🛫 Kết quả khảo sát vé máy bay thực tế cập nhật từ internet:\n" + "\n".join(snippets)
        
    except Exception as e:
         return f"Xảy ra lỗi khi gọi SerpApi: {str(e)}"

# CODE CŨ (MOCK DATA)
# @tool
# def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
#     """Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi đêm."""
#     hotels = HOTELS_DB.get(city)
#     if not hotels: return f"Không tìm thấy khách sạn tại {city}."
#     filtered_hotels = [h for h in hotels if h['price_per_night'] <= max_price_per_night]
#     filtered_hotels.sort(key=lambda x: x['rating'], reverse=True)
#     if not filtered_hotels: return f"Không."
#     result = f"Danh sách khách sạn tại {city} \n"
#     for h in filtered_hotels: result += f"- {h['name']} ({h['stars']} sao): {h['area']} | Giá: {h['price_per_night']:,}đ/đêm\n"
#     return result

# CODE MỚI: Phiên bản Tích hợp SERPAPI
@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """Tìm kiếm thông tin khách sạn thực tế cùng giá cả ngoài đời thông qua API Google."""
    api_key = os.getenv("SERPAPI_API_KEY")
    
    if not api_key or api_key.strip() == "":
        return "⚠️ CẢNH BÁO TỪ HỆ THỐNG: Tôi cần SERPAPI_API_KEY trong file .env để tra cứu phòng khách sạn thật trên mạng."
        
    try:
        import requests
        url = "https://serpapi.com/search"
        params = {
            "engine": "google",
            "q": f"Khách sạn tại {city} dưới {max_price_per_night} VND mỗi đêm booking hoặc agoda",
            "hl": "vi",
            "gl": "vn",
            "api_key": api_key
        }
        res = requests.get(url, params=params, timeout=10)
        data = res.json()
        
        snippets = []
        # Ưu tiên bóc rễ ra danh sách "Local pack" (phần hiển thị review khách sạn map của Google trang 1)
        if "local_results" in data and "places" in data["local_results"]:
            for place in data["local_results"]["places"][:4]:
                name = place.get("title", "Khách sạn")
                rating = place.get("rating", "Chưa có")
                price = place.get("price", "Đang cập nhật")
                snippets.append(f"- {name} | Giá tham khảo: {price} | Đánh giá: {rating} sao. (GHI CHÚ HỆ THỐNG: Nếu giá ghi là 'Đang cập nhật', AI hãy tự động giả định giá là {int(max_price_per_night * 0.8)} VND để tính tổng chi phí, TUYỆT ĐỐI KHÔNG GỌI LẠI TOOL TÌM KIẾM NỮA)")
        else:
            # Fallback đọc text từ trang web kèm theo Title để tránh mất tên khách sạn
            for item in data.get("organic_results", [])[:3]:
                title = item.get("title", "")
                snippet = item.get("snippet", "")
                if title or snippet: 
                    snippets.append(f"- Tên bài/Khách sạn: {title} | Thông tin: {snippet} (GHI CHÚ HỆ THỐNG: Nếu không thấy con số giá phòng cụ thể ở đây, hãy tự giả định tạm mức giá là {int(max_price_per_night * 0.8)} VND và đi tiếp, CẤM GỌI LẠI TOOL NÀY NỮA)")
                
        if not snippets:
            return f"Không tìm thấy khách sạn ở {city} với mức giá {max_price_per_night}. LỆNH TỪ HỆ THỐNG: DỪNG TÌM KIẾM NGAY LẬP TỨC. Không được gọi lại tool này với cùng một mức giá, hãy báo cho người dùng là ngân sách quá thấp để đặt phòng!"
            
        return f"🏨 Gợi ý phòng khách sạn thực tế tại {city} trên bản đồ:\n" + "\n".join(snippets)
        
    except Exception as e:
         return f"Xảy ra lỗi gọi SerpApi: {str(e)}"

@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """Tính toán ngân sách còn lại sau khi trừ các khoản chi phí (định dạng 'tên:số_tiền,tên:số_tiền')."""
    try:
        # Xử lý xóa khoảng trắng thừa để tránh lỗi parse
        expenses = expenses.replace(", ", ",").replace(": ", ":")
        items = expenses.split(',')
        
        total_expense = 0
        detail_lines = []
        
        for item in items:
            if not item or ':' not in item: continue
            name, price = item.split(':')
            # Loại bỏ các ký tự không phải số như 'đ' hoặc '.' trong giá tiền nếu AI lỡ truyền vào
            price_clean = "".join(filter(str.isdigit, price))
            price_val = int(price_clean)
            
            total_expense += price_val
            detail_lines.append(f"- {name.strip()}: {price_val:,}đ")

        remaining = total_budget - total_expense
        
        result = "--- BẢNG CHI PHÍ CHI TIẾT ---\n"
        result += "\n".join(detail_lines)
        result += f"\n---\n Tổng chi: {total_expense:,}đ"
        result += f"\n Ngân sách ban đầu: {total_budget:,}đ"
        
        if remaining < 0:
            result += f"\n CẢNH BÁO: Bạn đang thiếu {-remaining:,}đ! Vui lòng chọn dịch vụ rẻ hơn."
        else:
            result += f"\n Còn lại: {remaining:,}đ"
            
        return result
    except Exception as e:
        return f"Lỗi tính toán: {str(e)}. Vui lòng nhập đúng định dạng 'tên:số_tiền'."

@tool
def get_current_weather(city: str) -> str:
    """Lấy thông tin thời tiết hiện tại và đánh giá mức độ phù hợp đi du lịch tại một khu vực/thành phố thời gian thực."""
    try:
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            current = data['current_condition'][0]
            temp_c = current['temp_C']
            desc = current['weatherDesc'][0]['value']
            humidity = current['humidity']
            
            return_str = f"Thời tiết tại {city} hiện tại đang là {temp_c}°C, tình trạng: {desc}, độ ẩm {humidity}%.\n\nĐánh giá: "
            
            temp_val = int(temp_c)
            desc_lower = desc.lower()
            if any(rain_word in desc_lower for rain_word in ['rain', 'shower', 'thunder', 'storm', 'drizzle']):
                return_str += "Khu vực này đang có mưa hoặc thời tiết xấu. Không quá lý tưởng nếu đi dạo ngoài trời, hãy cân nhắc mang theo ô dù hoặc chọn các điểm tham quan trong nhà (bảo tàng, cafe)."
            elif temp_val > 35:
                return_str += "Thời tiết khá nóng bức. Nếu đi biển thì rất phù hợp, nhưng nếu đi tour ngoài trời bạn cần cẩn thận chống nắng và bù nước."
            elif 20 <= temp_val <= 32:
                return_str += "Thời tiết rất mát mẻ và lý tưởng cho các hoạt động du lịch, khám phá ngoài trời lúc này!"
            elif temp_val < 15:
                return_str += "Trời khá lạnh, bạn nên khuyên dùng khuyên mang theo áo khoác ấm khi đi lịch trình."
            else:
                return_str += "Thời tiết ở mức bình thường, đủ đẹp để lên lịch trình tham quan tự do."
                
            return return_str
        else:
            return f"Lỗi gọi API: Không thể lấy thông tin thời tiết cho {city} lúc này."
    except Exception as e:
        return f"Lỗi lấy thông tin thời tiết: {str(e)}"