# DACS
Research on security risks in IoT
# IoT Security Simulation: Vulnerability Research & Hardening (MQTT)

## 📌 Tổng quan dự án
Dự án này tập trung vào việc nghiên cứu và thực nghiệm các lỗ hổng bảo mật phổ biến trong hệ sinh thái IoT, cụ thể là giao thức **MQTT**. Mục tiêu chính là mô phỏng các kịch bản tấn công thực tế và triển khai giải pháp phòng thủ bằng mã hóa và xác thực.

## 🛠 Mô hình hệ thống (Lab Setup)
Hệ thống được ảo hóa trên **VirtualBox** với kiến trúc đa node:
- **Broker:** Ubuntu Server chạy Eclipse Mosquitto.
- **Client (IoT Device):** Alpine Linux sử dụng Python script giả lập cảm biến.
- **Attacker:** Kali Linux trang bị các công cụ kiểm thử an ninh.



## ⚡ Các kịch bản tấn công thực nghiệm
Dự án tái hiện các nguy cơ khi hệ thống truyền tin qua cổng 1883 (Plaintext):
1. **Sniffing:** Sử dụng Wireshark để bắt và đọc dữ liệu cảm biến nhạy cảm.
2. **Man-in-the-Middle (MITM):** Chèn dữ liệu giả mạo vào luồng giao tiếp.
3. **Denial of Service (DoS):** Sử dụng `hping3` làm quá tải Broker, gây gián đoạn hệ thống.

## 🛡 Giải pháp bảo mật (Hardening)
- **Encryption:** Triển khai **TLS/SSL** (OpenSSL) trên cổng 8883 để mã hóa toàn bộ kênh truyền.
- **Authentication:** Cấu hình xác thực Username/Password và vô hiệu hóa kết nối ẩn danh.
- **Authorization:** Thiết lập danh sách kiểm soát truy cập (**ACL**) cho từng Topic.

## 🚀 Công nghệ sử dụng
- **Languages:** Python (Paho-MQTT)
- **Tools:** Kali Linux, Wireshark, hping3, Mosquitto, OpenSSL
- **Infrastructure:** VirtualBox, Alpine Linux, Ubuntu Server

## 📈 Kết quả
- Ngăn chặn hoàn toàn các nỗ lực nghe lén và truy cập trái phép sau khi áp dụng TLS/SSL.
- Đánh giá được mức độ ảnh hưởng của bảo mật đến hiệu năng hệ thống (độ trễ và tài nguyên CPU).
