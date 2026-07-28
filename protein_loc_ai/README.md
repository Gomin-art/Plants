# ProteinLocAI

아미노산 서열 기반 단백질 세포 내 위치 예측 AI 서비스

## 프로젝트 소개

단백질 아미노산 서열을 입력하면 다음 세포 내 위치를 예측합니다.

- cytoplasm
- mitochondrion
- nucleus

## 주요 기술

- Python
- scikit-learn
- SVM
- FastAPI
- Streamlit
- Docker Compose

## Feature Engineering

총 452개 Feature를 사용했습니다.

- 아미노산 조성: 20개
- 생화학적 특성: 5개
- 서열 길이: 1개
- 2-mer 빈도: 400개
- N-terminal Feature: 26개

## 성능

- Holdout Accuracy: 약 0.736
- Holdout Balanced Accuracy: 약 0.737
- Holdout Macro F1-score: 약 0.73
- 5-Fold Mean Macro F1-score: 약 0.712
- 5-Fold Mean Balanced Accuracy: 약 0.719

## 실행 방법

```powershell
docker compose up --build