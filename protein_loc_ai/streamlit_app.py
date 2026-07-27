import requests
import streamlit as st
import os

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000"
)

# 페이지 기본 설정을 지정합니다.
st.set_page_config(
    page_title="ProteinLocAI",
    page_icon="🧬",
    layout="centered"
)

# 화면 제목을 표시합니다.
st.title("ProteinLocAI")
st.subheader("아미노산 서열 기반 단백질 세포 내 위치 예측")

# 사용자에게 입력받을 단백질 서열입니다.
sequence = st.text_area(
    "단백질 아미노산 서열을 입력하세요.",
    height=150,
    placeholder="예: MENEKENLFCEPHKRGLMKT..."
)

# 예측 버튼을 생성합니다.
predict_button = st.button(
    "세포 내 위치 예측"
)

# 버튼을 눌렀을 때 실행됩니다.
if predict_button:

    # 입력값이 비어 있는지 확인합니다.
    if not sequence.strip():
        st.warning("아미노산 서열을 입력하세요.")

    else:
        # FastAPI 서버로 보낼 데이터를 생성합니다.
        request_data = {
            "sequence": sequence
        }

        try:
        # FastAPI 서버에 예측 요청을 보냅니다.
            response = requests.post(
                f"{API_BASE_URL}/predict",
                json=request_data,
                timeout=30
            )

            # 잘못된 입력에 대한 오류 메시지를 표시합니다.
            if response.status_code == 400:
                error_detail = response.json().get(
                    "detail",
                    "입력값을 확인하세요."
                )

                st.error(error_detail)

            else:
                # 400 이외의 서버 오류를 확인합니다.
                response.raise_for_status()

                # 정상 응답을 JSON으로 변환합니다.
                result = response.json()

                st.success(
                    f"예측 위치: {result['predicted_location']}"
                )

                st.info(
                    f"신뢰도 상태: "
                    f"{result['confidence_status']}"
                )

                st.metric(
                    "최대 예측 확률",
                    f"{result['max_probability']:.2%}"
                )

                st.metric(
                    "1위와 2위 확률 차이",
                    f"{result['probability_gap']:.2%}"
                )

                st.subheader("클래스별 예측 확률")

                probability_data = result["probabilities"]

                st.bar_chart(probability_data)

                st.write(probability_data)

        except requests.exceptions.ConnectionError:
            st.error(
                "FastAPI 서버에 연결할 수 없습니다."
            )

        except requests.exceptions.RequestException as error:
            st.error(
                f"API 요청 중 오류가 발생했습니다: {error}"
            )