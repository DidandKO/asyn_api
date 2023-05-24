from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from models.user import User, UserIn
from repositories.users import UserRepository
from endpoints.depends import get_user_repository, get_current_user

router = APIRouter()


@router.get("/", response_model=List[User])
async def read_users(users: UserRepository = Depends(get_user_repository),
                     limit: int = 100,
                     skip: int = 0):
    return await users.get_all(limit=limit, skip=skip)


@router.post("/", response_model=User)
async def create(user: UserIn,
                 users: UserRepository = Depends(get_user_repository)):
    return await users.create(u=user)


@router.put("/", response_model=User)
async def update_user(id: int,
                      user: UserIn,
                      users: UserRepository = Depends(get_user_repository),
                      current_user: User = Depends(get_current_user)):
    editor = await users.get_by_id(id=id)
    if editor is None or editor.email != current_user.email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not found user")
    return await users.update(id=id, u=user)
