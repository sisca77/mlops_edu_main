from contextlib import asynccontextmanager
from fastapi import HTTPException
import logging

from app.model import LoanModel
from app.schemas import LoanRequest, LoanResponse, AskRequest, AskResponse
from app.gemini_client import ask_gemini, analyze_question
from fastapi import FastAPI, HTTPException


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('대출 심사 모델을 로드합니다.')
    model = LoanModel()
    try:
        model.load()
        logger.info('모델 로드 성공')
    except Exception as e:
        logger.error(f'모델 로드 실패: {e}')
        logger.warning('/predict 엔드포인트는 모델 로드 후 사용가능')
    app.state.model = model

    yield

    logger.info('대출 심사 API를 종료합니다.')
    


app = FastAPI(
    title = '대출 심사 예측 API',
    description = 'ML 모델 기반 대출 승인 여부를 예측하는 API',
    version = '1.0.0',
    lifespan = lifespan
)

@app.get('/')
async def root():
    return {"message": "대출 심사 예측 API에 오신 것을 환영합니다. \
            /predict 엔드포인트를 사용하여 대출 승인 여부를 예측하세요."}
    
@app.get('/health')
async def health_check():
    model = app.state.model 
    model_loaded = model.pipeline is not None
    return {
        "status" : "healthy" if model_loaded else "degraded",
        "model_loaded" : model_loaded
    }

@app.post("/predict", response_model = LoanResponse)
async def predict(request: LoanRequest):
    model = app.state.model

    try:

        result = model.predict(request.model_dump())
        return LoanResponse(**result)
    
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail="입력값처리오류")
    except Exception as e:
        raise HTTPException(status_code=500)


@app.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest):
    try:
        result = analyze_question(request.question)
        return AskResponse(question=request.question, **result)
    except Exception as e:
        logger.error(f"AI API 오류: {e}")
        raise HTTPException(status_code=500, detail="AI API 호출 중 오류가 발생했습니다.")