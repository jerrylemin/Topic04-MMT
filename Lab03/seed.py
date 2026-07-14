from werkzeug.security import generate_password_hash

from database import clear_db, get_db, init_db


USERS = [
    (1, "admin", "admin@lab.local", "Admin123!", "admin"),
    (12, "user_a", "usera@lab.local", "UserA123!", "user"),
    (13, "user_b", "userb@lab.local", "UserB123!", "user"),
]

PRODUCTS = [
    (5, "USB Security Key", "Khóa bảo mật USB dùng cho dữ liệu mô phỏng.", 100000, 20),
    (6, "Wireless Mouse", "Chuột không dây dùng trong phòng lab.", 250000, 15),
    (7, "Mechanical Keyboard", "Bàn phím cơ dữ liệu mẫu.", 1200000, 10),
    (8, "Lab Laptop", "Máy tính giả lập, không có giao dịch thật.", 15000000, 5),
]

INVOICES = [
    (1001, 12, "demo_paid", 100000, 5, "USB Security Key", 100000, 1),
    (1002, 13, "demo_paid", 250000, 6, "Wireless Mouse", 250000, 1),
    (1003, 12, "demo_paid", 1200000, 7, "Mechanical Keyboard", 1200000, 1),
]


def reset_database() -> None:
    clear_db()
    init_db()
    db = get_db()
    db.executemany(
        "INSERT INTO users(id, username, email, password_hash, role) VALUES (?, ?, ?, ?, ?)",
        [(uid, username, email, generate_password_hash(password), role) for uid, username, email, password, role in USERS],
    )
    db.executemany(
        "INSERT INTO products(id, name, description, price_vnd, stock) VALUES (?, ?, ?, ?, ?)",
        PRODUCTS,
    )
    for invoice_id, user_id, status, total, product_id, name, price, quantity in INVOICES:
        db.execute(
            "INSERT INTO invoices(id, user_id, status, total_amount) VALUES (?, ?, ?, ?)",
            (invoice_id, user_id, status, total),
        )
        db.execute(
            """INSERT INTO invoice_items
               (invoice_id, product_id, product_name, unit_price, quantity, line_total)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (invoice_id, product_id, name, price, quantity, price * quantity),
        )
    db.commit()


if __name__ == "__main__":
    from app import create_app

    application = create_app()
    with application.app_context():
        reset_database()
    print("Đã khởi tạo lại Lab03/lab03.db")

