from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def authenticate_user(
    db: Session,
    username: str,
    password: str,
) -> str | None:
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    
    if not verify_password(password, user.hashed_password):
        return None
    
    return create_access_token(
        subject=str(user.id),
        role=user.role
    )
