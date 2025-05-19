from fastapi import APIRouter, HTTPException, status, Form
from version1.auth.utils.jwt_utils import create_access_token

router = APIRouter()


@router.post("/login")
def login(
    username: str = Form(..., example=""), 
    password: str = Form(..., example="")
):
    if username == "pharma" and password == "1234":
        token = create_access_token({"sub": "pharma"})
    elif username == "coop" and password == "1234":
        token = create_access_token({"sub": "coop"})
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")

    return {"access_token": token, "token_type": "bearer"}
