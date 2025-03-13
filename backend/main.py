from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.convert import router as convert_router  # 파일 변환 API 라우터
from api.progress import router as progress_router  # 파일 변환 API 라우터
from api.test import router as test_router  # 파일 변환 API 라우터

app = FastAPI()

# ✅ CORS 설정 추가 (localhost:5173을 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vue 개발 서버 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

# API 라우터 등록
app.include_router(test_router)
app.include_router(convert_router)
app.include_router(progress_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
