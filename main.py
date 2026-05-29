import streamlit as st
import math
import streamlit.components.v1 as components

st.set_page_config(page_title="계산기", page_icon="🧮", layout="centered")

# ── 세션 상태 초기화 ──────────────────────────────
if "expression" not in st.session_state:
    st.session_state.expression = ""
if "result" not in st.session_state:
    st.session_state.result = ""
if "history" not in st.session_state:
    st.session_state.history = []

# ── 버튼 동작 함수 ────────────────────────────────
def press(val):
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
        safe = (
            expr
            .replace("^", "**")
            .replace("mod", "%")
            .replace("log(", "math.log(")
            .replace("√(", "math.sqrt(")
        )
        res = eval(safe, {"__builtins__": {}, "math": math})
        res_str = f"{res:,.10g}"
        st.session_state.history.append(f"{expr} = {res_str}")
        st.session_state.result = res_str
    except ZeroDivisionError:
        st.session_state.result = "⚠️ 0으로 나눌 수 없습니다"
    except Exception:
        st.session_state.result = "⚠️ 수식 오류"

# ── 화면 표시 ─────────────────────────────────────
st.title("🧮 다기능 계산기")

expr_display = st.session_state.expression if st.session_state.expression else "0"
result_display = f"= {st.session_state.result}" if st.session_state.result else "&nbsp;"
result_color = "#ff5252" if "⚠️" in st.session_state.result else "#4fc3f7"

st.markdown(f"""
<div style="background:#1e1e1e; color:#ffffff; font-size:1.4rem;
     padding:0.8rem 1rem; border-radius:10px 10px 0 0;
     text-align:right; min-height:3rem; word-break:break-all;">
  {expr_display}
</div>
<div style="background:#2a2a2a; color:{result_color}; font-size:2rem; font-weight:bold;
     padding:0.5rem 1rem; border-radius:0 0 10px 10px;
     text-align:right; min-height:3rem;">
  {result_display}
</div>
<br>
""", unsafe_allow_html=True)

# ── 버튼 레이아웃 ─────────────────────────────────

# 행 1: AC, ⌫, mod, ^
r0 = st.columns(4)
with r0[0]: st.button("AC",       key="b_ac",   use_container_width=True, on_click=clear_all)
with r0[1]: st.button("⌫",       key="b_bk",   use_container_width=True, on_click=backspace)
with r0[2]: st.button("mod",      key="b_mod",  use_container_width=True, on_click=press, args=("mod",))
with r0[3]: st.button("^",        key="b_pow",  use_container_width=True, on_click=press, args=("^",))

# 행 2: log, √, (, )
r1 = st.columns(4)
with r1[0]: st.button("log(a,b)", key="b_log",  use_container_width=True, on_click=press, args=("log(",))
with r1[1]: st.button("√",        key="b_sqrt", use_container_width=True, on_click=press, args=("√(",))
with r1[2]: st.button("(",        key="b_lp",   use_container_width=True, on_click=press, args=("(",))
with r1[3]: st.button(")",        key="b_rp",   use_container_width=True, on_click=press, args=(")",))

# 행 3~5: 숫자 + 사칙연산
r2 = st.columns(4)
with r2[0]: st.button("7", key="b_7", use_container_width=True, on_click=press, args=("7",))
with r2[1]: st.button("8", key="b_8", use_container_width=True, on_click=press, args=("8",))
with r2[2]: st.button("9", key="b_9", use_container_width=True, on_click=press, args=("9",))
with r2[3]: st.button("÷", key="b_div", use_container_width=True, on_click=press, args=("/",))

r3 = st.columns(4)
with r3[0]: st.button("4", key="b_4", use_container_width=True, on_click=press, args=("4",))
with r3[1]: st.button("5", key="b_5", use_container_width=True, on_click=press, args=("5",))
with r3[2]: st.button("6", key="b_6", use_container_width=True, on_click=press, args=("6",))
with r3[3]: st.button("×", key="b_mul", use_container_width=True, on_click=press, args=("*",))

r4 = st.columns(4)
with r4[0]: st.button("1", key="b_1", use_container_width=True, on_click=press, args=("1",))
with r4[1]: st.button("2", key="b_2", use_container_width=True, on_click=press, args=("2",))
with r4[2]: st.button("3", key="b_3", use_container_width=True, on_click=press, args=("3",))
with r4[3]: st.button("−", key="b_sub", use_container_width=True, on_click=press, args=("-",))

r5 = st.columns(4)
with r5[0]: st.button("0", key="b_0",     use_container_width=True, on_click=press, args=("0",))
with r5[1]: st.button(".", key="b_dot",   use_container_width=True, on_click=press, args=(".",))
with r5[2]: st.button("( )", key="b_par", use_container_width=True, on_click=press, args=("(",))
with r5[3]: st.button("+", key="b_add",   use_container_width=True, on_click=press, args=("+",))

# = 버튼
st.button("＝  계산하기", key="b_eq", use_container_width=True,
          on_click=calculate, type="primary")

# ── 버튼 색상 주입 (JS) ───────────────────────────
components.html("""
<script>
  function applyColors() {
    const btns = window.parent.document.querySelectorAll('button');
    btns.forEach(btn => {
      const txt = btn.innerText.trim();
      // 빨간색: AC, ⌫
      if (txt === 'AC' || txt === '⌫') {
        btn.style.setProperty('background-color', '#c62828', 'important');
        btn.style.setProperty('color', 'white', 'important');
        btn.style.setProperty('border', '1px solid #b71c1c', 'important');
      }
      // 파란색: 사칙연산자 + 모듈러 + 지수
      else if (['+', '−', '×', '÷', 'mod', '^'].includes(txt)) {
        btn.style.setProperty('background-color', '#1565c0', 'important');
        btn.style.setProperty('color', 'white', 'important');
        btn.style.setProperty('border', '1px solid #0d47a1', 'important');
      }
    });
  }
  applyColors();
  setTimeout(applyColors, 300);
  setTimeout(applyColors, 800);
</script>
""", height=0, scrolling=False)

# ── 계산 기록 ─────────────────────────────────────
if st.session_state.history:
    st.divider()
    st.markdown("### 📋 계산 기록")
    for h in reversed(st.session_state.history[-10:]):
        st.code(h, language=None)
    if st.button("🗑️ 기록 지우기", key="b_clrhist"):
        st.session_state.history = []

st.divider()
st.caption("Made with ❤️ using Streamlit · 중앙대학교병원 병동간호 1팀")
    
