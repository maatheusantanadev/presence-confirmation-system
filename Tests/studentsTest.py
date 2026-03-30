# Testes (1 ao 20) desenvolvidos por Francisco Pedro

import unittest
from fastapi.testclient import TestClient
import sys, os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Permite importar arquivos da raiz do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app
from database import Base, get_db
from models import Student
from auth import get_admin_user


# CONFIGURAÇÃO DO BANCO DE TESTE

# Cria um banco SQLite em memória (não salva dados em disco)
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False}
)

# Mantém uma única conexão ativa para os testes
connection = engine.connect()

# Cria uma sessão de banco vinculada à conexão
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=connection
)

# Cria as tabelas no banco em memória
Base.metadata.create_all(bind=connection)


# OVERRIDE DO BANCO

# Substitui a dependência original do FastAPI (get_db)
# para usar o banco de testes
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


# Cliente de testes do FastAPI
client = TestClient(app)


# MOCK DE AUTENTICAÇÃO

# Simula um usuário admin para liberar acesso às rotas protegidas
def override_get_admin_user():
    return {"sub": "adminuser", "role": "admin"}


app.dependency_overrides[get_admin_user] = override_get_admin_user


# CLASSE DE TESTES

class TestStudentEndpoints(unittest.TestCase):

    # Executado antes de cada teste
    def setUp(self):
        self.db = TestingSessionLocal()

        # Limpa a tabela de estudantes
        self.db.query(Student).delete()
        self.db.commit()

    # Executado após cada teste
    def tearDown(self):
        self.db.close()


    # TESTES DE LISTAGEM (GET)

    # 1. Deve retornar lista vazia
    def test_list_students_empty(self):
        response = client.get("/students")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    # 2. Deve retornar alunos cadastrados
    def test_list_students_with_data(self):
        student = Student(name="Pedro", email="pedro@gmail.com")
        self.db.add(student)
        self.db.commit()

        response = client.get("/students")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) > 0)


    # TESTES DE CRIAÇÃO (POST)

    # 3. Criar aluno com dados válidos
    def test_create_student_success(self):
        response = client.post("/students", json={
            "name": "Joao",
            "email": "joao@gmail.com"
        })
        self.assertEqual(response.status_code, 200)

    # 4. Não permitir email duplicado
    def test_create_student_duplicate_email(self):
        student = Student(name="Maria", email="maria@gmail.com")
        self.db.add(student)
        self.db.commit()

        response = client.post("/students", json={
            "name": "Outra",
            "email": "maria@gmail.com"
        })
        self.assertEqual(response.status_code, 400)

    # 5. Não permitir email inválido
    def test_create_student_invalid_email(self):
        response = client.post("/students", json={
            "name": "Teste",
            "email": "email-invalido"
        })
        self.assertEqual(response.status_code, 422)

    # 6. Não permitir nome inválido
    def test_create_student_invalid_name(self):
        response = client.post("/students", json={
            "name": "",
            "email": "teste@gmail.com"
        })
        self.assertEqual(response.status_code, 422)


    # TESTES DE ATUALIZAÇÃO (PUT)

    # 7. Atualizar aluno com sucesso
    def test_update_student_success(self):
        student = Student(name="Ana", email="ana@gmail.com")
        self.db.add(student)
        self.db.commit()

        response = client.put(f"/students/{student.id}", json={
            "name": "Ana Updated",
            "email": "ana2@gmail.com"
        })
        self.assertEqual(response.status_code, 200)

    # 8. Atualizar aluno inexistente
    def test_update_student_not_found(self):
        response = client.put("/students/999", json={
            "name": "Teste",
            "email": "teste@gmail.com"
        })
        self.assertEqual(response.status_code, 404)

    # 9. Não permitir email duplicado na atualização
    def test_update_student_duplicate_email(self):
        s1 = Student(name="A", email="a@gmail.com")
        s2 = Student(name="B", email="b@gmail.com")
        self.db.add_all([s1, s2])
        self.db.commit()

        response = client.put(f"/students/{s1.id}", json={
            "name": "A",
            "email": "b@gmail.com"
        })
        self.assertEqual(response.status_code, 400)

    # 10. Não permitir email inválido na atualização
    def test_update_student_invalid_email(self):
        student = Student(name="Teste", email="teste@gmail.com")
        self.db.add(student)
        self.db.commit()

        response = client.put(f"/students/{student.id}", json={
            "name": "Novo",
            "email": "invalido"
        })
        self.assertEqual(response.status_code, 422)


    # TESTES DE REMOÇÃO (DELETE)

    # 11. Deletar aluno com sucesso
    def test_delete_student_success(self):
        student = Student(name="Carlos", email="carlos@gmail.com")
        self.db.add(student)
        self.db.commit()

        response = client.delete(f"/students/{student.id}")
        self.assertEqual(response.status_code, 200)

    # 12. Deletar aluno inexistente
    def test_delete_student_not_found(self):
        response = client.delete("/students/999")
        self.assertEqual(response.status_code, 404)


    # TESTES COMPLEMENTARES

    # 13. Criar múltiplos alunos
    def test_create_multiple_students(self):
        for i in range(3):
            response = client.post("/students", json={
                "name": f"Aluno{i}",
                "email": f"aluno{i}@gmail.com"
            })
            self.assertEqual(response.status_code, 200)

    # 14. Atualizar várias vezes o mesmo aluno
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

    # 15. Tentar deletar duas vezes
    def test_delete_twice(self):
        student = Student(name="Del", email="del@gmail.com")
        self.db.add(student)
        self.db.commit()

        client.delete(f"/students/{student.id}")
        response = client.delete(f"/students/{student.id}")
        self.assertEqual(response.status_code, 404)

    # 16. Verifica se o aluno foi salvo no banco
    def test_student_saved_in_db(self):
        client.post("/students", json={
            "name": "DBTest",
            "email": "db@gmail.com"
        })

        student = self.db.query(Student).filter_by(email="db@gmail.com").first()
        self.assertIsNotNone(student)

    # 17. Verifica se o ID permanece após update
    def test_update_keeps_id(self):
        student = Student(name="ID", email="id@gmail.com")
        self.db.add(student)
        self.db.commit()

        response = client.put(f"/students/{student.id}", json={
            "name": "Novo",
            "email": "novo@gmail.com"
        })

        self.assertEqual(response.json()["id"], student.id)

    # 18. Nome apenas com espaços não é permitido
    def test_create_student_name_only_spaces(self):
        response = client.post("/students", json={
            "name": "   ",
            "email": "space@gmail.com"
        })
        self.assertEqual(response.status_code, 422)

    # 19. Atualização com nome inválido (espaços)
    def test_update_student_name_only_spaces(self):
        student = Student(name="Teste", email="teste2@gmail.com")
        self.db.add(student)
        self.db.commit()

        response = client.put(f"/students/{student.id}", json={
            "name": "   ",
            "email": "novo2@gmail.com"
        })
        self.assertEqual(response.status_code, 422)

    # 20. Nome no tamanho máximo permitido
    def test_create_student_max_name_length(self):
        response = client.post("/students", json={
            "name": "A" * 50,
            "email": "max@gmail.com"
        })
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
    
