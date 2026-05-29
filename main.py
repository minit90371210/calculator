import streamlit as st
import math

st.set_page_config(page_title="계산기", page_icon="🧮", layout="centered")

# ── 세션 상태 초기화 ──────────────────────────────────────
if "expression" not in st.session_state:
    st.session_state.expression = ""
if "result" not in st.session_state:
    st.session_state.result = ""
if "history" not in st.session_state:
    st.session_state.history = []

def press(val):
    """버튼 클릭 시 수식에 값 추가"""
    st.session_state.expression += str(val)

def clear_all():
    st.session_state.expression = ""
    st.session_state.result = ""

def backspace():
    st.session_state.expression = st.session_state.expression[:-1]

def calculate():
    expr = st.session_state.expression
    if not expr:
        return
    try:
        # 수식 전처리: ^ → **, mod → %, log(a,b) 지원
        safe_expr = expr
        safe_expr = safe_expr.replace("^", "**")
        safe_expr = safe_expr.replace("mod", "%")
        safe_expr = safe_expr.replace("log(", "math.log(")
        safe_expr = safe_expr.replace("√(", "math.sqrt(")

        allowed = {
            "__builtins__": {},
            "math": math,
        }
        res = eval(safe_expr, allowed)
        res_str = f"{res:,.10g}"
        st.session_state.history.append(f"{expr} = {res_str}")
        st.session_state.result = res_str
    except ZeroDivisionError:
        st.session_state.result = "⚠️ 0으로 나눌 수 없습니다"
    except Exception:
        st.session_state.result = "⚠️ 수식 오류"

# ── UI ───────────────────────────────────────────────────
st.title("🧮 다기능 계산기")

# 디스플레이
st.text_input(
    "수식 입력창 (버튼 클릭 또는 직접 입력)",
    value=st.session_state.expression,
    key="display_input",
    placeholder="수식을 입력하거나 버튼을 누르세요",
)
# 직접 키보드 입력도 반영
if st.session_state.display_input != st.session_state.expression:
    st.session_state.expression = st.session_state.display_input

# 결과 표시
if st.session_state.result:
    color = "red" if "⚠️" in st.session_state.result else "#1a73e8"
    st.markdown(
        f"<h2 style='text-align:right; color:{color};'>= {st.session_state.result}</h2>",
        unsafe_allow_html=True,
    )

st.divider()

# ── 버튼 레이아웃 ─────────────────────────────────────────
# 행 1: 특수 기능
r0 = st.columns(4)
with r0[0]: st.button("AC", use_container_width=True, on_click=clear_all)
with r0[1]: st.button("⌫", use_container_width=True, on_click=backspace)
with r0[2]: st.button("mod", use_container_width=True, on_click=press, args=("mod",))
with r0[3]: st.button("^", use_container_width=True, on_click=press, args=("^",))

# 행 2: 로그·루트·괄호
r1 = st.columns(4)
with r1[0]: st.button("log(a,b)", use_container_width=True, on_click=press, args=("log(",))
with r1[1]: st.button("√", use_container_width=True, on_click=press, args=("√(",))
with r1[2]: st.button("(", use_container_width=True, on_click=press, args=("(",))
with r1[3]: st.button(")", use_container_width=True, on_click=press, args=(")",))

# 행 3~5: 숫자 + 사칙연산
r2 = st.columns(4)
with r2[0]: st.button("7", use_container_width=True, on_click=press, args=("7",))
with r2[1]: st.button("8", use_container_width=True, on_click=press, args=("8",))
with r2[2]: st.button("9", use_container_width=True, on_click=press, args=("9",))
with r2[3]: st.button("÷", use_container_width=True, on_click=press, args=("/",))

r3 = st.columns(4)
with r3[0]: st.button("4", use_container_width=True, on_click=press, args=("4",))
with r3[1]: st.button("5", use_container_width=True, on_click=press, args=("5",))
with r3[2]: st.button("6", use_container_width=True, on_click=press, args=("6",))
with r3[3]: st.button("×", use_container_width=True, on_click=press, args=("*",))

r4 = st.columns(4)
with r4[0]: st.button("1", use_container_width=True, on_click=press, args=("1",))
with r4[1]: st.button("2", use_container_width=True, on_click=press, args=("2",))
with r4[2]: st.button("3", use_container_width=True, on_click=press, args=("3",))
with r4[3]: st.button("−", use_container_width=True, on_click=press, args=("-",))

r5 = st.columns(4)
with r5[0]: st.button("0", use_container_width=True, on_click=press, args=("0",))
with r5[1]: st.button(".", use_container_width=True, on_click=press, args=(".",))
with r5[2]: st.button(",", use_container_width=True, on_click=press, args=(",",))
with r5[3]: st.button("+", use_container_width=True, on_click=press, args=("+",))

# = 버튼
st.button("＝", use_container_width=True, on_click=calculate, type="primary")

# ── 계산 기록 ─────────────────────────────────────────────
if st.session_state.history:
    st.divider()
    st.markdown("### 📋 계산 기록")
    for h in reversed(st.session_state.history[-10:]):
        st.text(h)
    if st.button("기록 지우기"):
        st.session_state.history = []

st.divider()
st.caption("Made with ❤️ using Streamlit · 중앙대학교병원 병동간호 1팀")
