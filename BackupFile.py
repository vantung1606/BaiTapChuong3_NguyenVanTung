import os
import shutil
import smtplib
import schedule
import time
from datetime import datetime
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

EMAIL_SENDER = os.getenv('EMAIL_SENDER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_RECEIVER = os.getenv('EMAIL_RECEIVER')

BACKUP_FOLDER = "BaiTapChuong3_NguyenVanTung"
os.makedirs(BACKUP_FOLDER, exist_ok=True)

def gui_email(tieu_de, noi_dung):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER
        msg['Subject'] = tieu_de

        msg.attach(MIMEText(noi_dung, 'plain'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)

        print(f"[{datetime.now()}] Đã gửi email thành công.")
    except Exception as e:
        print(f"[{datetime.now()}] Gửi email thất bại: {e}")

# Hàm sao lưu database
def backup_database():
    try:
        file_list = [f for f in os.listdir('.') if f.endswith('.sql') or f.endswith('.sqlite3')]
        
        if not file_list:
            raise Exception("Không tìm thấy file database.")

        for file in file_list:
            duong_dan_goc = os.path.join('.', file)
            duong_dan_backup = os.path.join(BACKUP_FOLDER, f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file}")
            shutil.copy2(duong_dan_goc, duong_dan_backup)

        gui_email("Sao lưu thành công", f"Đã sao lưu thành công lúc {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}.")
        print(f"[{datetime.now()}] Sao lưu thành công.")
    except Exception as e:
        gui_email("Sao lưu thất bại", f"Lỗi khi sao lưu: {str(e)}")
        print(f"[{datetime.now()}] Sao lưu thất bại: {e}")

# Đặt lịch sao lưu
schedule.every().day.at("00:00").do(backup_database)

print("Đang chạy chương trình sao lưu tự động...")

while True:
    schedule.run_pending()
    time.sleep(60)
