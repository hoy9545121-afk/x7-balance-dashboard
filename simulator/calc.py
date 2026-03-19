"""순수 계산 함수 (사이드 이펙트 없음)"""
from __future__ import annotations
import math
from .constants import (
    GRADE_ORDER, TIER_MAX_GRADE,
    WPN_BASE, WPN_GRADE, WPN_ENH,
    ARM_BASE, ARM_GRADE, ARM_ENH,
    RING_BASE, RING_GRADE, RING_ENH,
    NECK_BASE, NECK_GRADE, NECK_ENH,
    EAR_BASE, EAR_GRADE, EAR_ENH,
    MON_BASE, MON_GRADE,
    BASE_ATK_SPEED, DEF_CONST, CAPS,
    LEVEL_TABLE, MP_REGEN_INTERVAL,
    ADD_OPT_WPN, ADD_OPT_ARM, ADD_OPT_RING,
)
from .models import EquipSlot, PlayerConfig, MonsterConfig


def clamp_grade(tier: str, grade: str) -> str:
    """티어 최대 등급을 초과하지 않도록 등급을 클램프."""
    max_grade = TIER_MAX_GRADE[tier]
    if GRADE_ORDER[grade] > GRADE_ORDER[max_grade]:
        return max_grade
    return grade


# ── 경제 시스템 계산 ─────────────────────────────────────

def required_xp(level: int) -> float:
    """해당 레벨에서 다음 레벨로 가기 위한 필요 경험치 (ECON_SPEC 1-1)."""
    if level < 1: return 4300.0
    from .constants import BASE_REQ_XP, XP_GROWTH_RATE
    return BASE_REQ_XP * (XP_GROWTH_RATE ** (level - 1))


def monster_xp(tier: str, grade: str) -> float:
    """몬스터 처치 시 획득 경험치 (ECON_SPEC 1-3, 1-4)."""
    from .constants import MON_XP_BASE, MON_DIFF_XP_MULT
    base = MON_XP_BASE.get(tier, 10)
    mult = MON_DIFF_XP_MULT.get(grade, 1.0)
    return base * mult


def drop_expectation(kills: int, tier: str) -> float:
    """처치 수에 따른 장비 재료 드랍 기대값 (ECON_SPEC 4-1)."""
    from .constants import DROP_RATE_WPN
    rate = DROP_RATE_WPN.get(tier, 0.0) / 100.0
    return kills * rate


# ── 장비 스탯 (추가 옵션 포함) ──────────────────────────────

def weapon_atk(slot: EquipSlot) -> float:
    g = clamp_grade(slot.tier, slot.grade)
    base = WPN_BASE[slot.tier] + WPN_GRADE[g] + WPN_ENH[slot.tier] * slot.enh
    if slot.add_opt > 0 and slot.tier in ADD_OPT_WPN:
        base += ADD_OPT_WPN[slot.tier][slot.add_opt - 1]
    return base


def armor_def(slot: EquipSlot) -> float:
    g = clamp_grade(slot.tier, slot.grade)
    base = ARM_BASE[slot.tier] + ARM_GRADE[g] + ARM_ENH[slot.tier] * slot.enh
    if slot.add_opt > 0 and slot.tier in ADD_OPT_ARM:
        base += ADD_OPT_ARM[slot.tier][slot.add_opt - 1]
    return base


def ring_atk(slot: EquipSlot) -> float:
    g = clamp_grade(slot.tier, slot.grade)
    base = RING_BASE[slot.tier] + RING_GRADE[g] + RING_ENH[slot.tier] * slot.enh
    if slot.add_opt > 0 and slot.tier in ADD_OPT_RING:
        base += ADD_OPT_RING[slot.tier][slot.add_opt - 1]
    return base


def neck_def(slot: EquipSlot) -> float:
    g = clamp_grade(slot.tier, slot.grade)
    base = NECK_BASE[slot.tier] + NECK_GRADE[g] + NECK_ENH[slot.tier] * slot.enh
    if slot.add_opt > 0 and slot.tier in ADD_OPT_ARM:
        base += ADD_OPT_ARM[slot.tier][slot.add_opt - 1]
    return base


