import streamlit as st
import math
import random
import pandas as pd
import streamlit.components.v1 as components

try:
    import plotly.graph_objects as go
    PLOTLY_OK = True
except ImportError:
    PLOTLY_OK = False

st.set_page_config(page_title="멀티 앱", page_icon="🧮", layout="centered")

# ── 사이드바 메뉴 ─────────────────────────────────────────
st.sidebar.title("📂 메뉴")
menu = st.sidebar.radio(
    "앱을 선택하세요",
    ["🧮 계산기", "🎲 확률 시뮬레이터"],
)

# ════════════════════════════════════════════════════════════
#  1. 계산기
# ════════════════════════════════════════════════════════════
if menu == "🧮 계산기":

    if "expression" not in st.session_state:
        st.session_state.expression = ""
    if "result" not in st.session_state:
        st.session_state.result = ""
    if "history" not in st.session_state:
        st.session_state.history = []

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

    r0 = st.columns(4)
    with r0[0]: st.button("AC",       key="b_ac",   use_container_width=True, on_click=clear_all)
    with r0[1]: st.button("⌫",       key="b_bk",   use_container_width=True, on_click=backspace)
    with r0[2]: st.button("mod",      key="b_mod",  use_container_width=True, on_click=press, args=("mod",))
    with r0[3]: st.button("^",        key="b_pow",  use_container_width=True, on_click=press, args=("^",))

    r1 = st.columns(4)
    with r1[0]: st.button("log(a,b)", key="b_log",  use_container_width=True, on_click=press, args=("log(",))
    with r1[1]: st.button("√",        key="b_sqrt", use_container_width=True, on_click=press, args=("√(",))
    with r1[2]: st.button("(",        key="b_lp",   use_container_width=True, on_click=press, args=("(",))
    with r1[3]: st.button(")",        key="b_rp",   use_container_width=True, on_click=press, args=(")",))

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
    with r5[0]: st.button("0",   key="b_0",   use_container_width=True, on_click=press, args=("0",))
    with r5[1]: st.button(".",   key="b_dot", use_container_width=True, on_click=press, args=(".",))
    with r5[2]: st.button("( )", key="b_par", use_container_width=True, on_click=press, args=("(",))
    with r5[3]: st.button("+",   key="b_add", use_container_width=True, on_click=press, args=("+",))

    st.button("＝  계산하기", key="b_eq", use_container_width=True,
              on_click=calculate, type="primary")

    components.html("""
    <script>
      function applyColors() {
        const btns = window.parent.document.querySelectorAll('button');
        btns.forEach(btn => {
          const txt = btn.innerText.trim();
          if (txt === 'AC' || txt === '⌫') {
            btn.style.setProperty('background-color', '#c62828', 'important');
            btn.style.setProperty('color', 'white', 'important');
          } else if (['+', '−', '×', '÷', 'mod', '^'].includes(txt)) {
            btn.style.setProperty('background-color', '#1565c0', 'important');
            btn.style.setProperty('color', 'white', 'important');
          }
        });
      }
      applyColors();
      setTimeout(applyColors, 300);
      setTimeout(applyColors, 800);
    </script>
    """, height=0, scrolling=False)

    if st.session_state.history:
        st.divider()
        st.markdown("### 📋 계산 기록")
        for h in reversed(st.session_state.history[-10:]):
            st.code(h, language=None)
        if st.button("🗑️ 기록 지우기", key="b_clrhist"):
            st.session_state.history = []

    st.divider()
    st.caption("Made with ❤️ using Streamlit · 중앙대학교병원 병동간호 1팀")


