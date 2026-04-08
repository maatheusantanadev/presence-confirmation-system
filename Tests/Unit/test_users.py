# Testes (1 ao 20) desenvolvidos por Henrique Souza

import pytest
from pydantic import ValidationError
from Schemas.user import UserCreate


# =========================================================
# TESTE 1
# =========================================================
def test_1_create_user_success():
    """
    TESTE 1: Criar usuário válido
    """

    # 1 - CENÁRIO
    data = {"username": "manson", "password": "Password123", "role": "admin"}

    # 2 - EXECUÇÃO
    user = UserCreate(**data)

    # 3 - VALIDAÇÃO
    assert user.username == "manson"


# =========================================================
# TESTE 2
# =========================================================
def test_2_password_sem_numero():
    """
    TESTE 2: Senha sem número
    """

    # 1 - CENÁRIO
    data = {"username": "manson", "password": "Password", "role": "admin"}

    # 2 - EXECUÇÃO + VALIDAÇÃO
    with pytest.raises(ValidationError):
        UserCreate(**data)


# =========================================================
# TESTE 3
# =========================================================
def test_3_password_sem_maiuscula():
    """
    TESTE 3: Senha sem maiúscula
    """

    # 1 - CENÁRIO
    data = {"username": "manson", "password": "password123", "role": "admin"}

    # 2 - EXECUÇÃO + VALIDAÇÃO
    with pytest.raises(ValidationError):
        UserCreate(**data)


# =========================================================
# TESTE 4
# =========================================================
def test_4_password_curta():
    """
    TESTE 4: Senha curta
    """

    # 1 - CENÁRIO
    data = {"username": "manson", "password": "P1a", "role": "admin"}

    # 2 - EXECUÇÃO + VALIDAÇÃO
    with pytest.raises(ValidationError):
        UserCreate(**data)


# =========================================================
# TESTE 5
# =========================================================
def test_5_username_vazio():
    """
    TESTE 5: Username vazio
    """

    # 1 - CENÁRIO
    data = {"username": "", "password": "Password123", "role": "admin"}

    # 2 - EXECUÇÃO + VALIDAÇÃO
    with pytest.raises(ValidationError):
        UserCreate(**data)


# =========================================================
# TESTE 6
# =========================================================
def test_6_role_default():
    """
    TESTE 6: Role padrão
    """

    # 1 - CENÁRIO
    data = {"username": "manson", "password": "Password123"}

    # 2 - EXECUÇÃO
    user = UserCreate(**data)

    # 3 - VALIDAÇÃO
    assert user.role == "admin"


# =========================================================
# TESTE 7
# =========================================================
def test_7_username_com_espaco():
    """
    TESTE 7: Username com espaço
    """

    # 1 - CENÁRIO
    data = {"username": "man son", "password": "Password123", "role": "admin"}

    # 2 - EXECUÇÃO
    user = UserCreate(**data)

    # 3 - VALIDAÇÃO
    assert user.username == "man son"


# =========================================================
# TESTE 8
# =========================================================
def test_8_password_com_caractere_especial():
    """
    TESTE 8: Senha com caractere especial
    """

    # 1 - CENÁRIO
    data = {"username": "manson", "password": "Password@123", "role": "admin"}

    # 2 - EXECUÇÃO
    user = UserCreate(**data)

    # 3 - VALIDAÇÃO
    assert user.password == "Password@123"


# =========================================================
# TESTE 9
# =========================================================
def test_9_password_nula():
    """
    TESTE 9: Senha nula
    """

    # 1 - CENÁRIO
    data = {"username": "manson", "password": None, "role": "admin"}

    # 2 - EXECUÇÃO + VALIDAÇÃO
    with pytest.raises(ValidationError):
        UserCreate(**data)

# =========================================================
# TESTE 10
# =========================================================
def test_10_username_nulo():
    """
    TESTE 10: Username nulo
    """

    # 1 - CENÁRIO
    data = {"username": None, "password": "Password123", "role": "admin"}

    # 2 - EXECUÇÃO + VALIDAÇÃO
    with pytest.raises(ValidationError):
        UserCreate(**data)

