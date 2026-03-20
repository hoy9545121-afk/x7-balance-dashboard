"""순수 계산 함수 (MD Source of Truth 기반 복구)"""
from __future__ import annotations
import math
from .constants import (
    GRADE_ORDER, TIER_MAX_GRADE,
    WPN_BASE, WPN_GRADE, WPN_ENH,
    ARM_BASE, ARM_GRADE, ARM_ENH,
    RING_BASE, RING_GRADE, RING_ENH,
    NECK_BASE, NECK_GRADE, NECK_ENH,
    EAR_BASE, EAR_GRADE, EAR_ENH,
    BASE_ATK_SPEED, DEF_CONST, CAPS,
    MON_XP_BASE, MON_DIFF_XP_MULT, DROP_RATE_WPN,
    BASE_REQ_XP, XP_GROWTH_RATE
)

# ── 1. 경제 시스템 계산 ──────────────────────────────

def required_xp(level: int) -> float:
    """해당 레벨에서 다음 레벨로 가기 위한 필요 경험치 (ECON_SPEC 1-1)."""
    if level < 1: return BASE_REQ_XP
    return BASE_REQ_XP * (XP_GROWTH_RATE ** (level - 1))


def monster_xp(tier: str, grade: str) -> float:
    """몬스터 처치 시 획득 경험치 (ECON_SPEC 1-3)."""
    base = MON_XP_BASE.get(tier, 10)
    mult = MON_DIFF_XP_MULT.get(grade, 1.0)
    return base * mult


def drop_expectation(kills: int, tier: str) -> float:
    """처치 수에 따른 장비 재료 드랍 기대값 (ECON_SPEC 4-1)."""
    rate = DROP_RATE_WPN.get(tier, 0.0) / 100.0
    return kills * rate


# ── 2. 장비 스탯 계산 ──────────────────────────────

def player_final_atk(cfg: PlayerConfig) -> float:
    # 무기 + 반지1 + 반지2
    w = cfg.weapon
    r1 = cfg.ring1
    r2 = cfg.ring2
    
    # 무기 스탯
    w_base = WPN_BASE.get(w.tier, 60)
    w_grade = WPN_GRADE.get(w.grade, 0)
    w_enh = WPN_ENH.get(w.tier, 8) * w.enh
    
    # 반지 스탯 (T3 이상만 존재)
    r1_base = RING_BASE.get(r1.tier, 0)
    r1_grade = RING_GRADE.get(r1.grade, 0)
    r1_enh = RING_ENH.get(r1.tier, 4) * r1.enh
    
    r2_base = RING_BASE.get(r2.tier, 0)
    r2_grade = RING_GRADE.get(r2.grade, 0)
    r2_enh = RING_ENH.get(r2.tier, 4) * r2.enh
    
    base_atk_sum = w_base + w_grade + w_enh + r1_base + r1_grade + r1_enh + r2_base + r2_grade + r2_enh
    
    # 추가 옵션 (IAO)
    from .constants import ADD_OPT_WPN, ADD_OPT_RING
    ao_w = ADD_OPT_WPN.get(w.tier, [0]*7)[w.add_opt]
    ao_r1 = ADD_OPT_RING.get(r1.tier, [0]*7)[r1.add_opt]
    ao_r2 = ADD_OPT_RING.get(r2.tier, [0]*7)[r2.add_opt]
    
    base_total = base_atk_sum + ao_w + ao_r1 + ao_r2
    vary_pct = min(cfg.atk_vary, CAPS["AttackVaryper"])
    total = round(base_total * (1 + vary_pct / 100.0) + min(cfg.add_atk, CAPS["AddAttackVary"]))
    return min(total, CAPS["AttackVary"] * (1 + CAPS["AttackVaryper"]/100.0))


def player_final_def(cfg: PlayerConfig) -> float:
    # 투구 + 갑옷 + 장갑 + 신발 + 목걸이 + 귀걸이
    slots = ["helmet", "chest", "gloves", "boots"]
    total_base = 0
    for s in slots:
        slot = getattr(cfg, s)
        total_base += ARM_BASE.get(slot.tier, 30)
        total_base += ARM_GRADE.get(slot.grade, 0)
        total_base += ARM_ENH.get(slot.tier, 4) * slot.enh
        from .constants import ADD_OPT_ARM
        total_base += ADD_OPT_ARM.get(slot.tier, [0]*7)[slot.add_opt]
        
    # 장신구 DEF
    n = cfg.neck
    e = cfg.ear
    total_base += (NECK_BASE.get(n.tier, 0) + NECK_GRADE.get(n.grade, 0) + NECK_ENH.get(n.tier, 4) * n.enh)
    total_base += (EAR_BASE.get(e.tier, 0) + EAR_GRADE.get(e.grade, 0) + EAR_ENH.get(e.tier, 4) * e.enh)
    
    # 장신구 추가옵션
    from .constants import ADD_OPT_ARM
    total_base += ADD_OPT_ARM.get(n.tier, [0]*7)[n.add_opt]
    total_base += ADD_OPT_ARM.get(e.tier, [0]*7)[e.add_opt]
    
    vary_pct = min(cfg.def_vary, CAPS["DefenseVaryper"])
    total = round(total_base * (1 + vary_pct / 100.0) + min(cfg.add_def, CAPS["AddDefenseVary"]))
    return min(total, CAPS["DefenseVary"] * (1 + CAPS["DefenseVaryper"]/100.0))


def player_hp(cfg: PlayerConfig) -> int:
    return int(1500 + (cfg.level - 1) * 100)


def player_mp(cfg: PlayerConfig) -> int:
    return int(360 + (cfg.level - 1) * 20)


def player_regen_mp(cfg: PlayerConfig) -> float:
    return 3.0 # MP_REGEN_INTERVAL(15s) 당 3 회복


def player_atk_speed(cfg: PlayerConfig) -> float:
    total_pct = min(cfg.atk_spd, CAPS["AtkSpeedVaryper"])
    return BASE_ATK_SPEED * (1 + total_pct / 100.0)


def effective_cd(base_cd: float, accel: float) -> float:
    total_accel = min(accel, CAPS["SkillCooldownAccVary"])
    return round(base_cd * 100.0 / (100.0 + total_accel) * 10) / 10


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
    
    # 치명타 (기대값 방식)
    if is_crit_skill:
        eff_crit_p = min(p_crit_chance, CAPS["CriVaryper"]) / 100.0
        eff_crit_d = min(p_crit_dmg, CAPS["CriDamageVaryper"]) / 100.0
        base_dmg *= (1.0 - eff_crit_p + eff_crit_p * (1.0 + eff_crit_d))
        
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
