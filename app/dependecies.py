from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Role
from app.config import get_settings

settings = get_settings()

def raise_http_exception(status_code, detail):
    raise HTTPException(status_code=status_code, detail=detail)

def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise_http_exception(status.HTTP_401_UNAUTHORIZED, "Invalid token")
        return username
    except JWTError:
        raise_http_exception(status.HTTP_401_UNAUTHORIZED, "Invalid token")

def get_current_user(
    db: Session = Depends(get_db), 
    token: str = Depends(oauth2_scheme)
):
    username = decode_jwt_token(token)
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise_http_exception(status.HTTP_401_UNAUTHORIZED, "Invalid token")
    return user

def check_user_role(user: User, required_role: Role):
    if user.role != required_role:
        raise_http_exception(status.HTTP_403_FORBIDDEN, "Permission denied")
    return user

def get_current_employer(user: User = Depends(get_current_user)):
    return check_user_role(user, Role.employer)

def get_current_employee(user: User = Depends(get_current_user)):
    return check_user_role(user, Role.employee)