# ════════════════════════════════════════════════════════════
#  2. 확률 시뮬레이터
# ════════════════════════════════════════════════════════════
elif menu == "🎲 확률 시뮬레이터":

    st.title("🎲 확률 시뮬레이터")
    st.markdown("주사위 또는 동전을 여러 번 던져 결과를 시각화합니다.")

    if not PLOTLY_OK:
        st.error("plotly 라이브러리를 불러올 수 없습니다. requirements.txt에 plotly==5.18.0 이 있는지 확인하세요.")
        st.stop()

    st.divider()

    col_left, col_right = st.columns(2)
    with col_left:
        sim_type = st.selectbox("시뮬레이션 종류", ["🎲 주사위", "🪙 동전"])
    with col_right:
        trials = st.number_input(
            "시행 횟수", min_value=10, max_value=100000, value=100, step=10
        )

    if sim_type == "🎲 주사위":
        dice_faces = st.slider("주사위 면의 수", min_value=4, max_value=20, value=6, step=2)

    run_btn = st.button("▶ 시뮬레이션 실행", type="primary", use_container_width=True)

    if run_btn:
        st.divider()

        # ── 주사위 ────────────────────────────────────────
        if sim_type == "🎲 주사위":
            results = [random.randint(1, dice_faces) for _ in range(int(trials))]
            counts  = {i: results.count(i) for i in range(1, dice_faces + 1)}
            labels  = [f"{i}면" for i in counts.keys()]
            values  = list(counts.values())
            expected     = int(trials) / dice_faces
            expected_pct = round(100 / dice_faces, 2)
            actual_pcts  = [round(v / int(trials) * 100, 2) for v in values]

            st.subheader(f"🎲 {dice_faces}면 주사위 {int(trials):,}회 결과")

            # 막대 그래프
            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(
                x=labels, y=values,
                marker_color="#1565c0",
                text=values, textposition="outside",
                name="횟수"
            ))
            fig_bar.add_hline(
                y=expected, line_dash="dash", line_color="red",
                annotation_text=f"이론값 ({expected:.1f}회)",
                annotation_position="top right"
            )
            fig_bar.update_layout(
                title="각 면별 출현 횟수",
                xaxis_title="주사위 면", yaxis_title="횟수",
                plot_bgcolor="#f9f9f9", height=400
            )
            st.plotly_chart(fig_bar, use_container_width=True)

            # 파이 차트
            fig_pie = go.Figure(go.Pie(
                labels=labels, values=values,
                hole=0.35, textinfo="label+percent"
            ))
            fig_pie.update_layout(title="각 면별 출현 비율", height=400)
            st.plotly_chart(fig_pie, use_container_width=True)

            # 수렴 그래프
            cumulative, count_1 = [], 0
            for i, r in enumerate(results, 1):
                if r == 1:
                    count_1 += 1
                cumulative.append(round(count_1 / i * 100, 2))

            fig_conv = go.Figure()
            fig_conv.add_trace(go.Scatter(
                x=list(range(1, int(trials) + 1)), y=cumulative,
                mode="lines", line=dict(color="#1565c0", width=1.5),
                name="1면 출현율"
            ))
            fig_conv.add_hline(
                y=expected_pct, line_dash="dash", line_color="red",
                annotation_text=f"이론 확률 {expected_pct}%"
            )
            fig_conv.update_layout(
                title="'1면' 누적 출현율 수렴 그래프",
                xaxis_title="시행 횟수", yaxis_title="누적 출현율 (%)",
                plot_bgcolor="#f9f9f9", height=350
            )
            st.plotly_chart(fig_conv, use_container_width=True)

            # 통계표
            st.subheader("📊 상세 통계표")
            df = pd.DataFrame({
                "면": labels,
                "출현 횟수": values,
                "실제 확률 (%)": actual_pcts,
                "이론 확률 (%)": [expected_pct] * dice_faces,
                "차이 (%)": [round(a - expected_pct, 2) for a in actual_pcts]
            })
            st.dataframe(df, use_container_width=True, hide_index=True)

        # ── 동전 ──────────────────────────────────────────
        elif sim_type == "🪙 동전":
            results = [random.choice(["앞면", "뒷면"]) for _ in range(int(trials))]
            heads   = results.count("앞면")
            tails   = results.count("뒷면")

            st.subheader(f"🪙 동전 {int(trials):,}회 결과")

            c1, c2 = st.columns(2)
            c1.metric("앞면 (HEAD)", f"{heads}회",
                      f"{round(heads / int(trials) * 100, 1)}%")
            c2.metric("뒷면 (TAIL)", f"{tails}회",
                      f"{round(tails / int(trials) * 100, 1)}%")

            # 막대 그래프
            fig_bar = go.Figure(go.Bar(
                x=["앞면", "뒷면"], y=[heads, tails],
                marker_color=["#1565c0", "#c62828"],
                text=[heads, tails], textposition="outside"
            ))
            fig_bar.add_hline(
                y=int(trials) / 2, line_dash="dash", line_color="green",
                annotation_text=f"이론값 ({int(trials)//2}회)"
            )
            fig_bar.update_layout(
                title="앞면 / 뒷면 출현 횟수",
                yaxis_title="횟수", plot_bgcolor="#f9f9f9", height=400
            )
            st.plotly_chart(fig_bar, use_container_width=True)

            # 파이 차트
            fig_pie = go.Figure(go.Pie(
                labels=["앞면", "뒷면"], values=[heads, tails],
                hole=0.35,
                marker_colors=["#1565c0", "#c62828"],
                textinfo="label+percent"
            ))
            fig_pie.update_layout(title="앞면 / 뒷면 비율", height=400)
            st.plotly_chart(fig_pie, use_container_width=True)

            # 수렴 그래프
            cumulative, cnt = [], 0
            for i, r in enumerate(results, 1):
                if r == "앞면":
                    cnt += 1
                cumulative.append(round(cnt / i * 100, 2))

            fig_conv = go.Figure()
            fig_conv.add_trace(go.Scatter(
                x=list(range(1, int(trials) + 1)), y=cumulative,
                mode="lines", line=dict(color="#1565c0", width=1.5),
                name="앞면 출현율"
            ))
            fig_conv.add_hline(
                y=50, line_dash="dash", line_color="red",
                annotation_text="이론 확률 50%"
            )
            fig_conv.update_layout(
                title="앞면 누적 출현율 수렴 그래프",
                xaxis_title="시행 횟수", yaxis_title="누적 출현율 (%)",
                plot_bgcolor="#f9f9f9", height=350
            )
            st.plotly_chart(fig_conv, use_container_width=True)

            # 통계표
            st.subheader("📊 상세 통계표")
            df = pd.DataFrame({
                "결과": ["앞면", "뒷면"],
                "출현 횟수": [heads, tails],
                "실제 확률 (%)": [round(heads/int(trials)*100, 2),
                                   round(tails/int(trials)*100, 2)],
                "이론 확률 (%)": [50.0, 50.0],
                "차이 (%)": [round(heads/int(trials)*100 - 50, 2),
                              round(tails/int(trials)*100 - 50, 2)]
            })
            st.dataframe(df, use_container_width=True, hide_index=True)

    st.divider()
    st.caption("Made with ❤️ using Streamlit · 중앙대학교병원 병동간호 1팀")
