# ProteinLocAI

아미노산 서열 기반 단백질 세포 내 위치 예측 AI 서비스

## 1. 프로젝트 소개

단백질의 아미노산 서열을 입력하면 단백질의 세포 내 위치를 예측하는 머신러닝 서비스입니다.

예측 대상은 다음 3가지입니다.

- cytoplasm
- mitochondrion
- nucleus

## 2. 시스템 구조

```text
사용자
  ↓
Streamlit 웹 화면
  ↓ HTTP POST
FastAPI 백엔드
  ↓
Feature Engineering
  ↓
SVM 모델
  ↓
예측 위치 및 확률 반환

```


## 3. 사용 기술

Python
pandas
NumPy
scikit-learn
FastAPI
Streamlit
Uvicorn
joblib

## 4. 데이터

UniProt에서 직접 다운로드한 단백질 서열 데이터를 사용했습니다.

사용한 클래스:
nucleus
cytoplasm
mitochondrion

전처리 과정:
중복 Entry 제거
비표준 아미노산 서열 제거
아미노산 조성 계산
생화학적 특성 계산
서열 길이 계산
2-mer 빈도 계산

## 5. Feature Engineering

총 426개 Feature를 사용했습니다.

아미노산 조성: 20개

생화학적 특성: 5개

서열 길이: 1개

2-mer 빈도: 400개

## 6. 모델

여러 모델을 비교한 결과 SVM을 최종 모델로 선택했습니다.

선정 기준:
Macro F1-score
Balanced Accuracy
클래스별 Recall
교차검증 안정성

## 7. 모델 성능

테스트 데이터 기준:

Accuracy: 약 0.715

Balanced Accuracy: 약 0.694

Macro F1-score: 약 0.69

모델은 예측 위치뿐 아니라 클래스별 예측 확률과 신뢰도 상태도 반환합니다.

## 8. 실행 방법

FastAPI 실행
python -m uvicorn app:app --reload

API 문서:
http://127.0.0.1:8000/docs

Health Check:
http://127.0.0.1:8000/health

Streamlit 실행
python -m streamlit run streamlit_app.py

웹 화면:
http://localhost:8501

## 9. 주요 API

POST /predict

입력:
{
  "sequence": "MENEKENLFCEPHKRGLMKTPLKESTTANIVLAEIQPDFGPLTTPTKPKE"
}

출력:
{
  "predicted_location": "cytoplasm",
  "max_probability": 0.4065,
  "probability_gap": 0.0289,
  "confidence_status": "추가 검토 필요"
}

## 10. 한계점

세포 내 위치가 여러 개인 단백질은 단일 라벨 데이터에서 제외했습니다.
아미노산 서열만 사용했기 때문에 구조 정보와 기능 정보가 제한적입니다.
mitochondrion 클래스의 예측 성능 개선이 필요합니다.
본 서비스는 연구 및 학습 목적이며 의료적 진단을 대체하지 않습니다.

## 11. 향후 개선 방향

단백질 3-mer Feature 추가
N-terminal 서열 Feature 추가
CNN 또는 Transformer 기반 모델 적용
단백질 구조 정보 결합
Docker 기반 배포
모델 모니터링 및 성능 기록

이제 프로젝트의 분석 과정, 모델, API, 실행 방법, 한계점이 하나의 문서에 정리됩니다.s