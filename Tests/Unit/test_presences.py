import pytest
from datetime import datetime, timedelta
from Schemas.presence import PresenceCreate
from fastapi.testclient import TestClient
from pydantic import ValidationError
from main import app

client = TestClient(app)

# =========================
# TESTES DE SCHEMA
# =========================

def test_status_valido_presente():
    # 1 - CRIANDO CENÁRIO
    data = {"student_id": 1, "status": "presente"}

    # 2 - EXECUÇÃO
    p = PresenceCreate(**data)

    # 3 - VALIDAÇÃO
    assert p.status == "presente"


def test_status_valido_ausente():
    # 1 - CRIANDO CENÁRIO
    data = {"student_id": 1, "status": "ausente"}

    # 2 - EXECUÇÃO
    p = PresenceCreate(**data)

    # 3 - VALIDAÇÃO
    assert p.status == "ausente"


def test_status_valido_justificado():
    # 1 - CRIANDO CENÁRIO
    data = {"student_id": 1, "status": "justificado"}

    # 2 - EXECUÇÃO
    p = PresenceCreate(**data)

    # 3 - VALIDAÇÃO
    assert p.status == "justificado"


def test_status_uppercase():
    # 1 - CRIANDO CENÁRIO
    data = {"student_id": 1, "status": "PRESENTE"}

    # 2 - EXECUÇÃO
    p = PresenceCreate(**data)

    # 3 - VALIDAÇÃO
    assert p.status == "presente"


def test_status_com_espaco():
    # 1 - CRIANDO CENÁRIO
    data = {"student_id": 1, "status": "  ausente "}

    # 2 - EXECUÇÃO
    p = PresenceCreate(**data)

    # 3 - VALIDAÇÃO
    assert p.status == "ausente"


def test_status_invalido():
    # 1 - CRIANDO CENÁRIO
    data = {"student_id": 1, "status": "faltou"}

    # 2 - EXECUÇÃO + 3 - VALIDAÇÃO
    with pytest.raises(ValueError):
        PresenceCreate(**data)


def test_data_valida_passado():
    # 1 - CRIANDO CENÁRIO
    data_passada = datetime.utcnow() - timedelta(days=1)

    # 2 - EXECUÇÃO
    p = PresenceCreate(student_id=1, date=data_passada)

    # 3 - VALIDAÇÃO
    assert p.date == data_passada


def test_data_igual_agora():
    # 1 - CRIANDO CENÁRIO
    agora = datetime.utcnow()

    # 2 - EXECUÇÃO
    p = PresenceCreate(student_id=1, date=agora)

    # 3 - VALIDAÇÃO
    assert p.date == agora


def test_data_futura():
    # 1 - CRIANDO CENÁRIO
    data_futura = datetime.utcnow() + timedelta(days=1)

    # 2 - EXECUÇÃO + 3 - VALIDAÇÃO
    with pytest.raises(ValueError):
        PresenceCreate(student_id=1, date=data_futura)


def test_student_id_obrigatorio():
    # 1 - CRIANDO CENÁRIO (sem student_id)

    # 2 - EXECUÇÃO + 3 - VALIDAÇÃO
    with pytest.raises(ValidationError):
        PresenceCreate()


# =========================
# TESTES DE API
# =========================

def test_rota_presenca_sucesso(monkeypatch):
    # 1 - CRIANDO CENÁRIO
    class MockResponse:
        def json(self):
            return {"success": True, "usuario": {"id": 1}}

    def mock_post(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("requests.post", mock_post)

    # 2 - EXECUÇÃO
    response = client.post(
        "/presence",
        files={"image": ("test.jpg", b"fake_image", "image/jpeg")}
    )

    # 3 - VALIDAÇÃO
    assert response.status_code == 200
    assert response.json()["msg"] == "Presença confirmada"


def test_rota_aluno_nao_reconhecido(monkeypatch):
    # 1 - CRIANDO CENÁRIO
    class MockResponse:
        def json(self):
            return {"success": False}

    def mock_post(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("requests.post", mock_post)

    # 2 - EXECUÇÃO
    response = client.post(
        "/presence",
        files={"image": ("test.jpg", b"fake", "image/jpeg")}
    )

    # 3 - VALIDAÇÃO
    assert response.status_code == 200
    assert response.json()["msg"] == "Aluno não reconhecido"


def test_rota_sem_imagem():
    # 1 - CRIANDO CENÁRIO (requisição sem arquivo)

    # 2 - EXECUÇÃO
    response = client.post("/presence")

    # 3 - VALIDAÇÃO
    assert response.status_code == 422


def test_resposta_tem_msg(monkeypatch):
    # 1 - CRIANDO CENÁRIO
    class MockResponse:
        def json(self):
            return {"success": False}

    def mock_post(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("requests.post", mock_post)

    # 2 - EXECUÇÃO
    response = client.post(
        "/presence",
        files={"image": ("test.jpg", b"fake", "image/jpeg")}
    )

    # 3 - VALIDAÇÃO
    assert "msg" in response.json()


def test_api_metodo_invalido():
    # 1 - CRIANDO CENÁRIO (método GET em rota POST)

    # 2 - EXECUÇÃO
    response = client.get("/presence")

    # 3 - VALIDAÇÃO
    assert response.status_code == 405


def test_upload_tipo_errado(monkeypatch):
    # 1 - CRIANDO CENÁRIO
    class MockResponse:
        def json(self):
            return {"success": False}

    def mock_post(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("requests.post", mock_post)

    # 2 - EXECUÇÃO
    response = client.post(
        "/presence",
        files={"image": ("test.txt", b"text", "text/plain")}
    )

    # 3 - VALIDAÇÃO
    assert response.status_code == 200


def test_retorno_json_valido(monkeypatch):
    # 1 - CRIANDO CENÁRIO
    class MockResponse:
        def json(self):
            return {"success": True, "usuario": {"id": 2}}

    def mock_post(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("requests.post", mock_post)

    # 2 - EXECUÇÃO
    response = client.post(
        "/presence",
        files={"image": ("img.jpg", b"img", "image/jpeg")}
    )

    # 3 - VALIDAÇÃO
    assert isinstance(response.json(), dict)


def test_status_padrao_schema():
    # 1 - CRIANDO CENÁRIO (sem status)

    # 2 - EXECUÇÃO
    p = PresenceCreate(student_id=1)

    # 3 - VALIDAÇÃO
    assert p.status == "presente"


def test_date_padrao_none():
    # 1 - CRIANDO CENÁRIO (sem date)

    # 2 - EXECUÇÃO
    p = PresenceCreate(student_id=1)

    # 3 - VALIDAÇÃO
    assert p.date is None


def test_string_status_strip_lower():
    # 1 - CRIANDO CENÁRIO
    data = {"student_id": 1, "status": "  JUSTIFICADO "}

    # 2 - EXECUÇÃO
    p = PresenceCreate(**data)

    # 3 - VALIDAÇÃO
    assert p.status == "justificado"


def test_multiplas_criacoes_validas():
    # 1 - CRIANDO CENÁRIO
    status_list = ["presente", "ausente", "justificado"]

    # 2 - EXECUÇÃO + 3 - VALIDAÇÃO
    for status in status_list:
        p = PresenceCreate(student_id=1, status=status)
        assert p.status == status