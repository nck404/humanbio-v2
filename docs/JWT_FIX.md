# 🔧 Fix JWT Identity Type Conversion

## Vấn đề
Lỗi 422 (UNPROCESSABLE ENTITY) xảy ra vì `get_jwt_identity()` trả về **string** nhưng database models expect **integer** cho `user_id`.

## Giải pháp
Đã sửa tất cả các routes để convert JWT identity sang integer:

### Files đã sửa:
1. ✅ `routes/auth.py` - `/me`, `/me/settings`
2. ✅ `routes/chat.py` - Tất cả endpoints
3. ✅ `routes/forum.py` - Tất cả endpoints
4. ✅ `routes/comments.py` - `/comments` POST

### Thay đổi:
```python
# TRƯỚC (SAI)
user_id = get_jwt_identity()

# SAU (ĐÚNG)
user_id = int(get_jwt_identity())
```

## Cách test
1. Restart backend:
   ```bash
   cd src/backend
   python app.py
   ```

2. Đăng nhập lại vào frontend

3. Thử các tính năng:
   - ✅ Load user profile
   - ✅ Update settings
   - ✅ Create chat session
   - ✅ Send messages
   - ✅ Load chat history

## Lưu ý
- JWT tokens cũ vẫn hoạt động
- Không cần migrate database
- Không cần thay đổi frontend
