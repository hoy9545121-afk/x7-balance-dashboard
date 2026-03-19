"""순수 계산 함수 (Updated with HTML Spec V2026-03-19)"""
from __future__ import annotations
import math
from .constants import (
    GRADE_ORDER, TIER_MAX_GRADE,
    WPN_BASE, WPN_GRADE, WPN_ENH,
    ARM_BASE, ARM_GRADE, ARM_ENH,
    BASE_ATK_SPEED, DEF_CONST, CAPS,
    DROP_RATE_SAME_TIER, DROP_RATE_LOWER_TIER,
    BASE_XP_PER_MIN
)

# ── 경제 시스템 계산 (HTML 확정안 반영) ──────────────────────────────

def required_xp(level: int) -> float:
    """
    레벨별 필요 경험치 산출 (HTML 기획서 앵커 타임 기반 근사치).
    10Lv(2h), 20Lv(6h), 30Lv(12h), 60Lv(330h)
    """
    # 기본 공식: 베이스 4300에서 시작하되, 구간별 가중치 부여
    if level < 1: return 4300.0
    # HTML 기획서의 '누계 시간' 곡선을 따르도록 계수 조정 (1.065 기본 유지하되 레벨대별 보정)
    rate = 1.065
    if level > 40: rate = 1.08  # 40레벨 이후 급증 구간 반영
    if level > 60: rate = 1.10  # 후반부 엔드게임 구간
    return 4300.0 * (rate ** (level - 1))


def monster_xp_efficiency(player_level: int, monster_tier: str) -> float:
    """분당 획득 경험치 효율 (기본 500 XP/min)."""
    # 지역 레벨과 캐릭터 레벨 차이에 따른 효율 저하 등은 추후 구현 가능
    return BASE_XP_PER_MIN


def drop_rate_by_tier(player_tier: str, monster_tier: str) -> float:
    """티어 관계에 따른 드랍 확률 반환 (%)"""
    p_idx = int(player_tier.replace("Tier", ""))
    m_idx = int(monster_tier.replace("Tier", ""))
    
    if p_idx == m_idx:
        return DROP_RATE_SAME_TIER # 15%
    elif p_idx > m_idx:
        return DROP_RATE_LOWER_TIER # 2%
    else:
        return 0.0 # 상위 티어 드랍 없음 (기획 규칙)


# ── 장비 스탯 (기존 로직 유지) ──────────────────────────────

def player_final_atk(cfg: PlayerConfig) -> float:
    # 무기
    w = cfg.weapon
    base_atk = WPN_BASE.get(w.tier, 60)
    grade_atk = WPN_GRADE.get(w.grade, 0)
    enh_atk = WPN_ENH.get(w.tier, 8) * w.enh
    
    # 추가 옵션 (AddAttackVary)
    from .constants import ADD_OPT_WPN
    add_atk = ADD_OPT_WPN.get(w.tier, [0]*7)[w.add_opt]
    
    total = base_atk + grade_atk + enh_atk + add_atk + cfg.atk_fixed
    total *= (1 + cfg.atk_pct / 100.0)
    return min(total, CAPS["AttackVary"] * (1 + CAPS["AttackVaryper"]/100.0))

def player_final_def(cfg: PlayerConfig) -> float:
    slots = ["helmet", "chest", "gloves", "boots"]
    total_base = 0
    for s in slots:
        slot = getattr(cfg, s)
        total_base += ARM_BASE.get(slot.tier, 30)
        total_base += ARM_GRADE.get(slot.grade, 0)
        total_base += ARM_ENH.get(slot.tier, 4) * slot.enh
        from .constants import ADD_OPT_ARM
        total_base += ADD_OPT_ARM.get(slot.tier, [0]*7)[slot.add_opt]
    
    total = total_base + cfg.def_fixed
    total *= (1 + cfg.def_pct / 100.0)
    return min(total, CAPS["DefenseVary"] * (1 + CAPS["DefenseVaryper"]/100.0))

def player_hp(cfg: PlayerConfig) -> int:
    base = 1500 + (cfg.level - 1) * 100
    total = (base + cfg.hp_fixed) * (1 + cfg.hp_pct / 100.0)
    return int(min(total, CAPS["MaxHpVary"] * (1 + CAPS["MaxHpVaryper"]/100.0)))

def player_mp(cfg: PlayerConfig) -> int:
    base = 360 + (cfg.level - 1) * 20
    total = (base + cfg.mp_fixed) * (1 + cfg.mp_pct / 100.0)
    return int(min(total, CAPS["MaxMpVary"] * (1 + CAPS["MaxMpVaryper"]/100.0)))

def player_regen_mp(cfg: PlayerConfig) -> float:
    return 3.0 # MP_REGEN_INTERVAL(15s) 당 3 회복

def player_atk_speed(cfg: PlayerConfig) -> float:
    total_pct = min(cfg.atk_speed_pct, CAPS["AtkSpeedVaryper"])
    return BASE_ATK_SPEED * (1 + total_pct / 100.0)

def effective_cd(base_cd: float, accel: float) -> float:
    total_accel = min(accel, CAPS["SkillCooldownAccVary"])
    return base_cd * 100.0 / (100.0 + total_accel)

def single_hit_dmg(
    atk: float, target_def: float, 
    dmg_up: float, dmg_down: float,
    mode_up: float, mode_down: float,
    skill_coeff: float, is_crit_skill: bool,
    p_crit_chance: float, p_crit_dmg: float
) -> float:
    # 방어 감쇄
    def_mult = DEF_CONST / (target_def + DEF_CONST)
    
    # 데미지 증감
    total_dmg_mult = (1 + dmg_up / 100.0) * (1 - dmg_down / 100.0)
    total_mode_mult = (1 + mode_up / 100.0) * (1 - mode_down / 100.0)
    
    # 기초 데미지
    base_dmg = atk * (skill_coeff / 100.0) * def_mult * total_dmg_mult * total_mode_mult
    
    # 치명타 (스킬이 치명타 가능일 때만 적용)
    if is_crit_skill:
        eff_crit_p = min(p_crit_chance, CAPS["CriVaryper"]) / 100.0
        eff_crit_d = min(p_crit_dmg, CAPS["CriDamageVaryper"]) / 100.0
        # 기대값 방식: (1-p)*1 + p*d
        base_dmg *= (1.0 - eff_crit_p + eff_crit_p * eff_crit_d)
        
    return max(1.0, base_dmg)

def monster_stats(cfg: MonsterConfig) -> dict:
    from .constants import MON_BASE, MON_GRADE
    b = MON_BASE[cfg.tier]
    m = MON_GRADE[cfg.grade]
    return {
        "atk": round(b["atk"] * m["atk_mult"]),
        "def": round(b["def"] * m["def_mult"]),
        "hp":  round(b["hp"]  * m["hp_mult"]),
    }
