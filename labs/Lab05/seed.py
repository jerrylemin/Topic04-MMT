from flask import Flask, has_app_context
from werkzeug.security import generate_password_hash

from config import Config
from database import get_db, init_db
from security_utils import legacy_digest


USERS = (
    (1, "admin_lab", "Quản trị Lab", "admin@lab.local", "admin", "AdminLab123!"),
    (2, "student_a", "Sinh viên A", "studenta@lab.local", "user", "StudentA123!"),
    (3, "student_b", "Sinh viên B", "studentb@lab.local", "user", "StudentB123!"),
)
PRODUCTS = (
    (1, "USB Security Key", "Security", "Khóa bảo mật USB dùng cho lab.", 850000, 12, 1),
    (2, "Wireless Mouse", "Peripheral", "Chuột không dây cho máy lab.", 420000, 20, 1),
    (3, "Mechanical Keyboard", "Peripheral", "Bàn phím cơ thực hành.", 1250000, 9, 1),
    (4, "Lab Laptop", "Computer", "Máy tính giả lập dành riêng cho lab.", 18500000, 4, 1),
    (5, "Network Cable", "Network", "Cáp mạng cho mô hình local.", 90000, 50, 1),
    (6, "Web Security Book", "Book", "Tài liệu an toàn ứng dụng web.", 390000, 16, 1),
    (7, "Linux Practice USB", "Storage", "USB thực hành Linux local.", 280000, 24, 1),
    (8, "Local Test Router", "Network", "Router chỉ dùng trong mô hình giả lập.", 1450000, 6, 1),
)


def reset_database() -> None:
    db = get_db()
    db.executescript("""
        DELETE FROM login_attempts;
        DELETE FROM query_events;
        DELETE FROM audit_logs;
        DELETE FROM trace_records;
        DELETE FROM products;
        DELETE FROM users;
    """)
    db.executemany(
        """INSERT INTO users
           (id, username, display_name, email, role, legacy_password_digest, password_hash, active)
           VALUES (?, ?, ?, ?, ?, ?, ?, 1)""",
        [
            (user_id, username, display_name, email, role, legacy_digest(password),
             generate_password_hash(password, method="pbkdf2:sha256:600000"))
            for user_id, username, display_name, email, role, password in USERS
        ],
    )
    db.executemany(
        """INSERT INTO products
           (id, name, category, description, price_vnd, stock, visible)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        PRODUCTS,
    )
    db.commit()


def main() -> None:
    app = Flask(__name__)
    app.config.from_object(Config)
    with app.app_context():
        init_db()
        reset_database()
    print("Lab05 database reset with 3 local demo users and 8 products.")


if __name__ == "__main__":
    main()

