import re
from Models.user import User


def validate_username(username):
    """
    Valida o username
    """
    if not username or not isinstance(username, str):
        raise Exception("Invalid username")


def validate_password(password):
    """
    Valida a senha com regras:
    - mínimo 6 caracteres
    - pelo menos 1 número
    - pelo menos 1 letra maiúscula
    """

    if not password or not isinstance(password, str):
        raise Exception("Invalid password")

    if len(password) < 6:
        raise Exception("Password too short")

    if not re.search(r"\d", password):
        raise Exception("Password must contain a number")

    if not re.search(r"[A-Z]", password):
        raise Exception("Password must contain an uppercase letter")


def create_user(db, username, password, role="admin"):
    """
    FUNÇÃO PRINCIPAL PARA CRIAR USUÁRIO
    """

    # ========================================
    # 1 - VALIDAÇÕES
    # ========================================
    validate_username(username)
    validate_password(password)

    if role is None:
        role = "admin"

    # ========================================
    # 2 - VERIFICAR DUPLICIDADE
    # ========================================
    existing_user = db.query(User).filter(User.username == username).first()

    if existing_user:
        raise Exception("User already exists")

    # ========================================
    # 3 - CRIAR USUÁRIO
    # ========================================
    new_user = User(
        username=username,
        password=password,
        role=role
    )

    # ========================================
    # 4 - SALVAR NO BANCO
    # ========================================
    db.add(new_user)
    db.commit()

    return new_user