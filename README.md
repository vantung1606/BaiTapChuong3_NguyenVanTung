# Dự án Backup Database Tự Động

## Mô tả
Chương trình tự động sao lưu các file database (.sql, .sqlite3) vào thư mục `BackupFile/` vào lúc 00:00 mỗi ngày và gửi email thông báo kết quả (thành công hoặc thất bại).

## Hướng dẫn cài đặt

### 1. Clone repository
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### 2. Cài đặt thư viện cần thiết
```bash
pip install -r requirements.txt
```

### 3. Tạo file `.env`
Tạo file `.env` ngay trong thư mục project với nội dung như sau:

```env
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_RECEIVER=receiver_email@gmail.com
```

> Lưu ý:
> - `EMAIL_SENDER`: địa chỉ email gửi đi
> - `EMAIL_PASSWORD`: mật khẩu ứng dụng (application password)
> - `EMAIL_RECEIVER`: địa chỉ email nhận thông báo

👉 Nếu dùng Gmail, cần bật xác thực 2 lớp và tạo **App Password**.

## Cách chạy chương trình

Chạy file `BackupFile.py`:

```bash
python BackupFile.py
```

Chương trình sẽ:
- Quét thư mục hiện tại, tìm file `.sql` hoặc `.sqlite3`
- Copy vào thư mục `BackupFile/`
- Gửi email báo cáo mỗi ngày vào lúc 00:00

## Cấu trúc thư mục

```
backup_project/
|
|├— BackUpFile.py           # File Python chính
|├— .env                # File chứa thông tin email
|├— requirements.txt    # Các thư viện cần cài
|└— .gitignore          # Bỏ qua file .env
```

## Lưu ý

- Tuyệt đối không push file `.env` lên GitHub.
- Kiểm tra thông tin email trước khi chạy.
- Nên để server/máy tính luôn bật để backup đúng giờ.

