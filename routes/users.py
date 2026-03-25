@router.post("/register")
def register(user: UserCreate, db: Session):
    db_user = User(
        username=user.username,
        password=user.password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    return {"msg": "User criado"}