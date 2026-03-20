"""몬스터 설정 패널 — 헤더 시인성 강화 버전"""
from __future__ import annotations
import streamlit as st
from simulator.constants import TIERS, MON_GRADES_LIST, MON_BASE, MON_GRADE
from simulator.models import MonsterConfig


def render_monster_config() -> MonsterConfig:
    """몬스터 설정 아코디언."""
    with st.expander("😈 몬스터", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            tier = st.selectbox("티어", TIERS, index=2)  # 기본 Tier3
        with c2:
            grade = st.selectbox("등급", MON_GRADES_LIST, index=0)  # 기본 Normal

        cfg = MonsterConfig(tier=tier, grade=grade)
        
        # 실시간 스탯 요약 (시인성 강조)
        stats = _get_monster_summary(cfg)
        st.markdown(
            f"<div style='font-size:13px; color:#7a9ab8; font-weight:600; margin-top:8px;'>"
            f"HP <span style='color:#e84b4b'>{stats['hp']:,}</span> · "
            f"ATK <span style='color:#e8b84b'>{stats['atk']:,}</span> · "
            f"DEF <span style='color:#4b8ce8'>{stats['def']:,}</span>"
            "</div>",
            unsafe_allow_html=True
        )
        
    return cfg


def _get_monster_summary(cfg: MonsterConfig) -> dict:
    b = MON_BASE[cfg.tier]
    m = MON_GRADE[cfg.grade]
    return {
        "atk": round(b["atk"] * m["atk_mult"]),
        "def": round(b["def"] * m["def_mult"]),
        "hp":  round(b["hp"]  * m["hp_mult"]),
    }
