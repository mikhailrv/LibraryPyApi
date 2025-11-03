# scripts/add_test_user.py
import asyncio
from sqlmodel import Session, select
from app.database.db import engine
from app.auth.models import User

def main():
    with Session(engine) as session:
        stmt = select(User).where(User.username == "admin")
        user = session.exec(stmt).first()
        if user:
            print("✅ User already exists")
            return

        user = User(
            username="admin",
            hashed_password="admin123",  # ← ИСПРАВЛЕНО
            role="Librarian"  # ← По спецификации
        )
        session.add(user)
        session.commit()
        print("✅ User 'admin' added successfully")

if __name__ == "__main__":
    main()