# =========================================================
# TESTE 11
# =========================================================
def test_11_username_valido():
    """
    TESTE 11: Username válido
    """

    # 1 - CENÁRIO
    data = {"username": "user123", "password": "Password123", "role": "admin"}

    # 2 - EXECUÇÃO
    user = UserCreate(**data)

    # 3 - VALIDAÇÃO
    assert user.username == "user123"


# =========================================================
# TESTE 12
# =========================================================
def test_12_password_valida():
    """
    TESTE 12: Senha válida
    """

    # 1 - CENÁRIO
    data = {"username": "manson", "password": "Abc123", "role": "admin"}

    # 2 - EXECUÇÃO
    user = UserCreate(**data)

    # 3 - VALIDAÇÃO
    assert user.password == "Abc123"


# =========================================================
# TESTE 13
# =========================================================
def test_13_role_none():
    """
    TESTE 13: Role None vira padrão
    """

    # 1 - CENÁRIO
    data = {"username": "manson", "password": "Password123", "role": None}

    # 2 - EXECUÇÃO
    user = UserCreate(**data)

    # 3 - VALIDAÇÃO
    assert user.role == "admin"


# =========================================================
# TESTE 14
# =========================================================
def test_14_username_espacos():
    """
    TESTE 14: Username só com espaços
    """

    # 1 - CENÁRIO
    data = {"username": "   ", "password": "Password123", "role": "admin"}

    # 2 - EXECUÇÃO + VALIDAÇÃO
    with pytest.raises(ValidationError):
        UserCreate(**data)


# =========================================================
# TESTE 15
# =========================================================
def test_15_password_minimo_valido():
    """
    TESTE 15: Senha mínima válida
    """

    # 1 - CENÁRIO
    data = {"username": "manson", "password": "A1b2c3", "role": "admin"}

    # 2 - EXECUÇÃO
    user = UserCreate(**data)

    # 3 - VALIDAÇÃO
    assert user.password == "A1b2c3"


# =========================================================
# TESTE 16
# =========================================================
def test_16_password_sem_letra():
    """
    TESTE 16: Senha sem letra maiúscula válida
    """

    # 1 - CENÁRIO
    data = {"username": "manson", "password": "1234567", "role": "admin"}

    # 2 - EXECUÇÃO + VALIDAÇÃO
    with pytest.raises(ValidationError):
        UserCreate(**data)

# =========================================================
# TESTE 17
# =========================================================
def test_17_objeto_criado():
    """
    TESTE 17: Objeto criado corretamente
    """

    # 1 - CENÁRIO
    data = {"username": "manson", "password": "Password123", "role": "admin"}

    # 2 - EXECUÇÃO
    user = UserCreate(**data)

    # 3 - VALIDAÇÃO
    assert isinstance(user, UserCreate)


# =========================================================
# TESTE 18
# =========================================================
def test_18_password_com_numero_e_maiuscula():
    """
    TESTE 18: Senha válida com número e maiúscula
    """

    # 1 - CENÁRIO
    data = {"username": "manson", "password": "Test123", "role": "admin"}

    # 2 - EXECUÇÃO
    user = UserCreate(**data)

    # 3 - VALIDAÇÃO
    assert user.password == "Test123"


# =========================================================
# TESTE 19
# =========================================================
def test_19_username_normal():
    """
    TESTE 19: Username normal válido
    """

    # 1 - CENÁRIO
    data = {"username": "abc", "password": "Password123", "role": "admin"}

    # 2 - EXECUÇÃO
    user = UserCreate(**data)

    # 3 - VALIDAÇÃO
    assert user.username == "abc"


# =========================================================
# TESTE 20
# =========================================================
def test_20_password_invalida():
    """
    TESTE 20: Senha inválida geral
    """

    # 1 - CENÁRIO
    data = {"username": "manson", "password": "abc", "role": "admin"}

    # 2 - EXECUÇÃO + VALIDAÇÃO
    with pytest.raises(ValidationError):
        UserCreate(**data)
