from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

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

# # 簡単なユーザーデータベース（実際の実装ではセキュアな方法で保存する必要があります）
# users = {
#     'bani': 'password123',
#     'lego': 'password456'
# }

# # リクエストボディのバリデーション用モデル
# class LoginRequest(BaseModel):
#     username: str
#     password: str

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

if __name__ == "__main__":
    # アプリケーションを指定されたURLで実行
    uvicorn.run(app, host="127.0.0.1", port=8000)
