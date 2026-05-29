import streamlit as st
import math

st.set_page_config(page_title="계산기", page_icon="🧮", layout="centered")

st.title("🧮 다기능 계산기")
st.markdown("사칙연산 · 모듈러 · 지수 · 로그 연산을 지원합니다.")

# 연산 선택
operation = st.selectbox(
    "연산 종류를 선택하세요",
    [
        "➕ 덧셈 (a + b)",
        "➖ 뺄셈 (a - b)",
        "✖️ 곱셈 (a × b)",
        "➗ 나눗셈 (a ÷ b)",
        "🔢 모듈러 연산 (a mod b)",
        "📈 지수 연산 (a ^ b)",
        "📉 로그 연산 (log_b(a))",
    ],
)

st.divider()

# 로그 연산은 입력 안내가 다름
if "로그" in operation:
    st.markdown("**log_b(a)** : a의 b진 로그를 계산합니다.")
    a = st.number_input("진수 (a)", value=100.0, format="%.6f")
    b = st.number_input("밑 (b, 0과 1 제외)", value=10.0, format="%.6f")
else:
    col1, col2 = st.columns(2)
    with col1:
        a = st.number_input("첫 번째 값 (a)", value=0.0, format="%.6f")
    with col2:
        b = st.number_input("두 번째 값 (b)", value=0.0, format="%.6f")

st.divider()

# 계산
if st.button("계산하기", use_container_width=True, type="primary"):
    result = None
    error = None

    try:
        if "덧셈" in operation:
            result = a + b
            formula = f"{a} + {b}"

        elif "뺄셈" in operation:
            result = a - b
            formula = f"{a} - {b}"

        elif "곱셈" in operation:
            result = a * b
            formula = f"{a} × {b}"

        elif "나눗셈" in operation:
            if b == 0:
                error = "⚠️ 0으로 나눌 수 없습니다."
            else:
                result = a / b
                formula = f"{a} ÷ {b}"

        elif "모듈러" in operation:
            if b == 0:
                error = "⚠️ 모듈러 연산의 제수는 0이 될 수 없습니다."
            else:
                result = a % b
                formula = f"{a} mod {b}"

        elif "지수" in operation:
            result = a ** b
            formula = f"{a} ^ {b}"

        elif "로그" in operation:
            if a <= 0:
                error = "⚠️ 진수(a)는 0보다 커야 합니다."
            elif b <= 0 or b == 1:
                error = "⚠️ 밑(b)은 0 초과이며 1이 아니어야 합니다."
            else:
                result = math.log(a, b)
                formula = f"log_{b}({a})"

    except OverflowError:
        error = "⚠️ 결과값이 너무 커서 계산할 수 없습니다."
    except Exception as e:
        error = f"⚠️ 오류 발생: {e}"

    if error:
        st.error(error)
    elif result is not None:
        st.success(f"**{formula} = {result:,.10g}**")
        st.metric(label="계산 결과", value=f"{result:,.10g}")

st.divider()
st.caption("Made with ❤️ using Streamlit · 중앙대학교병원 병동간호 1팀")
