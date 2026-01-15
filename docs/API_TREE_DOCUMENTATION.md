
## Tổng quan hệ thống

**Base URL**: `http://localhost:5000`

**Technology Stack**:
- Framework: Flask
- Database: SQLite (SQLAlchemy ORM)
- Authentication: JWT (Flask-JWT-Extended)
- AI: Google Gemini API
- CORS: Enabled

---

## CẤU TRÚC API TREE

```
/api
├── AUTHENTICATION & USER (/api)
│   ├── POST   /register          # Đăng ký tài khoản mới
│   ├── POST   /login             # Đăng nhập
│   ├── GET    /me                # Lấy thông tin user hiện tại [JWT]
│   └── PUT    /me/settings       # Cập nhật settings [JWT]
│
├── ADMIN (/api/admin)
│   ├── 📝 Tests Management
│   │   ├── POST   /tests                    # Tạo bài test mới [ADMIN]
│   │   ├── GET    /tests                    # Danh sách tất cả tests [ADMIN]
│   │   ├── GET    /tests/<test_id>          # Chi tiết 1 test [ADMIN]
│   │   ├── PUT    /tests/<test_id>          # Cập nhật test [ADMIN]
│   │   └── DELETE /tests/<test_id>          # Xóa test [ADMIN]
│   │
│   └── Users Management
│       ├── GET    /users                    # Danh sách users [ADMIN]
│       └── POST   /users/<user_id>/promote  # Promote user lên admin [ADMIN]
│
├── TESTS (/api/tests)
│   ├── GET    /                  # Danh sách tests (có search)
│   └── GET    /<test_id>         # Chi tiết test + câu hỏi
│
├── COMMENTS (/api/comments)
│   ├── GET    /<slug>            # Lấy comments của 1 lesson
│   └── POST   /                  # Đăng comment mới [JWT]
│
├── FORUM (/api/forum)
│   ├── Posts
│   │   ├── GET    /posts                      # Danh sách posts (filter by topic)
│   │   ├── POST   /posts                      # Tạo post mới [JWT]
│   │   ├── GET    /posts/<post_id>            # Chi tiết post + comments
│   │   ├── POST   /posts/<post_id>/comments   # Thêm comment vào post [JWT]
│   │   └── POST   /posts/<post_id>/react      # React vào post [JWT]
│   │
│   └── Comments
│       └── POST   /comments/<comment_id>/react # React vào comment [JWT]
│
└── AI CHAT (/api/chat)
    ├── GET    /sessions                # Danh sách chat sessions [JWT]
    ├── POST   /session                 # Tạo session mới [JWT]
    ├── GET    /session/<session_id>    # Lấy messages của session [JWT]
    ├── DELETE /session/<session_id>    # Xóa session [JWT]
    └── POST   /message                 # Gửi message & nhận AI response [JWT]
```

---

## CHI TIẾT TỪNG MODULE

### AUTHENTICATION & USER (`/api`)

#### 🔹 `POST /api/register`
**Chức năng**: Đăng ký tài khoản mới

**Request Body**:
```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "recaptcha_token": "string"
}
```

**Response**: 
- `201`: User created successfully
- `400`: Missing fields / Username exists / Email exists / Invalid reCAPTCHA

**Logic**:
1. Validate required fields
2. Verify reCAPTCHA
3. Check username/email uniqueness
4. Hash password (bcrypt)
5. Create user in database

---

#### 🔹 `POST /api/login`
**Chức năng**: Đăng nhập và nhận JWT token

**Request Body**:
```json
{
  "email": "string",
  "password": "string",
  "recaptcha_token": "string"
}
```

**Response**:
```json
{
  "access_token": "jwt_token_string",
  "user": {
    "id": 1,
    "username": "john",
    "email": "john@example.com",
    "is_admin": false,
    "settings": {
      "primaryColor": "#6366f1",
      "fontSize": 16,
      "fontFamily": "sans"
    }
  }
}
```

**Logic**:
1. Verify reCAPTCHA
2. Find user by email
3. Check password hash
4. Generate JWT token (identity = user.id as string)
5. Return token + user data

