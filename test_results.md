# TravelBuddy Test Results (mock data)

## Test 1: Direct answer

**Bạn:** Xin chào ! Tôi muốn đi du lịch nhưng chưa biết đi đâu

*TravelBuddy đang suy nghĩ...*

> **[Hệ thống]** Trả lời trực tiếp

**TravelBuddy:** Chào bạn! Thật tuyệt khi bạn muốn đi du lịch! Bạn có thể cho mình biết thêm một chút về sở thích của bạn không? Bạn thích biển, núi, hay thành phố? Và bạn có ngân sách dự kiến cho chuyến đi này không?

---

## Test 2: Single tool call

**Bạn:** Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng

*TravelBuddy đang suy nghĩ...*

> **[Hệ thống]** Gọi tool: `search_flights({'origin': 'Hà Nội', 'destination': 'Đà Nẵng'})`
> 
> **[Hệ thống]** Trả lời trực tiếp

**TravelBuddy:** Dưới đây là các chuyến bay từ Hà Nội đi Đà Nẵng mà tôi tìm được:

1. **Vietnam Airlines (economy)**: 06:00 -> 07:20 | Giá: 1,450,000đ
2. **Vietnam Airlines (business)**: 14:00 -> 15:20 | Giá: 2,800,000đ
3. **VietJet Air (economy)**: 08:30 -> 09:50 | Giá: 890,000đ
4. **Bamboo Airways (economy)**: 11:00 -> 12:20 | Giá: 1,200,000đ

Bạn có ngân sách cho chuyến bay này là bao nhiêu? Hoặc bạn có muốn tôi gợi ý chuyến bay nào không?

---

## Test 3: Multi-step Tool Chaining

**Bạn:** Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu, tư vấn trước

*TravelBuddy đang suy nghĩ...*

> **[Hệ thống]** Gọi tool: `search_flights({'origin': 'Hà Nội', 'destination': 'Phú Quốc'})`
> 
> **[Hệ thống]** Gọi tool: `search_hotels({'city': 'Phú Quốc', 'max_price_per_night': 1950000})`
> 
> **[Hệ thống]** Gọi tool: `calculate_budget({'total_budget': 5000000, 'expenses': 'vé máy bay:1100000,khách sạn:3000000'})`
> 
> **[Hệ thống]** Trả lời trực tiếp

**TravelBuddy:** Dưới đây là gợi ý cho chuyến đi của bạn từ Hà Nội đến Phú Quốc:

**Chuyến bay:**
- VietJet Air: 16:00 -> 18:15 | Giá: 1,100,000đ

**Khách sạn:**
- **9Station Hostel (2 sao)**: Dương Đông | Giá: 200,000đ/đêm | Rating: 4.5
- **Sol by Meliá (4 sao)**: Bãi Trường | Giá: 1,500,000đ/đêm | Rating: 4.2
- **Lahana Resort (3 sao)**: Dương Đông | Giá: 800,000đ/đêm | Rating: 4.0

Mình gợi ý bạn chọn **9Station Hostel** vì giá rất hợp lý và có rating cao (4.5). Tổng chi phí cho 2 đêm sẽ là 400,000đ.

**Tổng chi phí ước tính:**
- Vé máy bay: 1,100,000đ
- Khách sạn (2 đêm): 400,000đ
- **Tổng chi: 1,500,000đ**

**Ngân sách còn lại: 3,500,000đ**

**Gợi ý thêm:**
Bạn có thể sử dụng số tiền còn lại để khám phá các hoạt động vui chơi, ăn uống tại Phú Quốc. Nếu bạn cần thêm thông tin hay hỗ trợ gì khác, cứ cho mình biết nhé!

---

## Test 4: Missing infor / Clarification

**Bạn:** Tôi muốn đặt khách sạn

*TravelBuddy đang suy nghĩ...*

> **[Hệ thống]** Trả lời trực tiếp

**TravelBuddy:** Để giúp bạn đặt khách sạn, mình cần thêm một số thông tin:

1. Bạn muốn đặt khách sạn ở thành phố nào?
2. Ngân sách của bạn cho mỗi đêm là bao nhiêu?
3. Thời gian bạn dự định lưu trú là bao lâu?

Hãy cho mình biết để mình có thể tư vấn tốt nhất nhé!

---

## Test 5: Guardfail / Refusal

**Bạn:** Giải giúp tôi bài tập python về linked list

*TravelBuddy đang suy nghĩ...*

> **[Hệ thống]** Trả lời trực tiếp

**TravelBuddy:** Xin lỗi, nhưng mình không thể giúp bạn với bài tập Python hay bất kỳ vấn đề nào không liên quan đến du lịch. Nếu bạn có kế hoạch du lịch hoặc cần tư vấn về chuyến đi, hãy cho mình biết nhé!

