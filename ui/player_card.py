"""플레이어 설정 패널 — 장비 슬롯에 추가 옵션(1-6단계) UI 포함"""
from __future__ import annotations
import streamlit as st
from simulator.constants import (
    TIERS, GRADES, TIER_MAX_GRADE, GRADE_ORDER,
    WEAPON_TYPES, SKILLS, SKILL_CMDS, CAPS,
    GRADE_COLOR, TIER_COLOR, CMD_COLOR,
)
from simulator.models import EquipSlot, PlayerConfig
from simulator.calc import (
    player_base_atk, player_base_def,
    player_final_atk, player_final_def,
    player_hp, player_mp, player_regen_mp, player_atk_speed, effective_cd,
)


# ── 공통 헬퍼 ────────────────────────────────────────────

_ACCESSORY_SLOTS = {"ring1", "ring2", "neck", "ear"}
_LOCKED_TIERS = {"Tier1", "Tier2"}


def _eq_row(label: str, slot_key: str, cfg: PlayerConfig, prefix: str) -> None:
    """장비 슬롯 한 행 (추가 옵션 포함)."""
    slot: EquipSlot = getattr(cfg, slot_key)
    is_acc = slot_key in _ACCESSORY_SLOTS
    max_grade = TIER_MAX_GRADE[slot.tier]
    avail_grades = GRADES[: GRADE_ORDER[max_grade] + 1]

    st.caption(label)
    c1, c2, c3, c4 = st.columns([2, 2, 1, 2])
    with c1:
        new_tier = st.selectbox(
            "티어", TIERS, index=TIERS.index(slot.tier),
            key=f"{prefix}_{slot_key}_tier", label_visibility="collapsed",
        )
    is_locked = is_acc and new_tier in _LOCKED_TIERS
    with c2:
        cur_grade = slot.grade if slot.grade in avail_grades else avail_grades[-1]
        new_grade = st.selectbox(
            "등급", avail_grades, index=avail_grades.index(cur_grade),
            key=f"{prefix}_{slot_key}_grade", label_visibility="collapsed",
            disabled=is_locked,
        )
    with c3:
        new_enh = st.number_input(
            "강화", min_value=0, max_value=10, value=slot.enh, step=1,
            key=f"{prefix}_{slot_key}_enh", label_visibility="collapsed",
            disabled=is_locked,
        )
    with c4:
        # 추가 옵션 선택 (0: 없음, 1~6단계)
        opt_labels = ["옵션 없음"] + [f"{i}단계" for i in range(1, 7)]
        new_opt = st.selectbox(
            "추가 옵션", range(7), index=slot.add_opt,
            format_func=lambda x: opt_labels[x],
            key=f"{prefix}_{slot_key}_add_opt", label_visibility="collapsed",
            disabled=is_locked,
        )

    if is_locked:
        setattr(cfg, slot_key, EquipSlot(tier=new_tier, grade="일반", enh=0, add_opt=0))
        st.markdown(
            "<div style='font-size:11px; color:#3a5068; margin-top:2px; margin-bottom:4px;'>"
            f"🔒 {new_tier} — Tier3부터 해금"
            "</div>",
            unsafe_allow_html=True,
        )
    else:
        setattr(cfg, slot_key, EquipSlot(tier=new_tier, grade=new_grade, enh=new_enh, add_opt=new_opt))
        tier_color = TIER_COLOR.get(new_tier, "#c0d4e8")
        grade_color = GRADE_COLOR.get(new_grade, "#c0d4e8")
        opt_text = f" · 옵션 {new_opt}단" if new_opt > 0 else ""
        st.markdown(
            "<div style='display:flex; gap:6px; align-items:center; font-size:11px; "
            "margin-top:2px; margin-bottom:4px;'>"
            f"<span style='color:{tier_color};'>● {new_tier}</span>"
            f"<span style='color:{grade_color};'>● {new_grade}</span>"
            f"<span style='color:var(--accent); font-weight:600;'>{opt_text}</span>"
            "</div>",
            unsafe_allow_html=True,
        )


