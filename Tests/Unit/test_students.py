# Testes (1 ao 20) desenvolvidos por Francisco Pedro

import pytest
from Services.studentes_service import create_student


# =========================================================
# MOCK DE BANCO (FakeDB)
# =========================================================

class FakeDB:
    """
    Simula um banco de dados.
    Não usa SQL real.
    """

    def __init__(self, existing_email=None):
        self.existing_email = existing_email
        self.saved_objects = []

    def query(self, *args, **kwargs):
        return self

    def filter_by(self, **kwargs):
        self.email = kwargs.get("email")
        return self

    def first(self):
        if self.email == self.existing_email:
            return {"email": self.email}
        return None

    def add(self, obj):
        self.saved_objects.append(obj)

    def commit(self):
        pass


# =========================================================
# TESTES (1 AO 20)
# =========================================================


def test_01_create_student_success():
    # 1 - CRIANDO CENÁRIO
    db = FakeDB()

    # 2 - EXECUÇÃO
    result = create_student("Pedro", "pedro@gmail.com", db)

    # 3 - VALIDAÇÃO
    assert result.name == "Pedro"
    assert result.email == "pedro@gmail.com"


def test_02_nome_vazio():
    db = FakeDB()
    with pytest.raises(ValueError):
        create_student("", "email@gmail.com", db)


def test_03_nome_espacos():
    db = FakeDB()
    with pytest.raises(ValueError):
        create_student("   ", "email@gmail.com", db)


def test_04_email_invalido():
    db = FakeDB()
    with pytest.raises(ValueError):
        create_student("Pedro", "emailinvalido", db)


def test_05_email_duplicado():
    db = FakeDB(existing_email="pedro@gmail.com")
    with pytest.raises(ValueError):
        create_student("Pedro", "pedro@gmail.com", db)


def test_06_email_vazio():
    db = FakeDB()
    with pytest.raises(ValueError):
        create_student("Pedro", "", db)


def test_07_nome_maximo():
    db = FakeDB()
    result = create_student("A"*50, "max@gmail.com", db)
    assert len(result.name) == 50


def test_08_nome_minimo():
    db = FakeDB()
    result = create_student("A", "a@gmail.com", db)
    assert result.name == "A"


def test_09_email_com_espaco():
    db = FakeDB()
    with pytest.raises(ValueError):
        create_student("Pedro", "email @gmail.com", db)


def test_10_multiplos_students():
    db = FakeDB()
    create_student("A", "a@gmail.com", db)
    create_student("B", "b@gmail.com", db)
    assert len(db.saved_objects) == 2


def test_11_nome_caracter_especial():
    db = FakeDB()
    result = create_student("João!", "joao@gmail.com", db)
    assert result.name == "João!"


def test_12_nome_numerico():
    db = FakeDB()
    result = create_student("123", "num@gmail.com", db)
    assert result.name == "123"


def test_13_trim_nome():
    db = FakeDB()
    result = create_student(" Pedro ", "pedro@gmail.com", db)
    assert result.name == "Pedro"


def test_14_retorna_objeto():
    db = FakeDB()
    result = create_student("Pedro", "pedro@gmail.com", db)
    assert result is not None


def test_15_salva_no_mock():
    db = FakeDB()
    create_student("Pedro", "pedro@gmail.com", db)
    assert len(db.saved_objects) == 1


def test_16_email_uppercase():
    db = FakeDB()
    result = create_student("Pedro", "PEDRO@GMAIL.COM", db)
    assert result.email == "PEDRO@GMAIL.COM"


def test_17_email_longo():
    db = FakeDB()
    email = "a"*30 + "@gmail.com"
    result = create_student("Pedro", email, db)
    assert result.email == email


def test_18_email_com_ponto():
    db = FakeDB()
    result = create_student("Pedro", "pedro.silva@gmail.com", db)
    assert "." in result.email


def test_19_email_subdominio():
    db = FakeDB()
    result = create_student("Pedro", "pedro@mail.com", db)
    assert "@mail.com" in result.email


def test_20_case_sensitive():
    db = FakeDB()
    result = create_student("Pedro", "Pedro@Gmail.com", db)
    assert result.email == "Pedro@Gmail.com"