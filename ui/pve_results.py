"""PVE 결과 패널 — 통계 & 차트 (V4: 필드/던전 경로 선택 포함)"""
from __future__ import annotations
import streamlit as st
from simulator.models import PveResult, PlayerConfig, MonsterConfig, MonteCarloSummary
from simulator.monte_carlo import MonteCarloEngine
from simulator.calc import player_final_atk, player_final_def
from charts.plotly_charts import dps_line_chart, stats_bar_chart, pie_chart
from simulator.constants import CRAFT_SPOILS_REQ, CRAFT_CORE_REQ

def render_pve_results(result: PveResult, p1: PlayerConfig, p2: PlayerConfig, monster: MonsterConfig) -> None:
    # ── 1. 상세 전투 통계 ─────────────────────────────────────
    with st.expander("📊 상세 전투 분석", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Player 1**")
            st.metric("평균 DPS", f"{result.solo1.avg_dps:,.0f}")
            st.metric("120초 킬수", f"{result.kills1}마리")
        with col2:
            st.markdown("**몬스터 스펙**")
            st.metric("HP / DEF", f"{result.mon_hp:,} / {result.mon_def:,}")
        with col3:
            st.markdown("**Player 2**")
            st.metric("평균 DPS", f"{result.solo2.avg_dps:,.0f}")
            st.metric("120초 킬수", f"{result.kills2}마리")

    # ── 2. 성장 효율 비교 (120초 기준) ──────────────────────
    st.markdown("### 📈 성장 효율 비교 (120초 기준)")
    e_col1, e_col2 = st.columns(2)
    with e_col1:
        st.info("**P1 성장 지표**")
        st.write(f"🔹 **획득 XP**: {result.solo1.total_xp:,.0f} | **숙련도**: {result.solo1.total_mastery:,.0f}")
        st.write(f"🔹 **재료 드랍(평균)**: {result.solo1.est_drops:.2f}개")
    with e_col2:
        st.info("**P2 성장 지표**")
        st.write(f"🔹 **획득 XP**: {result.solo2.total_xp:,.0f} | **숙련도**: {result.solo2.total_mastery:,.0f}")
        st.write(f"🔹 **재료 드랍(평균)**: {result.solo2.est_drops:.2f}개")

    # ── 3. 몬테카를로 장기 파밍 분석 (V4) ──────────────────────
    st.markdown("---")
    st.markdown("### 🎲 몬테카를로 제작 경로 분석")
    
    c1, c2 = st.columns(2)
    with c1:
        route = st.radio("파밍 경로 선택", ["필드(전리품)", "던전(코어)"], horizontal=True)
    with c2:
        period_opt = st.selectbox("파밍 기간 선택", ["1시간", "1일 (24h)", "1달 (30일)"], index=0)
    
    hours_map = {"1시간": 1.0, "1일 (24h)": 24.0, "1달 (30일)": 720.0}
    selected_hours = hours_map[period_opt]
    
    # 제작 목표 수량 가이드 (ECON_SPEC 5-2)
    target_label = "전리품" if route == "필드(전리품)" else "던전 코어"
    target_req = CRAFT_SPOILS_REQ.get(monster.tier, 60) if route == "필드(전리품)" else CRAFT_CORE_REQ.get(monster.tier, 3)
    
    st.caption(f"💡 **제작 목표**: {monster.tier} 무기 1파츠 제작 시 **{target_label} {target_req}개**가 필요합니다. (기획서 5-2 섹션 기준)")

    with st.spinner(f"{route} 시뮬레이션 중..."):
        mc1 = MonteCarloEngine.run_time_sim(p1, monster, hours=selected_hours, iterations=1000, route=route)
        mc2 = MonteCarloEngine.run_time_sim(p2, monster, hours=selected_hours, iterations=1000, route=route)
    
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        st.success(f"**P1 {target_label} 획득 분포**")
        labels = [b.range_label for b in mc1.buckets]
        values = [b.probability for b in mc1.buckets]
        st.plotly_chart(pie_chart(labels, values, f"P1 {target_label} 확률"), use_container_width=True)
        st.write(f"🎯 **평균**: {mc1.avg_items:,.1f}개 | **최소보장(P95)**: **{mc1.p95_items:,}개**")
        progress = min(mc1.avg_items / target_req, 1.0)
        st.progress(progress, f"제작 목표 달성률: {progress*100:.1f}%")
        
    with m_col2:
        st.success(f"**P2 {target_label} 획득 분포**")
        labels = [b.range_label for b in mc2.buckets]
        values = [b.probability for b in mc2.buckets]
        st.plotly_chart(pie_chart(labels, values, f"P2 {target_label} 확률"), use_container_width=True)
        st.write(f"🎯 **평균**: {mc2.avg_items:,.1f}개 | **최소보장(P95)**: **{mc2.p95_items:,}개**")
        progress = min(mc2.avg_items / target_req, 1.0)
        st.progress(progress, f"제작 목표 달성률: {progress*100:.1f}%")

    with st.expander("📝 상세 데이터 로그", expanded=False):
        st.write(f"🔹 시뮬레이션 기간: {selected_hours}시간")
        st.write(f"🔹 {monster.tier} 기준 {target_label} 요구량: {target_req}개")
        st.write("※ 던전 코어는 1회 클리어 시 T2=3개, T3+=5개를 획득하며 회당 15분이 소요된다고 가정합니다.")
