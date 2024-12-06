from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from app.database import get_db
from app.models import User, Role
from sqlalchemy.orm import Session

SECRET_KEY = "your_jwt_secret"
ALGORITHM = "HS256"

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

def get_current_employer(user: User = Depends(get_current_user)):
    if user.role != Role.employer:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
    return user

def get_current_employee(user: User = Depends(get_current_user)):
    if user.role != Role.employee:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
    return user