# TravelBuddy Test Results (realtime data)

## Test 6: Kiểm tra API Thời Tiết (wttr.in)
**Mục tiêu:** LLM tự nhận diện khu vực, trigger tool `get_current_weather`, đọc JSON nhiệt độ và đưa lời khuyên an toàn.

**Bạn:** Thời tiết ở Phú Quốc hiện tại thế nào? Có thích hợp để tắm biển không hay toàn mưa bão?

*TravelBuddy đang suy nghĩ...*

> **[Hệ thống]** Gọi tool: `get_current_weather({'city': 'Phú Quốc'})`
> 
> **[Hệ thống]** Trả lời trực tiếp

**TravelBuddy:** Thời tiết ở Phú Quốc hiện tại rất tuyệt vời với nhiệt độ 30°C, trời nắng và độ ẩm 62%. Đây là điều kiện lý tưởng để tắm biển và tham gia các hoạt động ngoài trời. Bạn có thể thoải mái tận hưởng kỳ nghỉ của mình tại đây!

---

## Test 7: Kiểm tra Vé máy bay (SerpApi)
**Mục tiêu:** Bắt buộc AI moi rễ kết quả giá vé máy bay thật từ Google Search (bỏ qua Mock database).

**Bạn:** Mình muốn bay từ Hà Nội đi Đà Lạt trong hôm nay, hãy check Google xem giá vé rẻ nhất của hãng nào là bao nhiêu?

*TravelBuddy đang suy nghĩ...*

> **[Hệ thống]** Gọi tool: `search_flights({'origin': 'Hà Nội', 'destination': 'Đà Lạt'})`
> 
> **[Hệ thống]** Trả lời trực tiếp

**TravelBuddy:** Hiện tại, mình đã tìm thấy thông tin về vé máy bay từ Hà Nội đi Đà Lạt như sau:

1. **Hãng hàng không**: Vietnam Airlines
   - **Giá vé một chiều**: 968.000 VND
   - **Giá vé khứ hồi**: 1.936.000 VND

2. **Hãng hàng không**: Vietjet Air
   - **Giá vé một chiều**: từ 490.000 VND

Bạn có muốn đặt vé khứ hồi hay một chiều? Và bạn có ngân sách cụ thể cho chuyến đi này không?

---

## Test 8: End-to-End Realtime Trip
**Mục tiêu:** Kiểm tra khả năng Agent điều phối tools, kềnh cựa Toán học phân bổ Quỹ ăn uống và format đúng.

**Bạn:** Tôi ở HN, muốn đi Nha Trang 3 ngày 2 đêm, ngân sách 9 triệu

*TravelBuddy đang suy nghĩ...*

> **[Hệ thống]** Gọi tool: `search_flights({'origin': 'Hà Nội', 'destination': 'Nha Trang'})`
> 
> **[Hệ thống]** Gọi tool: `get_current_weather({'city': 'Nha Trang'})`
> 
> **[Hệ thống]** Gọi tool: `calculate_budget({'total_budget': 9000000, 'expenses': 'vé máy bay:843000'})`
> 
> **[Hệ thống]** Gọi tool: `search_hotels({'city': 'Nha Trang', 'max_price_per_night': 2278500})`
> 
> **[Hệ thống]** Trả lời trực tiếp

**TravelBuddy:** Dưới đây là thông tin về chuyến đi mà mình tìm được cho bạn ở Nha Trang:

1. **Chuyến bay:**
   - **Giá vé đã chek:** 843.000 VNĐ

2. **Khách sạn:**
   - **Tên khách sạn:** Seaside Boutique Hotel Nha Trang Beach
   - **Số sao:** 4 sao
   - **Mức giá phòng mỗi đêm:** 1.822.800 VNĐ (giá tạm tính)

3. **Tổng kết chi phí:**
   - **Chi phí vé máy bay:** 843.000 VNĐ
   - **Chi phí khách sạn (2 đêm):** 3.645.600 VNĐ
   - **Tổng chi:** 4.488.600 VNĐ
   - **Ngân sách ban đầu:** 9.000.000 VNĐ
   - **Còn lại:** 4.511.400 VNĐ (Quỹ ăn uống và vui chơi thực tế của bạn)

4. **Gợi ý thêm:**
   - Với số tiền còn lại 4.511.400 VNĐ, bạn có thể thoải mái thưởng thức ẩm thực địa phương và tham gia các hoạt động vui chơi giải trí tại Nha Trang. Hãy nhớ thử các món hải sản tươi ngon và tham gia các tour khám phá đảo nhé!

Nếu bạn cần thêm thông tin hoặc muốn đặt phòng, hãy cho mình biết nhé!