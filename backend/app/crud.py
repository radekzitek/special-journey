from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import List, Optional

from app.models import User
from app.core.security import get_password_hash, verify_password
from . import models, schemas


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()


async def create_user(db: AsyncSession, email: str, password: str):
    hashed_password = get_password_hash(password)
    user = User(email=email, hashed_password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def authenticate_user(db: AsyncSession, email: str, password: str):
    user = await get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


async def update_password(db: AsyncSession, email: str, new_password: str):
    user = await get_user_by_email(db, email)
    if user:
        user.hashed_password = get_password_hash(new_password)
        await db.commit()
        return user
    return None


# User CRUD operations
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        role=user.role,
        is_active=user.is_active
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        return None
    
    update_data = user.dict(exclude_unset=True)
    
    if "password" in update_data and update_data["password"]:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user


# TeamMember CRUD operations
def get_team_member(db: Session, team_member_id: int):
    return db.query(models.TeamMember).filter(models.TeamMember.id == team_member_id).first()


def get_team_member_by_email(db: Session, email: str):
    return db.query(models.TeamMember).filter(models.TeamMember.email == email).first()


def get_team_member_by_user_id(db: Session, user_id: int):
    return db.query(models.TeamMember).filter(models.TeamMember.user_id == user_id).first()


def get_team_members(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    superior_id: Optional[int] = None,
    include_inactive: bool = False
):
    query = db.query(models.TeamMember)
    
    if superior_id is not None:
        query = query.filter(models.TeamMember.superior_id == superior_id)
    
    if not include_inactive:
        query = query.filter(models.TeamMember.is_active == True)
    
    return query.offset(skip).limit(limit).all()


def get_team_members_with_hierarchy(
    db: Session, 
    superior_id: Optional[int] = None, 
    include_inactive: bool = False
):
    query = db.query(models.TeamMember)
    
    if superior_id is not None:
        query = query.filter(models.TeamMember.superior_id == superior_id)
    else:
        query = query.filter(models.TeamMember.superior_id == None)
    
    if not include_inactive:
        query = query.filter(models.TeamMember.is_active == True)
    
    # Load with direct reports up to a reasonable depth
    return query.options(joinedload(models.TeamMember.direct_reports)).all()


def create_team_member(db: Session, team_member: schemas.TeamMemberCreate):
    db_team_member = models.TeamMember(**team_member.dict())
    
    # Check if email is already used
    if get_team_member_by_email(db, team_member.email):
        return None
    
    db.add(db_team_member)
    db.commit()
    db.refresh(db_team_member)
    return db_team_member


def update_team_member(db: Session, team_member_id: int, team_member: schemas.TeamMemberUpdate):
    db_team_member = db.query(models.TeamMember).filter(models.TeamMember.id == team_member_id).first()
    if db_team_member is None:
        return None
    
    update_data = team_member.dict(exclude_unset=True)
    
    # Check if email is being updated and if it's already in use
    if "email" in update_data and update_data["email"] != db_team_member.email:
        existing = get_team_member_by_email(db, update_data["email"])
        if existing and existing.id != team_member_id:
            return None
    
    for field, value in update_data.items():
        setattr(db_team_member, field, value)
    
    db.commit()
    db.refresh(db_team_member)
    return db_team_member


def delete_team_member(db: Session, team_member_id: int):
    db_team_member = db.query(models.TeamMember).filter(models.TeamMember.id == team_member_id).first()
    if db_team_member:
        db.delete(db_team_member)
        db.commit()
        return True
    return False