def render_player_config(prefix: str, cfg: PlayerConfig) -> PlayerConfig:
    """플레이어 설정 패널 (아코디언)."""
    color = "#e8b84b" if "Player 1" in prefix else "#4b8ce8"
    icon = "⚔" if "Player 1" in prefix else "🛡"
    
    with st.expander(f"{icon} {prefix}", expanded=True):
        col_w, col_lv = st.columns([2, 1])
        with col_w:
            cfg.weapon_type = st.radio(
                "무기", WEAPON_TYPES, index=WEAPON_TYPES.index(cfg.weapon_type),
                horizontal=True, key=f"{prefix}_weapon_type",
            )
        with col_lv:
            cfg.level = st.number_input(
                "레벨", min_value=1, max_value=100, value=cfg.level,
                key=f"{prefix}_level",
            )

        fatk = player_final_atk(cfg)
        fdef = player_final_def(cfg)
        fhp  = player_hp(cfg)
        fmp  = player_mp(cfg)
        frmp = player_regen_mp(cfg)
        fspd = player_atk_speed(cfg)
        
        # 스탯 메트릭
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("ATK", fatk)
        m2.metric("DEF", fdef)
        m3.metric("HP", f"{fhp:,}")
        m4.metric("MP", f"{fmp:,}")
        m5.metric("SPD", f"{fspd:.2f}")
        st.caption(f"MP 회복 +{frmp} / 15s")

        tab_equip, tab_stats, tab_skills = st.tabs(["⚙ 장비", "📊 능력치", "✨ 스킬"])

        with tab_equip:
            st.info("💡 장비 티어별 추가 옵션(1~6단계)이 포함됩니다.")
            
            # ── 신규: 장비 일괄 설정 ───────────────────────────
            with st.expander("🛠️ 장비 일괄 설정 (Batch Set)", expanded=False):
                bc1, bc2, bc3, bc4 = st.columns(4)
                with bc1: b_tier = st.selectbox("일괄 티어", TIERS, index=2, key=f"{prefix}_batch_tier")
                with bc2: b_grade = st.selectbox("일괄 등급", GRADES, index=0, key=f"{prefix}_batch_grade")
                with bc3: b_enh = st.number_input("일괄 강화", 0, 10, 0, key=f"{prefix}_batch_enh")
                with bc4: b_opt = st.selectbox("일괄 옵션", range(7), format_func=lambda x: ["없음", "1단", "2단", "3단", "4단", "5단", "6단"][x], key=f"{prefix}_batch_opt")
                
                if st.button("모든 슬롯에 일괄 적용", key=f"{prefix}_batch_apply", use_container_width=True):
                    all_slots = ["weapon", "helmet", "chest", "gloves", "boots", "ring1", "ring2", "neck", "ear"]
                    for s_key in all_slots:
                        # 악세서리 티어 제약 체크 (T1, T2 잠금)
                        if s_key in _ACCESSORY_SLOTS and b_tier in _LOCKED_TIERS:
                            setattr(cfg, s_key, EquipSlot(tier=b_tier, grade="일반", enh=0, add_opt=0))
                        else:
                            # 등급 클램프 체크
                            max_g = TIER_MAX_GRADE[b_tier]
                            actual_g = b_grade if GRADE_ORDER[b_grade] <= GRADE_ORDER[max_g] else max_g
                            setattr(cfg, s_key, EquipSlot(tier=b_tier, grade=actual_g, enh=b_enh, add_opt=b_opt))
                    st.success("모든 장비 슬롯이 일괄 변경되었습니다! (아래에서 개별 수정 가능)")
                    st.rerun()

            st.divider()
            
            # ── 기존 개별 슬롯 설정 ───────────────────────────
            _eq_row("무기",   "weapon", cfg, prefix)
            _eq_row("투구",   "helmet", cfg, prefix)
            _eq_row("갑옷",   "chest",  cfg, prefix)
            _eq_row("장갑",   "gloves", cfg, prefix)
            _eq_row("신발",   "boots",  cfg, prefix)
            _eq_row("반지1",  "ring1",  cfg, prefix)
            _eq_row("반지2",  "ring2",  cfg, prefix)
            _eq_row("목걸이", "neck",   cfg, prefix)
            _eq_row("귀걸이", "ear",    cfg, prefix)
            
            base_atk = player_base_atk(cfg)
            base_def = player_base_def(cfg)
            ca, cb = st.columns(2)
            ca.metric("장비 순수 ATK", round(base_atk))
            cb.metric("장비 순수 DEF", round(base_def))

        with tab_stats:
            _render_stats_tab(cfg, prefix)

        with tab_skills:
            _render_skills_tab(cfg, prefix)

    return cfg