---

#### 🔹 `GET /api/me` [JWT Required]
**Chức năng**: Lấy thông tin user hiện tại

**Headers**: `Authorization: Bearer <token>`

**Response**: User object với settings

**Logic**:
1. Extract user_id from JWT
2. Query user from database
3. Return user info + settings

---

#### 🔹 `PUT /api/me/settings` [JWT Required]
**Chức năng**: Cập nhật settings (màu, font, size)

**Request Body**:
```json
{
  "settings": {
    "primaryColor": "#ff5733",
    "fontSize": 18,
    "fontFamily": "serif"
  }
}
```

**Response**: Updated settings

**Logic**:
1. Get current user
2. Merge new settings with existing
3. Save to database
4. Return updated settings

---

### ADMIN MODULE (`/api/admin`)

#### Tests Management

#### 🔹 `POST /api/admin/tests` [Admin Required]
**Chức năng**: Tạo bài test mới với câu hỏi

**Request Body**:
```json
{
  "title": "Test Sinh học cơ bản",
  "description": "Mô tả test",
  "category": "Biology",
  "questions": [
    {
      "text": "Câu hỏi 1?",
      "image_data": "base64_or_url",
      "type": "multiple_choice",
      "options": ["A", "B", "C", "D"],
      "correct_answer": "A"
    }
  ]
}
```

**Logic**:
1. Create MockTest
2. Loop through questions array
3. Create Question for each
4. Link questions to test via test_id
5. Commit transaction

---

#### 🔹 `GET /api/admin/tests` [Admin Required]
**Chức năng**: Lấy danh sách tất cả tests (cho admin)

**Response**:
```json
[
  {
    "id": 1,
    "title": "Test 1",
    "description": "...",
    "category": "Biology",
    "question_count": 10
  }
]
```

---

#### 🔹 `GET /api/admin/tests/<test_id>` [Admin Required]
**Chức năng**: Xem chi tiết test (bao gồm đáp án đúng)

**Response**: Test object + questions array với correct_answer

---

#### 🔹 `PUT /api/admin/tests/<test_id>` [Admin Required]
**Chức năng**: Cập nhật test

**Logic**:
1. Update test metadata
2. Delete all old questions
3. Create new questions from request
4. Commit

---

#### 🔹 `DELETE /api/admin/tests/<test_id>` [Admin Required]
**Chức năng**: Xóa test

**Logic**: Cascade delete questions (configured in model)

---

#### 👥 Users Management

#### 🔹 `GET /api/admin/users` [Admin Required]
**Chức năng**: Danh sách tất cả users

**Response**:
```json
[
  {
    "id": 1,
    "username": "john",
    "email": "john@example.com",
    "is_admin": false
  }
]
```

---

#### 🔹 `POST /api/admin/users/<user_id>/promote` [Admin Required]
**Chức năng**: Promote user lên admin

**Logic**: Set `is_admin = True`

---

### TESTS MODULE (`/api/tests`)

#### 🔹 `GET /api/tests`
**Chức năng**: Danh sách tests (public, có search)

**Query Params**: `?q=search_term`

**Response**: Array of tests (không có correct_answer)

**Logic**:
- If query param exists: Filter by title (ILIKE)
- Else: Return all tests

---

#### 🔹 `GET /api/tests/<test_id>`
**Chức năng**: Chi tiết test + questions

**Response**: Test object + questions (CÓ correct_answer - for practice)

**Note**: Trong production nên tách endpoint `/check` để verify answers

---

### COMMENTS MODULE (`/api/comments`)

#### 🔹 `GET /api/comments/<slug>`
**Chức năng**: Lấy comments của 1 lesson (theo slug)

**Response**:
```json
[
  {
    "id": 1,
    "content": "Great lesson!",
    "username": "john",
    "avatar_seed": "john",
    "created_at": "2026-01-15T...",
    "replies": [
      {
        "id": 2,
        "content": "I agree!",
        "username": "jane",
        ...
      }
    ]
  }
]
```

**Logic**:
1. Query top-level comments (parent_id = None)
2. Recursive serialize: include replies
3. Order by created_at DESC

