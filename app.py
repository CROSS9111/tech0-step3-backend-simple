from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv

from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.orm import sessionmaker

import os
from supabase import create_client, Client

load_dotenv(override=True)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the environment variables.")

# SQLAlchemy エンジン＆セッション準備
# "/user"と"/login_user"にて使用する
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# FastAPIアプリケーションのインスタンスを作成
app = FastAPI()

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # すべてのオリジンを許可
    allow_credentials=True,
    allow_methods=["*"],  # すべてのメソッドを許可
    allow_headers=["*"],  # すべてのヘッダーを許可
)

# ルートURLにアクセスがあった場合に実行される関数
@app.get("/")
async def hello_world():
    return 'Hello, World!'

# /nightにアクセスがあった場合に実行される関数
@app.get("/night")
async def hello_night_world():
    return 'Good night!'

# # /night/{id}にアクセスがあった場合に実行される関数
# @app.get("/night/{id}")
# async def good_night(id: str):
#     # GETメソッドで/night/idにアクセスしてきたら、idさん、「早く寝てね」と返答します
#     return f'{id}さん、「早く寝てね」'

# 簡単なユーザーデータベース（実際の実装ではセキュアな方法で保存する必要があります）
users = {
    'bani': 'password123',
    'lego': 'password456'
}

# リクエストボディのバリデーション用モデル
class LoginRequest(BaseModel):
    username: str
    password: str

# # '/login'エンドポイントを定義
# @app.post("/login")
# async def login(login_data: LoginRequest):
#     username = login_data.username
#     password = login_data.password
    
#     # ユーザー名がusersディクショナリに存在し、かつパスワードが一致するか確認します
#     if username in users and users[username] == password:
#         # 認証成功の場合、歓迎メッセージを含むJSONレスポンスを返します
#         return {"message": f'ようこそ！{username}さん'}
#     else:
#         # 認証失敗の場合、エラーメッセージを含むJSONレスポンスと
#         # HTTP status code 401（Unauthorized）を返します
#         raise HTTPException(
#             status_code=401,
#             detail="認証失敗"
#         )
    

# メタデータに反映させて、テーブルオブジェクトを取得
metadata = MetaData()
users_table = Table("users", metadata, autoload_with=engine)

# /users に GET でアクセスされたときに
# Supabaseのsers テーブルの全レコードを返すエンドポイント
@app.get("/users")
def read_users():
    """
    /users に GET でアクセスされたときに
    users テーブルの全レコードを返すエンドポイント
    """
    try:
        with SessionLocal() as session:
            stmt = select(users_table)
            result = session.execute(stmt).all()
            # row._mapping で {カラム名: 値} の dict が取れる
            users = [dict(row._mapping) for row in result]
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB読み込みエラー: {e}")
    
@app.post("/users_login")
async def users_login(login_data: LoginRequest):
    username = login_data.username
    password = login_data.password
    
    try:
        with SessionLocal() as session:
            # usersテーブルから指定されたユーザー名のレコードを検索
            stmt = select(users_table).where(users_table.c.username == username)
            result = session.execute(stmt).first()
            
            if result:
                # ユーザーが見つかった場合、パスワードを検証
                user_data = dict(result._mapping)
                if user_data["password"] == password:  # 実際の実装ではハッシュ化したパスワードを比較するべき
                    # 認証成功の場合、成功メッセージとユーザー情報を返す
                    return {
                        "success": True, 
                        "message": f"ようこそ！{username}さん", 
                        "user": {
                            "id": user_data["id"],
                            "username": user_data["username"]
                            # パスワードなど機密情報は含めない
                        }
                    }
            
            # ユーザーが見つからないか、パスワードが一致しない場合
            raise HTTPException(
                status_code=401,
                detail="認証失敗: ユーザー名またはパスワードが正しくありません"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"認証処理中にエラーが発生しました: {str(e)}")
    
if __name__ == "__main__":
    # アプリケーションを指定されたURLで実行
    uvicorn.run(app, host="127.0.0.1", port=8000)