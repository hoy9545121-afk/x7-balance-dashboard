"""성장 밸런스 뷰 — 캐릭터 레벨 경험치 테이블 및 시각화"""
from __future__ import annotations
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from simulator.calc import required_xp
from simulator.constants import C

def render_growth_view():
    st.header("📈 캐릭터 성장 밸런스")
    
    # 1. 경험치 공식 안내
    st.info("💡 **경험치 공식**: $req\_xp(lv) = 4300 \\times 1.065^{(lv-1)}$")
    
    # 2. 레벨 테이블 데이터 생성
    levels = range(1, 101)
    xp_data = []
    cum_xp = 0
    for lv in levels:
        req = required_xp(lv)
        cum_xp += req
        xp_data.append({
            "레벨": lv,
            "해당 레벨 필요 XP": round(req),
            "누적 XP": round(cum_xp)
        })
    
    df_xp = pd.DataFrame(xp_data)
    
    # 3. 차트 시각화
    st.subheader("📊 경험치 요구량 곡선")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_xp["레벨"], y=df_xp["해당 레벨 필요 XP"],
        name="필요 XP", mode="lines",
        line=dict(color=C["accent"], width=3),
        fill="tozeroy", fillcolor="rgba(232, 184, 75, 0.1)"
    ))
    fig.update_layout(
        paper_bgcolor=C["bg"], plot_bgcolor=C["panel"],
        font=dict(color=C["text"]),
        xaxis=dict(title="레벨", gridcolor=C["border"]),
        yaxis=dict(title="경험치", gridcolor=C["border"]),
        margin=dict(l=40, r=20, t=20, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # 4. 상세 테이블 (익스팬더)
    st.subheader("📝 레벨별 상세 경험치 테이블")
    st.dataframe(
        df_xp,
        column_config={
            "레벨": st.column_config.NumberColumn(format="%d"),
            "해당 레벨 필요 XP": st.column_config.NumberColumn(format="%d"),
            "누적 XP": st.column_config.NumberColumn(format="%d"),
        },
        hide_index=True,
        use_container_width=True
    )
