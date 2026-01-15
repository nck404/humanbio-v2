# Hướng dẫn cài đặt AI Chat với Gemini

## Bước 1: Cài đặt dependencies

```bash
cd src/backend
pip install -r requirements.txt
```

## Bước 2: Cấu hình Gemini API Key

1. Truy cập https://makersuite.google.com/app/apikey để lấy API key
2. Mở file `src/backend/.env`
3. Thay thế `your-gemini-api-key-here` bằng API key của bạn:

```
GEMINI_API_KEY=AIzaSy...your-actual-key
```

## Bước 3: Tạo database migration

```bash
# Từ thư mục src/backend
flask db migrate -m "Add ChatSession and ChatMessage"
flask db upgrade
```

Hoặc nếu không dùng migrations, database sẽ tự động tạo khi chạy app:

```bash
python app.py
```

## Bước 4: Chạy backend

```bash
cd src/backend
python app.py
```

Backend sẽ chạy tại http://localhost:5000

## Bước 5: Chạy frontend

```bash
cd src/frontend/Humanbio
npm run dev
```

## Tính năng AI Chat

- ✅ **AI thực sự hoạt động** với Gemini API
- ✅ **Lịch sử chat** - Tất cả chat được lưu vào database
- ✅ **Tạo chat mới** - Nút "New Chat" để bắt đầu cuộc trò chuyện mới
- ✅ **Copy câu trả lời** - Hover vào tin nhắn AI để copy
- ✅ **Resize window** - Kéo góc dưới bên phải để thay đổi kích thước
- ✅ **Draggable** - Kéo header để di chuyển cửa sổ
- ✅ **Responsive** - Giao diện mobile riêng biệt
- ✅ **Sidebar lịch sử** - Xem và chuyển đổi giữa các chat cũ

## Lưu ý

- Cần đăng nhập để sử dụng AI chat
- Mỗi user có lịch sử chat riêng
- Chat history được lưu vĩnh viễn trong database
- Title của chat tự động được tạo từ tin nhắn đầu tiên
