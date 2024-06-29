from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from event_manager.core.database import with_session
from event_manager.dal.user import user_manager
from event_manager.schemas.user import User, UserCreate, UserUpdate

router = APIRouter()


@router.post("/", response_model=User)
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(with_session)):
    try:
        return await user_manager.create(db, user_in)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{user_id}", response_model=User)
async def read_user(user_id: int, db: AsyncSession = Depends(with_session)):
    try:
        user = await user_manager.get(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{user_id}", response_model=User)
async def update_user(
    user_id: int, user_in: UserUpdate, db: AsyncSession = Depends(with_session)
):
    try:
        db_user = await user_manager.get(db, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        return await user_manager.update(db, db_user, user_in)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{user_id}", response_model=User)
async def delete_user(user_id: int, db: AsyncSession = Depends(with_session)):
    try:
        user = await user_manager.remove(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=list[User])
async def get_all_users(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(with_session)
):
    try:
        return await user_manager.get_all(db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
