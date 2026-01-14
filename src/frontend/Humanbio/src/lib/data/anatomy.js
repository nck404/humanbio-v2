export const anatomyData = [
  {
    id: "head",
    name: "Đầu & Cổ",
    description: "Trung tâm chỉ huy chứa bộ não và các giác quan chính.",
    path: "M 235 90 C 220 80 220 20 250 15 C 280 20 280 80 265 90 C 265 100 235 100 235 90 Z",
    color: "#6366f1",
    subParts: [
      {
        id: "brain",
        name: "Bộ Não",
        description: "Cơ quan phức tạp nhất, điều khiển mọi suy nghĩ và hành động.",
        details: "Bộ não người chứa khoảng 86 tỷ tế bào thần kinh, kết nối với nhau qua hàng nghìn tỷ khớp thần kinh."
      },
      {
        id: "eyes",
        name: "Mắt",
        description: "Cơ quan thị giác tiếp nhận ánh sáng.",
        details: "Mắt có khả năng tự làm sạch nhờ nước mắt và chớp mắt."
      }
    ]
  },
  {
    id: "torso",
    name: "Thân Trên",
    description: "Khoang chứa các cơ quan sinh tồn quan trọng.",
    path: "M 220 100 C 180 110 180 160 200 280 C 220 300 280 300 300 280 C 320 160 320 110 280 100 C 260 110 240 110 220 100 Z",
    color: "#ec4899",
    subParts: [
      {
        id: "heart",
        name: "Tim",
        description: "Máy bơm sinh học tuần hoàn máu nuôi cơ thể.",
        details: "Tim đập liên tục suốt đời, tạo ra áp lực đủ để phun máu xa 9 mét."
      },
      {
        id: "lungs",
        name: "Phổi",
        description: "Cơ quan trao đổi khí chính.",
        details: "Tổng diện tích bề mặt của các phế nang phổi có thể bao phủ một nửa sân tennis."
      },
      {
        id: "liver",
        name: "Gan",
        description: "Nhà máy hóa chất của cơ thể, lọc độc tố.",
        details: "Gan là cơ quan nội tạng duy nhất có khả năng tái tạo lại một phần đáng kể sau khi bị cắt bỏ."
      }
    ]
  },
  {
    id: "l_arm",
    name: "Tay Trái",
    description: "Chi trên hỗ trợ cầm nắm và vận động.",
    path: "M 180 110 C 160 120 140 200 130 250 C 140 320 160 320 170 250 C 180 200 190 140 190 130 Z",
    color: "#8b5cf6",
    subParts: [
        { id: "humerus_l", name: "Xương Cánh Tay", description: "Xương lớn ở phần trên cánh tay." },
        { id: "hand_l", name: "Bàn Tay", description: "Cấu trúc phức tạp với 27 xương." }
    ]
  },
  {
    id: "r_arm",
    name: "Tay Phải",
    description: "Chi trên hỗ trợ cầm nắm và vận động.",
    path: "M 320 110 C 340 120 360 200 370 250 C 360 320 340 320 330 250 C 320 200 310 140 310 130 Z",
    color: "#8b5cf6",
    subParts: [
        { id: "humerus_r", name: "Xương Cánh Tay", description: "Xương lớn ở phần trên cánh tay." },
        { id: "hand_r", name: "Bàn Tay", description: "Cấu trúc phức tạp với 27 xương." }
    ]
  },
  {
    id: "legs",
    name: "Chân & Khung Chậu",
    description: "Hệ thống nâng đỡ và di chuyển.",
    path: "M 200 280 C 180 300 180 400 200 550 C 240 560 260 560 300 550 C 320 400 320 300 300 280 Z",
    color: "#3b82f6",
    subParts: [
        { id: "femur", name: "Xương Đùi", description: "Xương dài và cứng nhất cơ thể." },
        { id: "knees", name: "Khớp Gối", description: "Khớp lớn nhất và phức tạp nhất." }
    ]
  }
];
