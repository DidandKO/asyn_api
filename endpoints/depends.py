from core.security import JWTBearer, decode_access_token
from models.user import User
from repositories.jobs import JobRepository
from repositories.users import UserRepository
from db.base import database
from fastapi import Depends, HTTPException, status


def get_user_repository() -> UserRepository:
    return UserRepository(database)


def get_job_repository() -> JobRepository:
    return JobRepository(database)


async def get_current_user(user: UserRepository = Depends(get_user_repository),
                     token: str = Depends(JWTBearer())) -> User:
    cred_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credential are not valid")
    payload = decode_access_token(token)
    if payload is None:
        raise cred_exception

    email: str = payload.get("sub")
    if email is None:
        raise cred_exception

    user: User = await user.get_by_email(email=email)
    if user is None:
        raise cred_exception
    return user
