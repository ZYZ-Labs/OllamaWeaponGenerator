# backend/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import StreamingResponse  # 导入 StreamingResponse
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Optional
import os

from fastapi.middleware.cors import CORSMiddleware

from database import engine, SessionLocal, Base
import models
import schemas
import crud
import auth
import ollama_client
import logging
import json

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 自动创建表（仅在首次运行时执行，正式环境可使用数据库迁移工具）
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 前端运行的地址，可根据实际情况修改
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据库依赖项
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 注册接口
@app.post("/register", response_model=schemas.Token)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    user_created = crud.create_user(db, user)
    access_token = auth.create_access_token(
        data={"sub": user_created.username},
        expires_delta=timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

# 登录接口
@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    access_token = auth.create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

# 武器生成接口
@app.post("/generate_weapon")
def generate_weapon_endpoint(request: schemas.WeaponGenerateRequest):
    # 直接通过属性访问
    world_description = request.world_description+"请生成一件游戏武器，严格返回 JSON 格式文本，不要附带其他文字。输出内容必须以 { 开始，以 } 结束"
    model = request.model or "deepseek-r1:8b"
    if not world_description:
        raise HTTPException(status_code=400, detail="缺少 world_description 参数")
    try:
        weapon_data = ollama_client.generate_weapon(model, world_description)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"weapon": weapon_data}

@app.post("/generate_weapon_stream")
def generate_weapon_stream_endpoint(request: schemas.WeaponGenerateRequest):
    # 拼接提示，确保严格要求返回 JSON 格式
    prompt = f"{request.world_description}\n请生成一件游戏武器，严格返回 JSON 格式文本，不要附带其他文字。输出内容必须以 {{ 开始，以 }} 结束。"
    model = request.model or "deepseek-r1:8b"
    if not request.world_description:
        raise HTTPException(status_code=400, detail="缺少 world_description 参数")
    
    logger.debug("开始流式生成武器: model=%s, prompt=%s", model, prompt)
    
    def event_generator():
        accumulated = ""  # 用于累积返回的 response 内容
        try:
            for chunk in ollama_client.generate_weapon_stream(model, prompt):
                text = chunk.strip()
                try:
                    # 尝试解析每个流式返回的 chunk
                    j = json.loads(text)
                except Exception as e:
                    logger.error("解析 JSON chunk 失败: %s, 原始数据: %s", e, chunk)
                    # 如果解析失败，直接跳过当前 chunk
                    continue

                # 如果有 response 字段，将其累加
                if "response" in j:
                    accumulated += j["response"]
                    # 返回累积的内容（如果你希望实时更新前端，每个 chunk 都发送一次）
                    yield f"data: {accumulated}\n\n"
                # 如果 done 为 True，则结束流式返回
                if j.get("done", False):
                    break
        except Exception as e:
            logger.error("流式生成武器异常: %s", e)
            yield f"data: 生成武器错误: {str(e)}\n\n"
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")


# 武器保存接口
@app.post("/save_weapon", response_model=schemas.Weapon)
def save_weapon(weapon_data: dict, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    logger.debug("收到的weapon_data: %s", weapon_data)
    # 将中文键转换为英文键
    data = {
        "type": weapon_data.get("类型"),
        "name": weapon_data.get("名称"),
        "attributes": weapon_data.get("属性"),
        "effects": weapon_data.get("特效"),
        "skills": weapon_data.get("特技"),
        "background": weapon_data.get("背景")
    }
    logger.debug("转换后的data: %s", data)
    try:
        weapon_in = schemas.WeaponCreate(**data)
    except Exception as e:
        logger.error("数据转换错误: %s", e)
        raise HTTPException(status_code=422, detail=f"数据转换错误: {e}")
    saved_weapon = crud.create_weapon(db, weapon_in.dict(), current_user.id)
    logger.debug("保存的武器: %s", saved_weapon)
    return saved_weapon

@app.get("/models")
def get_models():
    return ollama_client.get_models()
