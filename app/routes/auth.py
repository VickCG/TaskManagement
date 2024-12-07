from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from pydantic import BaseModel
from app.database import get_db
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserResponse, TokenData
from app.services.auth_service import AuthService
from app.config import get_settings

class LoginRequest(BaseModel):
    username: str
    password: str


settings = get_settings()

ERROR_MESSAGES = {
    "invalid_token": "Invalid token",
    "user_not_found": "Incorrect username or password",
    "missing_credentials": "Username and password are required",
    "user_exists": "Username or email already registered",
}

router = APIRouter(prefix="/auth", tags=["authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def raise_http_exception(status_code: int, message_key: str):
    detail = ERROR_MESSAGES.get(message_key, "Unknown error")
    raise HTTPException(status_code=status_code, detail=detail)


def get_user_by_username(db: Session, username: str) -> User:
    return db.query(User).filter(User.username == username).first()


def authenticate_user(db: Session, username: str, password: str) -> User:
    user = get_user_by_username(db, username)
    if not user or not AuthService.verify_password(password, user.hashed_password):
        return None
    return user


def decode_jwt_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise_http_exception(status.HTTP_401_UNAUTHORIZED, "invalid_token")
        return TokenData(username=username)
    except JWTError:
        raise_http_exception(status.HTTP_401_UNAUTHORIZED, "invalid_token")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    token_data = decode_jwt_token(token)
    user = get_user_by_username(db, token_data.username)
    if user is None:
        raise_http_exception(status.HTTP_401_UNAUTHORIZED, "invalid_token")
    return user


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter((User.username == user.username) | (User.email == user.email)).first():
        raise_http_exception(status.HTTP_409_CONFLICT, "user_exists")
    
    hashed_password = AuthService.get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", status_code=status.HTTP_200_OK)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    username = login_data.username
    password = login_data.password
    
    if not username or not password:
        raise_http_exception(status.HTTP_400_BAD_REQUEST, "missing_credentials")
    
    user = authenticate_user(db, username, password)
    if not user:
        raise_http_exception(status.HTTP_401_UNAUTHORIZED, "user_not_found")
    
    access_token = AuthService.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