def _render_stats_tab(cfg: PlayerConfig, prefix: str) -> None:
    """능력치 보정 슬라이더."""
    c1, c2 = st.columns(2)
    with c1:
        cfg.atk_vary = st.slider("공격력%", 0.0, 50.0, cfg.atk_vary, 0.5, key=f"{prefix}_atk_vary")
        cfg.add_atk = st.slider("추가 공격력", 0.0, 300.0, cfg.add_atk, 1.0, key=f"{prefix}_add_atk")
        cfg.crit_chance = st.slider("치명타 확률%", 0.0, 80.0, cfg.crit_chance, 0.5, key=f"{prefix}_crit_chance")
        cfg.skill_accel = st.slider("스킬 가속", 0.0, 100.0, cfg.skill_accel, 0.5, key=f"{prefix}_skill_accel")
    with c2:
        cfg.def_vary = st.slider("방어력%", 0.0, 50.0, cfg.def_vary, 0.5, key=f"{prefix}_def_vary")
        cfg.add_def = st.slider("추가 방어력", 0.0, 600.0, cfg.add_def, 1.0, key=f"{prefix}_add_def")
        cfg.crit_dmg = st.slider("치명타 피해%", 0.0, 300.0, cfg.crit_dmg, 1.0, key=f"{prefix}_crit_dmg")
        cfg.atk_spd = st.slider("공격 속도%", 0.0, 300.0, cfg.atk_spd, 1.0, key=f"{prefix}_atk_spd")
    
    st.divider()
    c3, c4 = st.columns(2)
    with c3:
        cfg.dmg_up = st.slider("주는 피해↑%", 0.0, 100.0, cfg.dmg_up, 0.5, key=f"{prefix}_dmg_up")
        cfg.pve_dmg_up = st.slider("PVE 피해↑%", 0.0, 100.0, cfg.pve_dmg_up, 0.5, key=f"{prefix}_pve_dmg_up")
    with c4:
        cfg.dmg_down = st.slider("받는 피해↓%", 0.0, 50.0, cfg.dmg_down, 0.5, key=f"{prefix}_dmg_down")
        cfg.pve_dmg_down = st.slider("PVE 피해↓%", 0.0, 50.0, cfg.pve_dmg_down, 0.5, key=f"{prefix}_pve_dmg_down")


def _render_skills_tab(cfg: PlayerConfig, prefix: str) -> None:
    """스킬셋 선택 및 레벨 설정."""
    # 1. 스킬셋 선택
    available_sets = list(SKILLS.get(cfg.weapon_type, {}).keys())
    if not available_sets:
        st.warning("선택한 무기에 정의된 스킬셋이 없습니다.")
        return

    # 현재 선택된 스킬셋이 유효하지 않으면 첫 번째 것으로 초기화
    if cfg.skill_set_name not in available_sets:
        cfg.skill_set_name = available_sets[0]

    st.markdown("### ✨ 스킬셋 선택")
    cfg.skill_set_name = st.selectbox(
        "사용할 스킬셋", available_sets, 
        index=available_sets.index(cfg.skill_set_name),
        key=f"{prefix}_skill_set_select"
    )
    
    st.divider()

    # 2. 선택된 스킬셋의 스킬 리스트 표시
    skill_list = SKILLS[cfg.weapon_type][cfg.skill_set_name]
    for sk in skill_list:
        if sk["cmd"] == "평타": continue
        cmd = sk["cmd"]
        lv = cfg.skill_levels.get(cmd, 1)
        lv_idx = min(lv - 1, len(sk["levels"]) - 1)
        ld = sk["levels"][lv_idx]
        
        col_sk, col_lv_sk = st.columns([3, 1])
        with col_sk:
            st.markdown(
                f"<span style='color:{CMD_COLOR.get(cmd, '#ccc')}; font-weight:700;'>{cmd}</span> {sk['name']}<br>"
                f"<span style='font-size:11px; color:#607080;'>쿨 {ld['cd']}s · 계수 {ld['dmg']}%</span>",
                unsafe_allow_html=True
            )
        with col_lv_sk:
            new_lv = st.selectbox("Lv", [1,2,3,4,5], index=lv-1, key=f"{prefix}_sklv_{cmd}_{cfg.skill_set_name}", label_visibility="collapsed")
        cfg.skill_levels[cmd] = new_lv
