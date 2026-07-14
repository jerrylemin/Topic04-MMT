from app import create_app
from database import reset_db
app=create_app()
with app.app_context(): reset_db()
print("Đã khởi tạo lại lab01.db")
