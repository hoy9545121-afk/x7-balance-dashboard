"""PVP 결과 패널 — 통계 & 차트 (아레나는 app.py에서 위에 렌더링됨)"""
from __future__ import annotations
import os
import streamlit as st
from simulator.models import PvpResult, PlayerConfig
from simulator.calc import player_final_atk, player_final_def, player_hp, player_atk_speed
from simulator.constants import CAPS, ASSET_ROOT, WEAPON_ICON_KEY
from charts.plotly_charts import hp_timeline_chart, stats_bar_chart, radar_chart


def render_pvp_results(result: PvpResult, p1: PlayerConfig, p2: PlayerConfig) -> None:
    with st.expander("📊 상세 분석", expanded=False):
        ttk1_str = f"{result.ttk1:.2f}s" if result.ttk1 < float("inf") else "∞"
        ttk2_str = f"{result.ttk2:.2f}s" if result.ttk2 < float("inf") else "∞"

        def eff_hp(hp, def_):
            return round(hp * (1 + 500 / def_)) if def_ > 0 else hp

        def def_reduction(def_):
            return round(def_ / (def_ + 500) * 100, 1)

        p1_fatk = player_final_atk(p1)
        p2_fatk = player_final_atk(p2)
        p1_fdef = player_final_def(p1)
        p2_fdef = player_final_def(p2)
        p1_hp   = player_hp(p1)
        p2_hp   = player_hp(p2)

        def weapon_icon_path(cfg: PlayerConfig) -> str | None:
            key = WEAPON_ICON_KEY.get(cfg.weapon_type)
            if not key:
                return None
            return os.path.join(ASSET_ROOT, "weapons", f"weapon_{key}.png")

        col1, col2 = st.columns(2)
        with col1:
            icon1 = weapon_icon_path(p1)
            if icon1 and os.path.exists(icon1):
                st.image(icon1, width=48)
            st.markdown("**P1**")
            st.metric("DPS (vs P2)", f"{result.p1_sim.avg_dps:,.0f}")
            # 버프 기여도 계산 (120초 총 데미지 기준)
            p1_total = result.p1_sim.avg_dps * 60.0
            p1_buff_p = (result.p1_sim.buff_dmg / p1_total * 100) if p1_total > 0 else 0
            st.metric("버프 기여도", f"{p1_buff_p:.1f}%")
            st.metric("TTK", ttk1_str)
            st.metric("실효 HP", f"{eff_hp(p1_hp, p1_fdef):,}")
        with col2:
            icon2 = weapon_icon_path(p2)
            if icon2 and os.path.exists(icon2):
                st.image(icon2, width=48)
            st.markdown("**P2**")
            st.metric("DPS (vs P1)", f"{result.p2_sim.avg_dps:,.0f}")
            # 버프 기여도 계산 (120초 총 데미지 기준)
            p2_total = result.p2_sim.avg_dps * 60.0
            p2_buff_p = (result.p2_sim.buff_dmg / p2_total * 100) if p2_total > 0 else 0
            st.metric("버프 기여도", f"{p2_buff_p:.1f}%")
            st.metric("TTK", ttk2_str)
            st.metric("실효 HP", f"{eff_hp(p2_hp, p2_fdef):,}")

        st.plotly_chart(hp_timeline_chart(result.hp_timeline), use_container_width=True)

        labels = ["ATK", "DEF", "DPS", "HP"]
        p1_vals_bar = [p1_fatk, p1_fdef, result.p1_sim.avg_dps, p1_hp]
        p2_vals_bar = [p2_fatk, p2_fdef, result.p2_sim.avg_dps, p2_hp]
        st.plotly_chart(stats_bar_chart(labels, p1_vals_bar, p2_vals_bar), use_container_width=True)

        max_vals = [
            max(p1_fatk, p2_fatk) or 1,
            max(p1_fdef, p2_fdef) or 1,
            max(result.p1_sim.avg_dps, result.p2_sim.avg_dps) or 1,
            max(p1_hp, p2_hp) or 1,
            max(player_atk_speed(p1), player_atk_speed(p2)) or 1,
        ]
        radar_labels = ["ATK", "DEF", "DPS", "HP", "SPD"]
        p1_spd = player_atk_speed(p1)
        p2_spd = player_atk_speed(p2)
        p1_radar = [round(v / m * 100) for v, m in zip(
            [p1_fatk, p1_fdef, result.p1_sim.avg_dps, p1_hp, p1_spd], max_vals)]
        p2_radar = [round(v / m * 100) for v, m in zip(
            [p2_fatk, p2_fdef, result.p2_sim.avg_dps, p2_hp, p2_spd], max_vals)]
        st.plotly_chart(radar_chart(radar_labels, p1_radar, p2_radar), use_container_width=True)
