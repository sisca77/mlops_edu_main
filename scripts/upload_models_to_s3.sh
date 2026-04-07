#!/bin/bash
# ============================================
# 모델 및 데이터 파일을 S3에 업로드하는 스크립트
# ============================================
# 사용법: bash scripts/upload_models_to_s3.sh
# 사전조건: AWS CLI가 설치되어 있고 aws configure 완료
# ============================================

S3_BUCKET="mlops-loan-models"

echo "============================================"
echo "1. S3 버킷 생성 (이미 있으면 무시됨)"
echo "============================================"
aws s3 mb s3://$S3_BUCKET --region ap-northeast-2 2>/dev/null || true

echo ""
echo "============================================"
echo "2. 모델 파일 업로드"
echo "============================================"
aws s3 cp models/loan_pipeline.pkl s3://$S3_BUCKET/models/loan_pipeline.pkl
aws s3 cp models/label_encoders.pkl s3://$S3_BUCKET/models/label_encoders.pkl
aws s3 cp models/feature_names.pkl s3://$S3_BUCKET/models/feature_names.pkl

echo ""
echo "============================================"
echo "3. 데이터 파일 업로드"
echo "============================================"
aws s3 cp data/loan_data.csv s3://$S3_BUCKET/data/loan_data.csv
aws s3 cp data/prediction_logs.csv s3://$S3_BUCKET/data/prediction_logs.csv
aws s3 cp data/sample_reviews.csv s3://$S3_BUCKET/data/sample_reviews.csv

echo ""
echo "============================================"
echo "4. 업로드 확인"
echo "============================================"
aws s3 ls s3://$S3_BUCKET/ --recursive

echo ""
echo "완료!"