---

#### 🔹 `POST /api/comments` [JWT Required]
**Chức năng**: Đăng comment hoặc reply

**Request Body**:
```json
{
  "content": "My comment",
  "slug": "lesson-slug",
  "parent_id": null  // or comment_id for reply
}
```

**Logic**:
1. Get user_id from JWT
2. Create Comment with slug, user_id, parent_id
3. Return created comment

---

### FORUM MODULE (`/api/forum`)

#### 📄 Posts

#### 🔹 `GET /api/forum/posts`
**Chức năng**: Danh sách posts (có filter by topic)

**Query Params**: `?topic=General`

**Response**:
```json
[
  {
    "id": 1,
    "title": "Post title",
    "content": "...",
    "topic": "General",
    "created_at": "...",
    "author": {
      "username": "john",
      "avatar_seed": "john"
    },
    "comment_count": 5,
    "reaction_count": 10
  }
]
```

---

#### 🔹 `POST /api/forum/posts` [JWT Required]
**Chức năng**: Tạo post mới

**Request Body**:
```json
{
  "title": "My post",
  "content": "Content here",
  "topic": "Biology"  // optional, default "General"
}
```

---

#### 🔹 `GET /api/forum/posts/<post_id>`
**Chức năng**: Chi tiết post + comments + reactions

**Response**: Post object + nested comments + user reactions

**Logic**:
1. Get post
2. Optional JWT: get current_user_id
3. Serialize comments recursively
4. Include user's reaction if logged in
5. Return full post data

---

#### 🔹 `POST /api/forum/posts/<post_id>/comments` [JWT Required]
**Chức năng**: Thêm comment vào post

**Request Body**:
```json
{
  "content": "My comment",
  "parent_id": null  // for nested replies
}
```

---

#### 🔹 `POST /api/forum/posts/<post_id>/react` [JWT Required]
**Chức năng**: React vào post (like, love, etc.)

**Request Body**:
```json
{
  "type": "like"  // or "love", etc.
}
```

**Logic**:
1. Check if user already reacted
2. If same type: Remove reaction (toggle off)
3. If different type: Update reaction type
4. If no reaction: Create new reaction

---

#### 💭 Comments

#### 🔹 `POST /api/forum/comments/<comment_id>/react` [JWT Required]
**Chức năng**: React vào comment

**Logic**: Same as post reaction

---

###  AI CHAT MODULE (`/api/chat`)

#### 🔹 `GET /api/chat/sessions` [JWT Required]
**Chức năng**: Lấy danh sách chat sessions của user

**Response**:
```json
[
  {
    "id": 1,
    "title": "Chat về tim mạch",
    "created_at": "2026-01-15T..."
  }
]
```

**Logic**:
1. Get user_id from JWT
2. Query sessions by user_id
3. Order by created_at DESC

---

#### 🔹 `POST /api/chat/session` [JWT Required]
**Chức năng**: Tạo chat session mới

**Response**:
```json
{
  "id": 2,
  "title": "New Chat",
  "created_at": "...",
  "messages": []
}
```

**Logic**: Create empty ChatSession with default title "New Chat"

---

#### 🔹 `GET /api/chat/session/<session_id>` [JWT Required]
**Chức năng**: Lấy messages của 1 session

**Response**:
```json
[
  {
    "role": "user",
    "content": "Giải thích về tim?",
    "created_at": "..."
  },
  {
    "role": "model",
    "content": "Tim là cơ quan...",
    "created_at": "..."
  }
]
```

**Logic**:
1. Verify session belongs to user (403 if not)
2. Query messages by session_id
3. Order by created_at

---

#### 🔹 `DELETE /api/chat/session/<session_id>` [JWT Required]
**Chức năng**: Xóa chat session

**Logic**:
1. Verify ownership
2. Delete session (cascade delete messages)
3. Return success

---

#### 🔹 `POST /api/chat/message` [JWT Required]
**Chức năng**: Gửi message và nhận AI response

**Request Body**:
```json
{
  "session_id": 1,
  "content": "Giải thích về tim?"
}
```

