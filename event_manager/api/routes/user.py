from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from event_manager.core.database import with_session
from event_manager.dal.company import company_manager
from event_manager.dal.user import user_manager
from event_manager.keycloak.crud import (
    create_keycloak_user,
    delete_keycloak_user,
    update_keycloak_user,
)
from event_manager.keycloak.permission_definitions import Roles
from event_manager.keycloak.permissions import CanManageUser
from event_manager.keycloak.security import IsAuthorized
from event_manager.schemas.company import CompanyCreate
from event_manager.schemas.user import User, UserCreate, UserUpdate

router = APIRouter()
# Route Permissions
can_manage_user = IsAuthorized(CanManageUser)


@router.post("/", response_model=User, dependencies=[Depends(can_manage_user)])
async def create_user(
    user_in: UserCreate,
    company_in: CompanyCreate,
    password: str,
    is_admin: Optional[bool] = False,
    db: AsyncSession = Depends(with_session),
):
    try:
        if is_admin:
            user_in.role = Roles.ADMIN
        # Create user in Keycloak
        keycloak_user_id = await create_keycloak_user(
            username=user_in.username,
            email=user_in.email,
            password=password,
            is_admin=is_admin,
        )

        company = await company_manager.create(db, company_in)
        # Store Keycloak user_id in the local database
        user_in.keycloak_id = keycloak_user_id
        user_in.company_id - company.id
        new_user = await user_manager.create(db, user_in)
        return new_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{user_id}", response_model=User, dependencies=[Depends(can_manage_user)])
async def read_user(user_id: int, db: AsyncSession = Depends(with_session)):
    try:
        user = await user_manager.get(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{user_id}", response_model=User, dependencies=[Depends(can_manage_user)])
async def update_user(
    user_id: int, user_in: UserUpdate, db: AsyncSession = Depends(with_session)
):
    try:
        db_user = await user_manager.get(db, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        update_keycloak_user(
            username=user_in.username,
            user_id=db_user.keycloak_id,
            email=user_in.email,
            password=user_in.password,
        )
        return await user_manager.update(db, db_user, user_in)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete(
    "/{user_id}", response_model=User, dependencies=[Depends(can_manage_user)]
)
async def delete_user(user_id: int, db: AsyncSession = Depends(with_session)):
    try:
        db_user = await user_manager.remove(db, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        delete_keycloak_user(db_user.keycloak_id)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=list[User], dependencies=[Depends(can_manage_user)])
async def get_all_users(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(with_session)
):
    try:
        return await user_manager.get_all(db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
