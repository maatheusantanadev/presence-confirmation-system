import requests

@router.post("/attendance")
def mark_attendance(image: UploadFile, db: Session):

    # envia imagem para API externa
    response = requests.post(
        "http://sua-api-facial/recognize",
        files={"file": image.file}
    )

    result = response.json()

    if not result["recognized"]:
        return {"msg": "Aluno não reconhecido"}

    student_id = result["student_id"]

    attendance = Attendance(
        student_id=student_id,
        date=datetime.now(),
        status="presente"
    )

    db.add(attendance)
    db.commit()

    return {"msg": "Presença confirmada"}