**Response**:
```json
{
  "role": "model",
  "content": "Tim là cơ quan bơm máu..."
}
```

**Logic**:
1. Verify session ownership
2. Save user message to database
3. Get last 10 messages for context
4. Build Gemini chat history
5. Send prompt: "Trả lời câu hỏi sau bằng tiếng việt {content}"
6. Get AI response
7. Save AI message to database
8. Update session title (if first message)
9. Return AI response

**AI Configuration**:
- Model: `gemini-3-flash-preview`
- Language: Vietnamese (forced via prompt)
- Context: Last 10 messages

---

## 🔒 AUTHENTICATION & AUTHORIZATION

### JWT Authentication
- **Header**: `Authorization: Bearer <token>`
- **Token contains**: `user_id` (as string)
- **Expiration**: Configured in JWT_SECRET_KEY

### Decorators
- `@jwt_required()`: Requires valid JWT token
- `@admin_required`: Requires JWT + `is_admin = True`

### Authorization Checks
- **Chat sessions**: User can only access their own sessions
- **Forum reactions**: One reaction per user per post/comment
- **Admin routes**: Only accessible by admin users

---

## 🗄️ DATABASE MODELS

### User
- id, username, email, password_hash
- avatar_seed, is_admin
- **settings** (JSON): primaryColor, fontSize, fontFamily

### MockTest
- id, title, description, category, created_at
- **Relationship**: questions (cascade delete)

### Question
- id, test_id, question_text, image_url
- question_type, options (JSON), correct_answer

### Comment (Theory lessons)
- id, content, lesson_slug, user_id
- parent_id (self-referential for replies)
- **Relationship**: replies (cascade delete)

### ForumPost
- id, title, content, topic, user_id, created_at
- **Relationships**: comments, reactions, author

### ForumComment
- id, content, post_id, user_id, parent_id, created_at
- **Relationships**: replies, reactions, author

### ForumPostReaction / ForumCommentReaction
- id, user_id, post_id/comment_id, type

### ChatSession
- id, user_id, title, created_at
- **Relationship**: messages (cascade delete)

### ChatMessage
- id, session_id, role (user/model), content, created_at

---

## 🔄 CASCADE DELETE BEHAVIOR

- **MockTest deleted** → All Questions deleted
- **ForumPost deleted** → All Comments + Reactions deleted
- **ForumComment deleted** → All Replies + Reactions deleted
- **ChatSession deleted** → All Messages deleted
- **Comment deleted** → All Replies deleted

---

## 🚀 PERFORMANCE NOTES

### Optimizations
- Indexes on foreign keys (automatic)
- Lazy loading for relationships
- Limited chat history (10 messages)

### Potential Bottlenecks
- Forum reactions: O(n) search in Python (should use SQL JOIN)
- Recursive comment serialization: Can be slow with deep nesting
- No pagination on lists (should add for production)

---

## 🔐 SECURITY CONSIDERATIONS

### Implemented
✅ Password hashing (bcrypt)
✅ JWT authentication
✅ reCAPTCHA verification
✅ CORS enabled
✅ Authorization checks (user can only access own data)

### Missing (for production)
⚠️ Rate limiting
⚠️ Input sanitization (XSS protection)
⚠️ SQL injection protection (using ORM helps)
⚠️ HTTPS enforcement
⚠️ Token refresh mechanism
⚠️ Password reset flow

---

## 📊 API STATISTICS

- **Total Endpoints**: 28
- **Public Endpoints**: 4 (register, login, tests list, forum posts)
- **JWT Protected**: 18
- **Admin Only**: 6
- **AI Powered**: 1 (chat message)

---

## 🎯 USE CASES

### Student Flow
1. Register → Login → Get JWT
2. Browse tests → Take test
3. Read theory → Comment on lessons
4. Use AI chat for questions
5. Participate in forum

### Admin Flow
1. Login (admin account)
2. Create/Edit/Delete tests
3. Manage users (promote to admin)
4. Monitor forum activity

### AI Chat Flow
1. Create session
2. Send messages → Get AI responses (Vietnamese)
3. View chat history
4. Delete old chats

---
