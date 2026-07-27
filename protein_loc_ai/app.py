from pathlib import Path

import joblib
import pandas as pd

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="ProteinLocAI API",
    description="아미노산 서열 기반 단백질 세포 내 위치 예측 API",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {
        "message": "ProteinLocAI API is running"
    }

valid_amino_acids = sorted(
    list("ACDEFGHIKLMNPQRSTVWY")
)

amino_acid_groups = {
    "hydrophobic": set("AVILMFWY"),
    "polar": set("STNQC"),
    "positive": set("KRH"),
    "negative": set("DE"),
    "aromatic": set("FWY")
}

all_2mers = [
    aa1 + aa2
    for aa1 in valid_amino_acids
    for aa2 in valid_amino_acids
]

def calculate_aa_composition(sequence):
    sequence_length = len(sequence)

    composition = {}

    for aa in valid_amino_acids:
        composition[f"aa_{aa}"] = (
            sequence.count(aa) / sequence_length
        )

    return composition

def calculate_biochemical_features(sequence):
    sequence_length = len(sequence)

    features = {}

    for group_name, amino_acids in amino_acid_groups.items():
        group_count = sum(
            sequence.count(aa)
            for aa in amino_acids
        )

        features[f"{group_name}_ratio"] = (
            group_count / sequence_length
        )

    return features

def calculate_n_terminal_features(
    sequence,
    n_terminal_length=30
):
    # 단백질 서열의 앞부분 30개를 추출합니다.
    n_terminal_sequence = sequence[
        :n_terminal_length
    ]

    # 실제 N-terminal 길이를 확인합니다.
    actual_length = len(
        n_terminal_sequence
    )

    if actual_length == 0:
        raise ValueError(
            "N-terminal 서열이 비어 있습니다."
        )

    # N-terminal 아미노산 조성을 계산합니다.
    aa_features = calculate_aa_composition(
        n_terminal_sequence
    )

    # 기존 Feature와 구분하기 위해 접두사를 추가합니다.
    aa_features = {
        f"nterm_{key}": value
        for key, value in aa_features.items()
    }

    # N-terminal 생화학적 특성을 계산합니다.
    biochemical_features = (
        calculate_biochemical_features(
            n_terminal_sequence
        )
    )

    # 생화학적 Feature에도 접두사를 추가합니다.
    biochemical_features = {
        f"nterm_{key}": value
        for key, value in biochemical_features.items()
    }

    # N-terminal 길이 Feature를 추가합니다.
    length_feature = {
        "nterm_length": actual_length
    }

    return {
        **aa_features,
        **biochemical_features,
        **length_feature
    }


def calculate_2mer_frequency(sequence):
    counts = {
        mer: 0
        for mer in all_2mers
    }

    total_2mers = len(sequence) - 1

    for i in range(total_2mers):
        mer = sequence[i:i + 2]
        counts[mer] += 1

    for mer in counts:
        counts[mer] = counts[mer] / total_2mers

    return counts

def create_sequence_features(sequence):
    sequence = sequence.upper().replace(" ", "")

    # 공백 제거 후 서열이 비어 있는지 확인합니다.
    if not sequence:
        raise ValueError(
            "아미노산 서열을 입력해야 합니다."
        )

    # 2-mer 계산을 위해 최소 2개 이상의 아미노산이 필요합니다.
    if len(sequence) < 2:
        raise ValueError(
            "아미노산 서열은 최소 2개 이상이어야 합니다."
        )
    
    valid_amino_acids_set = set(
        "ACDEFGHIKLMNPQRSTVWY"
    )

    invalid_amino_acids = (
        set(sequence) - valid_amino_acids_set
    )

    if invalid_amino_acids:
        raise ValueError(
            f"허용되지 않는 아미노산: {invalid_amino_acids}"
        )

    aa_features = calculate_aa_composition(sequence)
    biochemical_features = (
        calculate_biochemical_features(sequence)
    )
    two_mer_features = (
    calculate_2mer_frequency(sequence)
    )

    # N-terminal Feature를 계산합니다.
    n_terminal_features = (
        calculate_n_terminal_features(
            sequence,
            n_terminal_length=30
        )
    )

    length_features = {
        "sequence_length": len(sequence)
    }

    all_features = {
    **aa_features,
    **biochemical_features,
    **length_features,
    **two_mer_features,
    **n_terminal_features
    }

    return pd.DataFrame([all_features])

# 저장된 최종 모델을 불러옵니다.
model_path = (
    Path("models")
    / "protein_location_n_terminal.joblib"
)

model_artifact = joblib.load(model_path)

@app.get("/health")
def health_check():
    # 현재 모델의 Feature 개수를 확인합니다.
    feature_count = len(
        model_artifact["feature_columns"]
    )

    # 모델이 사용하는 클래스를 확인합니다.
    labels = list(
        model_artifact["labels"]
    )

    # 모델 버전을 가져옵니다.
    model_version = model_artifact.get(
        "model_version",
        "unknown"
    )

    return {
        "status": "healthy",
        "model_loaded": True,
        "model_version": model_version,
        "feature_count": feature_count,
        "labels": labels
    }

def predict_protein_location(sequence, model_artifact):
    # 저장된 모델과 Feature 순서를 가져옵니다.
    model = model_artifact["model"]
    feature_columns = model_artifact["feature_columns"]

    # 입력 서열을 모델 입력 Feature로 변환합니다.
    features = create_sequence_features(sequence)

    # 학습 당시 Feature 순서와 동일하게 정렬합니다.
    features = features.reindex(
        columns=feature_columns,
        fill_value=0
    )

    # 클래스와 예측 확률을 계산합니다.
    probabilities = model.predict_proba(features)[0]
    classes = model.classes_

    # 가장 높은 확률의 클래스를 선택합니다.
    best_index = probabilities.argmax()
    predicted_location = classes[best_index]
    max_probability = probabilities[best_index]

    # 1위와 2위 확률의 차이를 계산합니다.
    sorted_probabilities = sorted(
        probabilities,
        reverse=True
    )

    probability_gap = (
        sorted_probabilities[0]
        - sorted_probabilities[1]
    )

    # 신뢰도 상태를 결정합니다.
    if (
        max_probability >= 0.70
        and probability_gap >= 0.15
    ):
        confidence_status = "신뢰도 높음"
    elif max_probability >= 0.50:
        confidence_status = "주의해서 해석"
    else:
        confidence_status = "추가 검토 필요"

    return {
        "predicted_location": predicted_location,
        "probabilities": {
            label: float(probability)
            for label, probability in zip(
                classes,
                probabilities
            )
        },
        "max_probability": float(max_probability),
        "probability_gap": float(probability_gap),
        "confidence_status": confidence_status
    }

class ProteinSequenceRequest(BaseModel):
    sequence: str = Field(
        ...,
        min_length=2,
        description="단백질 아미노산 서열"
    )


@app.post("/predict")
def predict_location(
    request: ProteinSequenceRequest
):
    # 사용자가 보낸 서열을 가져옵니다.
    sequence = request.sequence

    try:
        # 모델로 세포 내 위치를 예측합니다.
        result = predict_protein_location(
            sequence,
            model_artifact
        )

        return result

    except ValueError as error:
        # 잘못된 아미노산 입력은 사용자 입력 오류로 처리합니다.
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


