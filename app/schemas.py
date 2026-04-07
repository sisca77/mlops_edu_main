from pydantic import BaseModel, Field

class LoanRequest(BaseModel):
    """대출 심사를 위한 고객 정보 입력 스키마."""

    age: int = Field(
        ...,
        ge=19,
        le=100,
        description="나이",
        examples=[35],
    )

    gender: str = Field(
        ...,
        description="성별",
        examples=["남"],
    )

    annual_income: float = Field(
        ...,
        ge=0,
        description="연소득",
        examples=[5000.0],
    )

    employment_years: int = Field(
        ...,
        ge=0,
        le=50,
        description="근속연수",
        examples=[5],
    )

    housing_type: str = Field(
        ...,
        description="주거형태",
        examples=["자가"],
    )

    credit_score: int = Field(
        ...,
        ge=300,
        le=900,
        description="신용점수",
        examples=[720],
    )

    existing_loan_count: int = Field(
        ...,
        ge=0,
        description="기존대출건수",
        examples=[2],
    )

    annual_card_usage: float = Field(
        ...,
        ge=0,
        description="연간카드사용액",
        examples=[2400.0],
    )

    debt_ratio: float = Field(
        ...,
        ge=0,
        le=100,
        description="부채비율",
        examples=[35.5],
    )

    loan_amount: float = Field(
        ...,
        ge=100,
        description="대출신청액",
        examples=[3000.0],
    )

    loan_purpose: str = Field(
        ...,
        description="대출목적",
        examples=["주택구입"],
    )

    repayment_method: str = Field(
        ...,
        description="상환방식",
        examples=["원리금균등"],
    )

    loan_period: int = Field(
        ...,
        ge=6,
        le=360,
        description="대출기간",
        examples=[36],
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "age": 35,
                    "gender": "남",
                    "annual_income": 5000.0,
                    "employment_years": 5,
                    "housing_type": "자가",
                    "credit_score": 720,
                    "existing_loan_count": 2,
                    "annual_card_usage": 2400.0,
                    "debt_ratio": 35.5,
                    "loan_amount": 3000.0,
                    "loan_purpose": "주택구입",
                    "repayment_method": "원리금균등",
                    "loan_period": 36,
                }
            ]
        }
    }


class LoanResponse(BaseModel):
    approved: bool = Field(
        ...,
        description="승인 여부 (True=승인, False:거절)",
    )
    probability: float = Field(
        ...,
        ge=0.0, 
        le=1.0,
        description="승인 확률 (0.0~1.0)",
    )
    risk_grade: str = Field(
        ...,
        description="리스크 등급 ('A', 'B', 'C', 'D')"
    )


class AskRequest(BaseModel):
    """AI 질문 요청 스키마."""
    question: str = Field(
        ...,
        min_length=1,
        description="질문 내용",
        examples=["대출 금리가 너무 높아서 걱정이에요"],
    )


class AskResponse(BaseModel):
    """AI 질문 응답 스키마 (답변 + 감성분석 + 카테고리 분류)."""
    question: str = Field(
        ...,
        description="원본 질문",
    )
    answer: str = Field(
        ...,
        description="AI 답변",
    )
    sentiment: str = Field(
        ...,
        description="감성 분석 결과 (긍정 | 부정 | 중립)",
    )
    sentiment_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="감성 점수 (0.0~1.0, 1.0이 가장 긍정)",
    )
    category: str = Field(
        ...,
        description="카테고리 (대출/금융, 부동산, 신용/채무, 일반상담, 기타)",
    )