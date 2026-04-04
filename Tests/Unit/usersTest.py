# Testes (1 ao 20) desenvolvidos por Matheus Santana

import unittest
from fastapi.testclient import TestClient
import sys, os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from main import app
from database import Base, get_db
from models import User
from utils import hash_password
from auth import create_token, get_admin_user

# Criar engine em memória
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False}
)

# Criar a conexão principal
connection = engine.connect()

# Vincular a sessão à conexão única
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=connection
)

# Criar tabelas na conexão
Base.metadata.create_all(bind=connection)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

# Criar todas as tabelas
Base.metadata.create_all(bind=engine)

client = TestClient(app)


# Mock do admin para testes
def override_get_admin_user():
    return {"sub": "adminuser", "role": "admin"}


app.dependency_overrides[get_admin_user] = override_get_admin_user


class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.db = TestingSessionLocal()
        # Limpar DB antes de cada teste
        self.db.query(User).delete()
        self.db.commit()

    def tearDown(self):
        self.db.close()

    # 1
    def test_create_user_success(self):
        response = client.post("/register", json={
            "username": "testuser",
            "password": "password123",
            "role": "admin"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("msg", response.json())

    # 2
    def test_create_user_short_username(self):
        response = client.post("/register", json={
            "username": "ab",
            "password": "password123",
            "role": "admin"
        })
        self.assertEqual(response.status_code, 422)

    # 3
    def test_create_user_short_password(self):
        response = client.post("/register", json={
            "username": "testuser2",
            "password": "pass1",
            "role": "admin"
        })
        self.assertEqual(response.status_code, 422)

    # 4
    def test_create_user_password_no_number(self):
        response = client.post("/register", json={
            "username": "testuser3",
            "password": "password",
            "role": "admin"
        })
        self.assertEqual(response.status_code, 422)

    # 5
    def test_login_success(self):
        user = User(username="loginuser", password=hash_password("abc12345"), role="admin")
        self.db.add(user)
        self.db.commit()

        response = client.post("/login", data={"username": "loginuser", "password": "abc12345"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())

    # 6
    def test_login_invalid_user(self):
        response = client.post("/login", data={"username": "nouser", "password": "abc12345"})
        self.assertEqual(response.status_code, 401)

    # 7
    def test_login_invalid_password(self):
        user = User(username="userpass", password=hash_password("abc12345"), role="admin")
        self.db.add(user)
        self.db.commit()

        response = client.post("/login", data={"username": "userpass", "password": "wrongpass"})
        self.assertEqual(response.status_code, 401)

    # 8
    def test_logout(self):
        response = client.post("/logout")
        self.assertEqual(response.status_code, 200)
        self.assertIn("msg", response.json())

    # 9
    def test_delete_user_success(self):
        user = User(username="todelete", password=hash_password("abc12345"), role="admin")
        self.db.add(user)
        self.db.commit()
        user_id = user.id

        response = client.delete(f"/{user_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("msg", response.json())

    # 10
    def test_delete_user_not_found(self):
        response = client.delete("/999")
        self.assertEqual(response.status_code, 404)

    # 11
    def test_create_multiple_users(self):
        for i in range(5):
            response = client.post("/register", json={
                "username": f"user{i}",
                "password": f"pass{i}123",
                "role": "student"
            })
            self.assertEqual(response.status_code, 200)

    # 12
    def test_create_duplicate_username(self):
        client.post("/register", json={
            "username": "dupuser",
            "password": "password123",
            "role": "admin"
        })
        response = client.post("/register", json={
            "username": "dupuser",
            "password": "password123",
            "role": "admin"
        })
        self.assertEqual(response.status_code, 400)

    # 13
    def test_password_number_end(self):
        response = client.post("/register", json={
            "username": "numend",
            "password": "password9",
            "role": "admin"
        })
        self.assertEqual(response.status_code, 200)

    # 14
    def test_empty_role(self):
        response = client.post("/register", json={
            "username": "norole",
            "password": "pass1234",
            "role": ""
        })
        self.assertEqual(response.status_code, 422)

    # 15
    def test_login_uppercase_username(self):
        user = User(username="CaseUser".lower(), password=hash_password("pass1234"), role="admin")
        self.db.add(user)
        self.db.commit()
        response = client.post("/login", data={"username": "CaseUser", "password": "pass1234"})
        self.assertEqual(response.status_code, 200)

    # 16
    def test_delete_user_twice(self):
        user = User(username="doubledelete", password=hash_password("abc12345"), role="admin")
        self.db.add(user)
        self.db.commit()
        user_id = user.id
        client.delete(f"/{user_id}")
        response = client.delete(f"/{user_id}")
        self.assertEqual(response.status_code, 404)

    # 17
    def test_username_max_length(self):
        response = client.post("/register", json={
            "username": "u" * 20,
            "password": "password1",
            "role": "admin"
        })
        self.assertEqual(response.status_code, 200)

    # 18
    def test_username_too_long(self):
        response = client.post("/register", json={
            "username": "u" * 21,
            "password": "password1",
            "role": "admin"
        })
        self.assertEqual(response.status_code, 422)

    # 19
    def test_password_multiple_numbers(self):
        response = client.post("/register", json={
            "username": "multinums",
            "password": "pass1234word",
            "role": "admin"
        })
        self.assertEqual(response.status_code, 200)

    # 20
    def test_login_deleted_user(self):
        user = User(username="tobedeleted", password=hash_password("abc12345"), role="admin")
        self.db.add(user)
        self.db.commit()
        user_id = user.id
        client.delete(f"/{user_id}")
        response = client.post("/login", data={"username": "tobedeleted", "password": "abc12345"})
        self.assertEqual(response.status_code, 401)


if __name__ == "__main__":
    unittest.main()
