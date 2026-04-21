from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import models.user as user_models
import schemas.auth_schema as auth_schemas
from database import get_db

SECRET_KEY = "SANGAT_RAHASIA_SMART_FARMING"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter(prefix="/auth", tags=["Authentication"])


# --- FUNGSI HELPER ---

def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Decode dan verifikasi JWT token, lalu kembalikan user dari database."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token tidak valid atau sudah kadaluarsa",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(user_models.User).filter(user_models.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user


# --- ENDPOINT AUTH ---

@router.post(
    "/register",
    response_model=auth_schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrasi User Baru",
    description="Mendaftarkan user baru dengan username unik dan password yang di-hash menggunakan bcrypt."
)
def register(user: auth_schemas.UserCreate, db: Session = Depends(get_db)):
    # Cek apakah username sudah terdaftar
    existing_user = db.query(user_models.User).filter(
        user_models.User.username == user.username
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username sudah terdaftar"
        )

    # Buat user baru dengan password yang di-hash
    db_user = user_models.User(
        username=user.username,
        hashed_password=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post(
    "/login",
    response_model=auth_schemas.Token,
    summary="Login User",
    description="Autentikasi user dengan username dan password. Mengembalikan JWT access token jika berhasil."
)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Cari user di database
    user = db.query(user_models.User).filter(
        user_models.User.username == form_data.username
    ).first()

    # Verifikasi user dan password
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username atau password salah",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate JWT token
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}