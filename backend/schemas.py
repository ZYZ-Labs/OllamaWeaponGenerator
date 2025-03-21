# backend/schemas.py
from pydantic import BaseModel
from typing import Optional, Any, Dict

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class WeaponBase(BaseModel):
    类型: Optional[str] = None
    名称: Optional[str] = None
    属性: Optional[Dict[str, Any]] = None
    特效: Optional[Dict[str, Any]] = None
    特技: Optional[Dict[str, Any]] = None
    背景: Optional[str] = None

    class Config:
        # 如果你使用 Pydantic V2，使用 from_attributes 而非 orm_mode
        from_attributes = True
        # 如果允许额外字段，也可以设置 extra 参数
        extra = "allow"

class WeaponCreate(WeaponBase):
    pass

class Weapon(WeaponBase):
    id: int
    user_id: int
    created_at: str

    class Config:
        from_attributes = True

class WeaponGenerateRequest(BaseModel):
    world_description: str
    model: str