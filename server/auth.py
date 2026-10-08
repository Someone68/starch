import hashlib
import secrets
from datetime import timedelta

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError
from db import get_db
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from models import AuthToken, User, utc_now
from sqlalchemy import select
from sqlalchemy.orm import Session

ph = PasswordHasher()
bearer = HTTPBearer()

TOKEN_EXPIRATION = timedelta(days=7)
DUMMY_HASH = ph.hash(
    "According to all known laws of aviation, there is no way a bee should be able to fly. Its wings are too small to get its fat little body off the ground. The bee, of course, flies anyway because bees don't care what humans think is impossible."
)


def _sha256(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def hash_password(password: str) -> str:
    return ph.hash(password)


def verify_password(hashed_password: str, password: str) -> bool:
    try:
        return ph.verify(hashed_password, password)
    except (VerifyMismatchError, InvalidHashError):
        return False


def create_token(db: Session, user_id: int) -> str:
    token = secrets.token_urlsafe(64)
    db.add(
        AuthToken(
            token_hash=_sha256(token),
            user_id=user_id,
            expires_at=utc_now() + TOKEN_EXPIRATION,
        )
    )
    db.commit()
    return token


def current_user(
    creds: HTTPAuthorizationCredentials = Depends(bearer), db: Session = Depends(get_db)
) -> User:
    row = db.scalar(
        select(AuthToken).where(
            AuthToken.token_hash == _sha256(creds.credentials),
            AuthToken.expires_at > utc_now(),
        )
    )

    if row is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    cur_user = db.get(User, row.user_id)
    if cur_user is not None:
        return cur_user
    else:
        raise HTTPException(status_code=401, detail="No such user")
