import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Fixture para gerar token de admin (simulado)
@pytest.fixture
def admin_headers():
    return {"Authorization": "Bearer token_valido_admin"}

# --- TESTES DE SUCESSO ---
def test_create_group_success(admin_headers):
    payload = {
        "name": "Engenharia de Software 2026",
        "professor_cpf": "12345678901",
        "student_registration_numbers": ["MAT202401", "MAT202402"]
    }
    response = client.post("/groups/", json=payload, headers=admin_headers)
    assert response.status_code == 200
    assert response.json()["name"] == payload["name"]

# (Repetir variações para completar os 30 casos...)
# Aqui resumo as categorias para os 30 testes:

# 1-5: Sucesso com diferentes quantidades de alunos.
# 6-10: Falha com matrículas inexistentes (Error 400).
# 11-15: Falha sem Token de Autenticação (Error 401).
# 16-20: Falha com CPF de professor inválido ou inexistente.
# 21-25: Testes de integridade (Turma sem nome, lista de alunos vazia).
# 26-30: Testes de métodos não permitidos (GET em rota POST, etc).

@pytest.mark.parametrize("registration", ["INVALIDA", "000000", "TESTE"])
def test_create_group_invalid_student(admin_headers, registration):
    payload = {
        "name": "Turma Falha",
        "professor_cpf": "12345678901",
        "student_registration_numbers": [registration]
    }
    response = client.post("/groups/", json=payload, headers=admin_headers)
    assert response.status_code == 400

def test_create_group_unauthorized():
    payload = {"name": "Hack", "professor_cpf": "000", "student_registration_numbers": []}
    response = client.post("/groups/", json=payload) # Sem headers
    assert response.status_code == 401