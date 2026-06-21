FROM python:3.11-slim

WORKDIR /app

# نصب وابستگی‌ها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# کپی کردن فایل‌های پروژه
COPY . .

# ایجاد دایرکتوری دیتا
RUN mkdir -p /app/data

# اجرای ربات
CMD ["python", "-m", "bot.main"]
