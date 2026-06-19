"""X7 스킨 UI — 클로젯 (Skin UI — Closet)
실행: streamlit run app.py
"""
import streamlit as st

st.set_page_config(
    page_title  = "X7 스킨 UI — Closet",
    page_icon   = "✦",
    layout      = "wide",
    initial_sidebar_state="collapsed",
)

# 전역 배경/스크롤 즉시 적용 (CSS flash 방지)
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"] {
    background-color: #060b14 !important;
}
[data-testid="stSidebar"] { background-color: #0b1220 !important; }
</style>
""", unsafe_allow_html=True)

from ui.closet_ui import render_closet
render_closet()
