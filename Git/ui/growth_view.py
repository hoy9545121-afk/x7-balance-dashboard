"""성장 밸런스 뷰 — HTML 기획 확정안 기반 (v2026-03-19)"""
from __future__ import annotations
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from simulator.calc import required_xp
from simulator.constants import C, MASTERY_TIER_REQ

def render_growth_view():
    st.header("📈 캐릭터 및 숙련도 성장 밸런스")
    
    # ── 1. 지역별 성장 앵커 (HTML 1-2 섹션) ─────────────────────
    st.subheader("🗺 지역별 성장 기준표 (Anchor Time)")
    st.caption("※ T1 Normal 필드 사냥(500 XP/min) 기준 완료 시간입니다.")
    
    anchor_data = [
        {"지역": "이니스 섬", "레벨 구간": "1~10", "완료 레벨": "10레벨", "누계 시간": "2h", "숙련도": "1T"},
        {"지역": "솔즈리드 반도", "레벨 구간": "11~20", "완료 레벨": "20레벨", "누계 시간": "6h", "숙련도": "2T"},
        {"지역": "릴리엇 구릉지", "레벨 구간": "21~30", "완료 레벨": "30레벨", "누계 시간": "12h", "숙련도": "3T"},
        {"지역": "가랑돌 평원", "레벨 구간": "31~40", "완료 레벨": "40레벨", "누계 시간": "30h", "숙련도": "4T"},
        {"지역": "마리아 노플", "레벨 구간": "41~50", "완료 레벨": "50레벨", "누계 시간": "90h", "숙련도": "5T"},
        {"지역": "지옥 늪지대", "레벨 구간": "51~55", "완료 레벨": "55레벨", "누계 시간": "170h", "숙련도": "6T"},
        {"지역": "긴 모래톱", "레벨 구간": "56~60", "완료 레벨": "60레벨", "누계 시간": "330h", "숙련도": "7T"},
        {"지역": "만렙 구간", "레벨 구간": "61~100", "완료 레벨": "100레벨", "누계 시간": "1,200h", "숙련도": "7T"},
    ]
    st.table(pd.DataFrame(anchor_data))

    # ── 2. 경험치 요구량 차트 ─────────────────────────────────
    st.subheader("📊 레벨별 필요 경험치 곡선")
    levels = range(1, 101)
    xp_list = [required_xp(lv) for lv in levels]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(levels), y=xp_list,
        mode="lines", name="필요 XP",
        line=dict(color=C["accent"], width=3),
        fill="tozeroy", fillcolor="rgba(232, 184, 75, 0.1)"
    ))
    fig.update_layout(
        paper_bgcolor=C["bg"], plot_bgcolor=C["panel"],
        font=dict(color=C["text"]),
        xaxis=dict(title="캐릭터 레벨", gridcolor=C["border"]),
        yaxis=dict(title="해당 레벨 필요 XP", gridcolor=C["border"]),
        margin=dict(l=40, r=20, t=20, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── 3. 숙련도 시스템 (HTML 2-2 섹션) ───────────────────────
    st.markdown("---")
    st.subheader("🏆 숙련도 티어 요구량")
    st.info("💡 **숙련도 획득**: 분당 300 XP 고정 (전투 중 획득)")
    
    m_data = []
    for tier, req in MASTERY_TIER_REQ.items():
        m_data.append({
            "티어": tier,
            "총 필요 숙련도 XP": f"{req:,}",
            "달성 소요 시간": f"{req / (300 * 60):.1f}h"
        })
    st.table(pd.DataFrame(m_data))

    # ── 4. 상세 XP 테이블 (익스팬더) ──────────────────────────
    with st.expander("📝 캐릭터 레벨별 상세 데이터 (1~100)", expanded=False):
        detailed_xp = []
        cum_xp = 0
        for lv in range(1, 101):
            req = required_xp(lv)
            cum_xp += req
            detailed_xp.append({
                "Lv": lv,
                "필요 XP": f"{round(req):,}",
                "누적 XP": f"{round(cum_xp):,}",
                "예상 누적 시간": f"{cum_xp / (500 * 60):.1f}h"
            })
        st.dataframe(pd.DataFrame(detailed_xp), hide_index=True, use_container_width=True)
