# backend/crud.py
from sqlalchemy.orm import Session
from models import User, Weapon
from schemas import UserCreate
import auth

def create_user(db: Session, user: UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = User(username=user.username, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_weapon(db: Session, weapon_data: dict, user_id: int):
    # 这里假设 weapon_data 的键与生成 JSON 中的中文字段一致
    db_weapon = Weapon(
        user_id=user_id,
        type=weapon_data.get("类型"),
        name=weapon_data.get("名称"),
        attributes=weapon_data.get("属性"),
        effects=weapon_data.get("特效"),
        skills=weapon_data.get("特技"),
        background=weapon_data.get("背景")
    )
    db.add(db_weapon)
    db.commit()
    db.refresh(db_weapon)
    return db_weapon
