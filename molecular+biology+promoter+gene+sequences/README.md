# DNA Promoter Sequence Classification

DNA 염기서열을 활용해 promoter와 non-promoter를 분류하는 머신러닝 프로젝트입니다.

## 프로젝트 목적

유전자 발현 조절과 관련된 promoter 서열의 패턴을 머신러닝으로 학습하고, 새로운 DNA 서열이 promoter인지 분류합니다.

## Dataset

- Dataset: Molecular Biology Promoter Gene Sequences
- 전체 데이터: 106개
- Promoter: 53개
- Non-promoter: 53개
- 서열 길이: 57 bp
- 클래스: `+`, `-`

## Feature Engineering

## One-hot Encoding

각 염기 위치의 A, T, G, C를 0과 1로 변환했습니다.

```text
57개 위치 × 4개 염기 = 228개 Feature
```
## 3-mer Feature
연속된 3개 염기 조합의 빈도를 계산했습니다.

```text
4^3 = 64개 Feature
```

## Combined Feature
One-hot Feature와 3-mer Feature를 결합했습니다.

```text
228 + 64 = 292개 Feature
```

## 사용 모델
- Logistic Regression
- SVM
- Random Forest
- Extra Trees
## 모델 성능
5-Fold Cross Validation 결과입니다.

- One-hot Extra Trees: 약 0.943
- 3-mer Random Forest: 약 0.934
- Combined Random Forest: 약 0.972
- Combined Extra Trees: 약 0.962
Combined Feature를 사용한 Random Forest가 가장 높은 평균 Accuracy를 기록했습니다.

## 주요 분석
- Promoter와 non-promoter의 GC content 비교
- 위치별 염기 빈도 분석
- One-hot Feature Importance 분석
- 위치별 Feature Importance 분석
- 3-mer 패턴 분석
- Feature Set별 모델 성능 비교

## 주요 인사이트
One-hot Feature는 염기의 위치 정보를 표현하고, 3-mer Feature는 인접한 염기 조합 패턴을 표현합니다.

두 Feature를 결합했을 때 성능이 향상되어, 위치 정보와 국소 서열 패턴을 함께 사용하는 것이 효과적임을 확인했습니다.


## 한계점
- 데이터가 106개로 적습니다.
- 특정 데이터셋에 의존할 가능성이 있습니다.
- 외부 검증 데이터가 부족합니다.
- 새로운 생물 종의 서열에 대한 추가 검증이 필요합니다.

## 사용 기술
- Python
- pandas
- NumPy
- scikit-learn
- Matplotlib
- Seaborn
