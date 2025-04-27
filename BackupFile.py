import os
import shutil
import smtplib
import schedule
import time
from datetime import datetime
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Nạp biến môi trường từ file .env
load_dotenv()

# Lấy thông tin email từ biến môi trường
EMAIL_SENDER = os.getenv('EMAIL_SENDER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_RECEIVER = os.getenv('EMAIL_RECEIVER')

# Thư mục lưu file backup
BACKUP_FOLDER = "BaiTapChuong3_NguyenVanTung"
os.makedirs(BACKUP_FOLDER, exist_ok=True)

# Hàm gửi email thông báo với file đính kèm
def gui_email(tieu_de, noi_dung, file_dinh_kem=None):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER
        msg['Subject'] = tieu_de

        msg.attach(MIMEText(noi_dung, 'plain'))

        if file_dinh_kem:
            # Đính kèm file
            part = MIMEBase('application', 'octet-stream')
            with open(file_dinh_kem, 'rb') as file:
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(file_dinh_kem)}')
            msg.attach(part)

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)

        print(f"[{datetime.now()}] Đã gửi email thông báo thành công.")
    except Exception as e:
        print(f"[{datetime.now()}] Gửi email thất bại: {e}")

# Hàm tạo file .sql mới
def tao_file_sql():
    try:
        # Lấy ngày hiện tại để tạo tên file
        ten_file = f"backup_{datetime.now().strftime('%Y%m%d')}.sql"
        duong_dan_file = os.path.join(BACKUP_FOLDER, ten_file)
        
        # Nội dung của file .sql (ví dụ: tạo bảng và thêm dữ liệu mẫu)
        noi_dung_sql = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT
        );
        
        INSERT INTO users (name, email) VALUES ('Nguyen Van Tung', 'tung@example.com');
        """

        # Tạo và ghi nội dung vào file .sql
        with open(duong_dan_file, 'w') as file:
            file.write(noi_dung_sql)

        print(f"[{datetime.now()}] Đã tạo file {ten_file} thành công.")
        return duong_dan_file
    except Exception as e:
        print(f"[{datetime.now()}] Lỗi khi tạo file .sql: {e}")
        return None

# Hàm sao lưu database
def backup_database():
    try:
        # Tìm các file database có đuôi .sql hoặc .sqlite3
        danh_sach_file = [f for f in os.listdir('.') if f.endswith('.sql') or f.endswith('.sqlite3')]
        
        if not danh_sach_file:
            raise Exception("Không tìm thấy file database cần backup.")

        for file in danh_sach_file:
            duong_dan_goc = os.path.join('.', file)
            duong_dan_backup = os.path.join(BACKUP_FOLDER, f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file}")
            shutil.copy2(duong_dan_goc, duong_dan_backup)

        # Tạo file .sql mới và gửi qua email
        file_sql = tao_file_sql()
        if file_sql:
            gui_email("Sao lưu thành công", f"Đã sao lưu thành công lúc {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}.", file_sql)
        else:
            gui_email("Sao lưu thất bại", "Không thể tạo file .sql.")

        print(f"[{datetime.now()}] Sao lưu thành công.")
    except Exception as e:
        gui_email("Sao lưu thất bại", f"Lỗi khi sao lưu: {str(e)}")
        print(f"[{datetime.now()}] Sao lưu thất bại: {e}")

# Đặt lịch sao lưu lúc 00:00 mỗi ngày
schedule.every().day.at("00:00").do(backup_database)

print("Đang chạy chương trình sao lưu tự động...")

# Chạy vòng lặp kiểm tra lịch
while True:
    schedule.run_pending()
    time.sleep(60)  # Chờ 60 giây rồi kiểm tra lại
