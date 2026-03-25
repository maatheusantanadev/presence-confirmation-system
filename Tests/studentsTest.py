# Testes (1 ao 20) desenvolvidos por Francisco Pedro

import unittest
from fastapi.testclient import TestClient
import sys, os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app
from database import Base, get_db
from models import Student
from auth import get_admin_user

# Banco em memória
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False}
)

connection = engine.connect()

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=connection
)

Base.metadata.create_all(bind=connection)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


# Mock admin
def override_get_admin_user():
    return {"sub": "adminuser", "role": "admin"}


app.dependency_overrides[get_admin_user] = override_get_admin_user


class TestStudentEndpoints(unittest.TestCase):

    def setUp(self):
        self.db = TestingSessionLocal()
        self.db.query(Student).delete()
        self.db.commit()

    def tearDown(self):
        self.db.close()

    # 1
    def test_list_students_empty(self):
        response = client.get("/students")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    # 2
    def test_list_students_with_data(self):
        student = Student(name="Pedro", email="pedro@gmail.com")
        self.db.add(student)
        self.db.commit()

        response = client.get("/students")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) > 0)

    # 3
    def test_create_student_success(self):
        response = client.post("/students", json={
            "name": "Joao",
            "email": "joao@gmail.com"
        })
        self.assertEqual(response.status_code, 200)

    # 4
    def test_create_student_duplicate_email(self):
        student = Student(name="Maria", email="maria@gmail.com")
        self.db.add(student)
        self.db.commit()

        response = client.post("/students", json={
            "name": "Outra",
            "email": "maria@gmail.com"
        })
        self.assertEqual(response.status_code, 400)

    # 5
    def test_create_student_invalid_email(self):
        response = client.post("/students", json={
            "name": "Teste",
            "email": "email-invalido"
        })
        self.assertEqual(response.status_code, 422)

    # 6
    def test_create_student_invalid_name(self):
        response = client.post("/students", json={
            "name": "",
            "email": "teste@gmail.com"
        })
        self.assertEqual(response.status_code, 422)

    # 7
    def test_update_student_success(self):
        student = Student(name="Ana", email="ana@gmail.com")
        self.db.add(student)
        self.db.commit()

        response = client.put(f"/students/{student.id}", json={
            "name": "Ana Updated",
            "email": "ana2@gmail.com"
        })
        self.assertEqual(response.status_code, 200)

    # 8
    def test_update_student_not_found(self):
        response = client.put("/students/999", json={
            "name": "Teste",
            "email": "teste@gmail.com"
        })
        self.assertEqual(response.status_code, 404)

    # 9
    def test_update_student_duplicate_email(self):
        s1 = Student(name="A", email="a@gmail.com")
        s2 = Student(name="B", email="b@gmail.com")
        self.db.add_all([s1, s2])
        self.db.commit()

        response = client.put(f"/students/{s1.id}", json={
            "name": "A",
            "email": "b@gmail.com"
        })
        self.assertEqual(response.status_code, 422)

    # 10
    def test_update_student_invalid_email(self):
        student = Student(name="Teste", email="teste@gmail.com")
        self.db.add(student)
        self.db.commit()

        response = client.put(f"/students/{student.id}", json={
            "name": "Novo",
            "email": "invalido"
        })
        self.assertEqual(response.status_code, 422)

    # 11
    def test_delete_student_success(self):
        student = Student(name="Carlos", email="carlos@gmail.com")
        self.db.add(student)
        self.db.commit()

        response = client.delete(f"/students/{student.id}")
        self.assertEqual(response.status_code, 200)

    # 12
    def test_delete_student_not_found(self):
        response = client.delete("/students/999")
        self.assertEqual(response.status_code, 404)

    # 13
    def test_create_multiple_students(self):
        for i in range(3):
            response = client.post("/students", json={
                "name": f"Aluno{i}",
                "email": f"aluno{i}@gmail.com"
            })
            self.assertEqual(response.status_code, 200)

    # 14
    def test_update_multiple_times(self):
        student = Student(name="Loop", email="loop@gmail.com")
        self.db.add(student)
        self.db.commit()

        for i in range(3):
            response = client.put(f"/students/{student.id}", json={
                "name": f"Loop{i}",
                "email": f"loop{i}@gmail.com"
            })
            self.assertEqual(response.status_code, 200)

    # 15
    def test_delete_twice(self):
        student = Student(name="Del", email="del@gmail.com")
        self.db.add(student)
        self.db.commit()

        client.delete(f"/students/{student.id}")
        response = client.delete(f"/students/{student.id}")
        self.assertEqual(response.status_code, 404)

    # 16
    def test_student_saved_in_db(self):
        client.post("/students", json={
            "name": "DBTest",
            "email": "db@gmail.com"
        })

        student = self.db.query(Student).filter_by(email="db@gmail.com").first()
        self.assertIsNotNone(student)

    # 17
    def test_update_keeps_id(self):
        student = Student(name="ID", email="id@gmail.com")
        self.db.add(student)
        self.db.commit()

        response = client.put(f"/students/{student.id}", json={
            "name": "Novo",
            "email": "novo@gmail.com"
        })

        self.assertEqual(response.json()["id"], student.id)

    # 18
    def test_create_student_name_only_spaces(self):
        response = client.post("/students", json={
            "name": "   ",
            "email": "space@gmail.com"
        })
        self.assertEqual(response.status_code, 422)

    # 19
    def test_update_student_name_only_spaces(self):
        student = Student(name="Teste", email="teste2@gmail.com")
        self.db.add(student)
        self.db.commit()

        response = client.put(f"/students/{student.id}", json={
            "name": "   ",
            "email": "novo2@gmail.com"
        })
        self.assertEqual(response.status_code, 422)

    # 20
    def test_create_student_max_name_length(self):
        response = client.post("/students", json={
            "name": "A" * 50,
            "email": "max@gmail.com"
        })
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
    
