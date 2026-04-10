from Models.students import Student


def create_student(name: str, email: str, db):
    """
    REGRA DE NEGÓCIO:
    - validar nome
    - validar email
    - evitar duplicidade
    """

    # ---------------------------------------------------------
    # REGRA 1 - Nome não pode ser vazio
    # ---------------------------------------------------------
    if not name or not name.strip():
        raise ValueError("Nome inválido")

    name = name.strip()

    # ---------------------------------------------------------
    # REGRA 2 - Email não pode ser vazio
    # ---------------------------------------------------------
    if not email:
        raise ValueError("Email inválido")

    # ---------------------------------------------------------
    # REGRA 3 - Email deve conter '@'
    # ---------------------------------------------------------
    if "@" not in email:
        raise ValueError("Email inválido")

    # ---------------------------------------------------------
    # REGRA 4 - Não permitir duplicidade
    # ---------------------------------------------------------
    existing = db.query(Student).filter_by(email=email).first()
    if existing:
        raise ValueError("Email já cadastrado")

    # ---------------------------------------------------------
    # CRIAÇÃO DO OBJETO
    # ---------------------------------------------------------
    student = Student(name=name, email=email)

    db.add(student)
    db.commit()

    return student