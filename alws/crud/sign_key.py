import typing

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, update
from sqlalchemy.orm import selectinload
import datetime

from alws import models
from alws.crud.user import get_user
from alws.errors import (
    DataNotFoundError,
    PlatformMissingError,
    SignKeyAlreadyExistsError,
)
from alws.models import User
from alws.perms import actions
from alws.perms.authorization import can_perform
from alws.schemas import sign_schema


async def get_sign_keys(
    db: AsyncSession,
    user: User,
) -> typing.List[models.SignKey]:
    limited_user = await get_user(db, user.id)
    result = await db.execute(
        select(models.SignKey).where(models.SignKey.active).options(
            selectinload(models.SignKey.owner),
            selectinload(models.SignKey.roles).selectinload(
                models.UserRole.actions
            ),
        )
    )
    suitable_keys = [
        sign_key
        for sign_key in result.scalars().all()
        if can_perform(sign_key, limited_user, actions.UseSignKey.name)
    ]
    return suitable_keys


async def create_sign_key(
    db: AsyncSession, payload: sign_schema.SignKeyCreate
) -> models.SignKey:
    check = await db.execute(
        select(models.SignKey.id).where(models.SignKey.keyid == payload.keyid)
    )
    if check.scalars().first():
        raise SignKeyAlreadyExistsError(
            f"Key with keyid {payload.keyid} already exists"
        )
    if payload.platform_id:
        check_platform = await db.execute(
            select(models.Platform.id).where(
                models.Platform.id == payload.platform_id
            )
        )
        if not check_platform.scalars().first():
            raise PlatformMissingError(
                f"No platform with id '{payload.platform_id}' "
                "exists in the system"
            )
    sign_key = models.SignKey(**payload.model_dump())
    db.add(sign_key)
    await db.flush()
    await db.refresh(sign_key)
    return sign_key


async def update_sign_key(
    db: AsyncSession, key_id: int, payload: sign_schema.SignKeyUpdate
) -> models.SignKey:
    sign_key = await db.execute(select(models.SignKey).get(key_id))
    if not sign_key:
        raise DataNotFoundError(f"Sign key with ID {key_id} does not exist")
    for k, v in payload.model_dump().items():
        setattr(sign_key, k, v)
    db.add(sign_key)
    await db.flush()
    await db.refresh(sign_key)
    return sign_key
