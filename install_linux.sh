#!/bin/bash

# Script cài đặt Human Biology Backend cho Linux (Ubuntu/Debian)
# Tự động hóa việc cài đặt Python, Virtual Environment, và các dependencies.

# Màu sắc hiển thị
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}====================================================${NC}"
echo -e "${GREEN}🚀 Đang bắt đầu cài đặt Human Biology Backend cho Linux${NC}"
echo -e "${BLUE}====================================================${NC}"

# 1. Cập nhật hệ thống
echo -e "\n${BLUE}1/4: Cập nhật hệ thống...${NC}"
sudo apt update && sudo apt upgrade -y

# 2. Cài đặt Python và các công cụ cần thiết
echo -e "\n${BLUE}2/4: Cài đặt Python 3, pip và venv...${NC}"
sudo apt install -y python3 python3-pip python3-venv build-essential python3-dev

# 3. Tạo Virtual Environment
echo -e "\n${BLUE}3/4: Thiết lập môi trường ảo (Virtual Environment)...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✅ Đã tạo venv thành công.${NC}"
else
    echo -e "${BLUE}ℹ️ venv đã tồn tại, bỏ qua bước tạo mới.${NC}"
fi

# Kích hoạt môi trường ảo để cài đặt dependencies
source venv/bin/activate

# 4. Cài đặt Dependencies
echo -e "\n${BLUE}4/4: Cài đặt các thư viện Python cần thiết...${NC}"
pip install --upgrade pip

# Di chuyển vào thư mục backend
BACKEND_DIR="src/backend"
if [ -d "$BACKEND_DIR" ]; then
    cd "$BACKEND_DIR"
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        # Cài đặt thêm Gunicorn cho Linux
        pip install gunicorn psutil colorama
        echo -e "${GREEN}✅ Cài đặt dependencies thành công.${NC}"
    else
        echo -e "${RED}❌ Lỗi: Không tìm thấy file requirements.txt tại $BACKEND_DIR${NC}"
        exit 1
    fi
    cd ../..
else
    echo -e "${RED}❌ Lỗi: Không tìm thấy thư mục src/backend${NC}"
    exit 1
fi

echo -e "\n${BLUE}====================================================${NC}"
echo -e "${GREEN}🎉 CÀI ĐẶT HOÀN TẤT!${NC}"
echo -e "${BLUE}====================================================${NC}"
echo -e "Để chạy dự án, hãy sử dụng lệnh:"
echo -e "${GREEN}source venv/bin/activate${NC} (nếu chưa kích hoạt)"
echo -e "${GREEN}python3 deploy.py${NC}"
echo -e "${BLUE}====================================================${NC}"
