"""CORS 설정"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def register_cors(app: FastAPI) -> None:
	"""CORS 미들웨어 등록"""
	app.add_middleware(
		CORSMiddleware,
		allow_origins=["*"],  # 모든 origin 허용
		allow_credentials=True,
		allow_methods=["*"],  # 모든 HTTP 메서드 허용
		allow_headers=["*"],  # 모든 헤더 허용
	)
