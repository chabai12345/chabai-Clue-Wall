import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI(title="游戏档案")

DATA_DIR = Path(os.environ.get(
    'DETECTIVE_BOARD_DATA',
    Path(__file__).parent / "data"
))
DATA_DIR.mkdir(exist_ok=True)
STATIC_DIR = Path(os.environ.get(
    'DETECTIVE_BOARD_STATIC',
    Path(getattr(sys, '_MEIPASS', Path(__file__).parent)) / "static"
))

# ---- 数据模型 ----

class CardModel(BaseModel):
    id: str
    type: str          # character / clue / location / evidence
    title: str
    content: list = []
    x: float
    y: float
    w: float = 180     # 卡片宽度
    h: float = 180     # 卡片高度
    image: str = ""    # base64 图片数据

class ConnectionModel(BaseModel):
    id: str
    from_id: str
    to_id: str
    color: str
    label: str
    font_size: int = 14
    control_x: float | None = None
    control_y: float | None = None
    arrow_type: str = "single"

class BoardData(BaseModel):
    name: str
    cards: List[CardModel] = []
    connections: List[ConnectionModel] = []

# ---- 辅助 ----

def safe_name(name: str) -> str:
    """将存档名转为安全的文件名"""
    safe = re.sub(r'[\\/:*?"<>|]', '_', name)
    return safe.strip() or "未命名"

# ---- API ----

@app.get("/api/boards")
def list_boards():
    files = sorted(DATA_DIR.glob("*.json"), key=lambda f: f.stat().st_mtime, reverse=True)
    boards = []
    for f in files:
        try:
            with open(f, encoding="utf-8") as fp:
                data = json.load(fp)
            boards.append({
                "name": f.stem,
                "card_count": len(data.get("cards", [])),
                "updated": datetime.fromtimestamp(f.stat().st_mtime).strftime("%m-%d %H:%M")
            })
        except Exception:
            pass
    return boards


@app.post("/api/boards/{name}")
def save_board(name: str, data: BoardData):
    filename = safe_name(name) + ".json"
    filepath = DATA_DIR / filename
    with open(filepath, "w", encoding="utf-8") as fp:
        json.dump(data.model_dump(), fp, ensure_ascii=False, indent=2)
    return {"ok": True, "name": data.name}


@app.get("/api/boards/{name}")
def load_board(name: str):
    filename = safe_name(name) + ".json"
    filepath = DATA_DIR / filename
    if not filepath.exists():
        raise HTTPException(404, f"存档 '{name}' 不存在")
    with open(filepath, encoding="utf-8") as fp:
        return json.load(fp)


@app.delete("/api/boards/{name}")
def delete_board(name: str):
    filename = safe_name(name) + ".json"
    filepath = DATA_DIR / filename
    if filepath.exists():
        filepath.unlink()
    return {"ok": True}


# ---- 静态文件 ----

app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