def ear_def(slot: EquipSlot) -> float:
    g = clamp_grade(slot.tier, slot.grade)
    base = EAR_BASE[slot.tier] + EAR_GRADE[g] + EAR_ENH[slot.tier] * slot.enh
    if slot.add_opt > 0 and slot.tier in ADD_OPT_ARM:
        base += ADD_OPT_ARM[slot.tier][slot.add_opt - 1]
    return base


# ── 플레이어 기본 스탯 ────────────────────────────────────

def player_base_atk(cfg: PlayerConfig) -> float:
    return weapon_atk(cfg.weapon) + ring_atk(cfg.ring1) + ring_atk(cfg.ring2)


def player_base_def(cfg: PlayerConfig) -> float:
    return (
        armor_def(cfg.helmet) + armor_def(cfg.chest) +
        armor_def(cfg.gloves) + armor_def(cfg.boots) +
        neck_def(cfg.neck) + ear_def(cfg.ear)
    )


def player_final_atk(cfg: PlayerConfig) -> int:
    base = player_base_atk(cfg)
    vary = min(cfg.atk_vary, CAPS["AttackVaryper"])
    add  = min(cfg.add_atk,  CAPS["AddAttackVary"])
    return round(base * (1 + vary / 100) + add)


def player_final_def(cfg: PlayerConfig) -> int:
    base = player_base_def(cfg)
    vary = min(cfg.def_vary, CAPS["DefenseVaryper"])
    add  = min(cfg.add_def,  CAPS["AddDefenseVary"])
    return round(base * (1 + vary / 100) + add)


def player_hp(cfg: PlayerConfig) -> int:
    return LEVEL_TABLE[cfg.level - 1]["max_hp"]


def player_mp(cfg: PlayerConfig) -> int:
    return LEVEL_TABLE[cfg.level - 1]["max_mp"]


def player_regen_mp(cfg: PlayerConfig) -> int:
    """15초 틱당 MP 회복량 (RegenMpVary)."""
    return LEVEL_TABLE[cfg.level - 1]["regen_mp"]


def player_atk_speed(cfg: PlayerConfig) -> float:
    spd = min(cfg.atk_spd, CAPS["AtkSpeedVaryper"])
    return BASE_ATK_SPEED * (1 + spd / 100)


# ── 전투 계산 ────────────────────────────────────────────

def effective_cd(base_cd: float, skill_accel: float) -> float:
    """스킬 가속 적용 실질 쿨다운."""
    if base_cd == 0:
        return 0.0
    acc = min(skill_accel, CAPS["SkillCooldownAccVary"])
    return round(base_cd * 100 / (100 + acc) * 10) / 10


def single_hit_dmg(
    atk: float,
    def_: float,
    dmg_up: float,
    dmg_down: float,
    mode_up: float,
    mode_down: float,
    coeff: float,
    can_crit: bool,
    crit_chance: float,
    crit_dmg: float,
) -> int:
    """
    데미지 공식:
      ATK × (DEF_CONST / (DEF + DEF_CONST))
          × (1+dmgUp%) × (1−dmgDown%)
          × (1+modeUp%) × (1−modeDown%)
          × (coeff/100)
          × [critMult if can_crit]
    """
    def_mod = DEF_CONST / (def_ + DEF_CONST)
    d = atk * def_mod
    d *= (1 + min(dmg_up, CAPS["DamageUpVaryper"]) / 100)
    d *= (1 - min(dmg_down, CAPS["DamageDownVaryper"]) / 100)
    d *= (1 + min(mode_up, CAPS["PVEDamageUpVaryper"]) / 100)
    d *= (1 - min(mode_down, CAPS["PVEDamageDownVaryper"]) / 100)
    d *= coeff / 100
    if can_crit:
        crit_p = min(crit_chance, CAPS["CriVaryper"]) / 100
        crit_d = min(crit_dmg,   CAPS["CriDamageVaryper"]) / 100
        d *= (1 + crit_p * crit_d)
    return round(d)


def monster_stats(cfg: MonsterConfig) -> dict:
    b = MON_BASE[cfg.tier]
    m = MON_GRADE[cfg.grade]
    return {
        "atk": round(b["atk"] * m["atk_mult"]),
        "def": round(b["def"] * m["def_mult"]),
        "hp":  round(b["hp"]  * m["hp_mult"]),
    }
