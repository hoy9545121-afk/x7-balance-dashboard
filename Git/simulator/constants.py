"""모든 정적 데이터 (MD Source of Truth 기반 복구 - T2 8.333% 적용)"""
from __future__ import annotations
from typing import Final

# ── 1. 캐릭터 성장 (ECON_SPEC 1) ──────────────────────────
BASE_REQ_XP: Final[float] = 4300.0
XP_GROWTH_RATE: Final[float] = 1.065

LEVEL_TABLE: Final[list[dict]] = [
    {"level": i + 1, "max_hp": 1500 + i * 100, "max_mp": 360 + i * 20, "regen_hp": 5, "regen_mp": 3}
    for i in range(100)
]
MP_REGEN_INTERVAL: Final[float] = 15.0

# ── 2. 장비 스탯 (GAME_SPEC 1-2) ──────────────────────────
TIERS: Final[list[str]] = ["Tier1", "Tier2", "Tier3", "Tier4", "Tier5", "Tier6", "Tier7"]
GRADES: Final[list[str]] = ["일반", "고급", "희귀", "고대", "영웅", "유일", "유물"]
GRADE_ORDER: Final[dict[str, int]] = {g: i for i, g in enumerate(GRADES)}
TIER_MAX_GRADE: Final[dict[str, str]] = {"Tier1": "고급", "Tier2": "희귀", "Tier3": "고대", "Tier4": "영웅", "Tier5": "유일", "Tier6": "유물", "Tier7": "유물"}

WPN_BASE: Final[dict] = {"Tier1": 60, "Tier2": 80, "Tier3": 120, "Tier4": 180, "Tier5": 260, "Tier6": 360, "Tier7": 480}
WPN_GRADE: Final[dict] = {"일반": 0, "고급": 20, "희귀": 40, "고대": 60, "영웅": 80, "유일": 100, "유물": 120}
WPN_ENH: Final[dict] = {"Tier1": 8, "Tier2": 10, "Tier3": 12, "Tier4": 14, "Tier5": 16, "Tier6": 18, "Tier7": 20}

ARM_BASE: Final[dict] = {"Tier1": 30, "Tier2": 40, "Tier3": 60, "Tier4": 90, "Tier5": 130, "Tier6": 180, "Tier7": 240}
ARM_GRADE: Final[dict] = {"일반": 0, "고급": 10, "희귀": 20, "고대": 30, "영웅": 40, "유일": 50, "유물": 60}
ARM_ENH: Final[dict] = {"Tier1": 4, "Tier2": 5, "Tier3": 6, "Tier4": 7, "Tier5": 8, "Tier6": 9, "Tier7": 10}

RING_BASE: Final[dict] = {"Tier1": 0, "Tier2": 0, "Tier3": 30, "Tier4": 45, "Tier5": 65, "Tier6": 90, "Tier7": 120}
RING_GRADE: Final[dict] = {"일반": 0, "고급": 5, "희귀": 10, "고대": 15, "영웅": 20, "유일": 25, "유물": 30}
RING_ENH: Final[dict] = {"Tier1": 4, "Tier2": 5, "Tier3": 6, "Tier4": 7, "Tier5": 8, "Tier6": 9, "Tier7": 10}

NECK_BASE: Final[dict] = {"Tier1": 0, "Tier2": 0, "Tier3": 60, "Tier4": 90, "Tier5": 130, "Tier6": 180, "Tier7": 240}
NECK_GRADE: Final[dict] = {"일반": 0, "고급": 10, "희귀": 20, "고대": 30, "영웅": 40, "유일": 50, "유물": 60}
NECK_ENH: Final[dict] = {"Tier1": 4, "Tier2": 5, "Tier3": 6, "Tier4": 7, "Tier5": 8, "Tier6": 9, "Tier7": 10}

EAR_BASE: Final[dict] = {"Tier1": 0, "Tier2": 0, "Tier3": 60, "Tier4": 90, "Tier5": 130, "Tier6": 180, "Tier7": 240}
EAR_GRADE: Final[dict] = {"일반": 0, "고급": 10, "희귀": 20, "고대": 30, "영웅": 40, "유일": 50, "유물": 60}
EAR_ENH: Final[dict] = {"Tier1": 4, "Tier2": 5, "Tier3": 6, "Tier4": 7, "Tier5": 8, "Tier6": 9, "Tier7": 10}

# ── 3. 몬스터 데이터 (GAME_SPEC 5) ──────────────────────────
MON_BASE: Final[dict] = {
    "Tier1": {"atk":  30, "def":  12, "hp":   418},
    "Tier2": {"atk":  46, "def":  33, "hp":   539},
    "Tier3": {"atk": 118, "def":  61, "hp":  1147},
    "Tier4": {"atk": 178, "def":  80, "hp":  1666},
    "Tier5": {"atk": 268, "def": 110, "hp":  2289},
    "Tier6": {"atk": 364, "def": 140, "hp":  3020},
    "Tier7": {"atk": 486, "def": 177, "hp":  3807},
}
MON_GRADE: Final[dict] = {
    "Normal": {"atk_mult": 1.0, "def_mult": 1.0, "hp_mult": 1.0},
    "Strong": {"atk_mult": 1.1, "def_mult": 1.1, "hp_mult": 1.2},
    "Commander": {"atk_mult": 1.2, "def_mult": 1.2, "hp_mult": 1.5},
    "Elite": {"atk_mult": 1.3, "def_mult": 1.3, "hp_mult": 2.0},
    "Hero": {"atk_mult": 1.5, "def_mult": 1.5, "hp_mult": 5.0},
    "Boss": {"atk_mult": 2.0, "def_mult": 2.0, "hp_mult": 15.0},
}
MON_GRADES_LIST: Final[list[str]] = ["Normal", "Strong", "Commander", "Elite", "Hero", "Boss"]

# ── 4. 경제 및 드랍 (ECON_SPEC 2-1, 4-1, 5-2) ───────────────
MON_XP_BASE: Final[dict[str, int]] = {"Tier1": 10, "Tier2": 15, "Tier3": 22, "Tier4": 33, "Tier5": 49, "Tier6": 73, "Tier7": 109}
MON_DIFF_XP_MULT: Final[dict[str, float]] = {"Normal": 1.0, "Strong": 1.25, "Commander": 1.5, "Elite": 2.5, "Hero": 4.0, "Boss": 8.0}
MASTERY_XP_PER_MIN: Final[float] = 300.0

DROP_RATE_WPN: Final[dict[str, float]] = {
    "Tier1": 0.0, "Tier2": 8.333, "Tier3": 3.333, "Tier4": 1.00,
    "Tier5": 0.33, "Tier6": 0.13, "Tier7": 0.053,
}
DROP_RATE_BOSS_ITEM: Final[float] = 0.75

CRAFT_SPOILS_REQ: Final[dict[str, int]] = {"Tier2": 60, "Tier3": 180, "Tier4": 900}
CRAFT_CORE_REQ: Final[dict[str, int]] = {"Tier2": 3, "Tier3": 15, "Tier4": 45, "Tier5": 150, "Tier6": 450, "Tier7": 1500}
DUNGEON_CORE_PER_RUN: Final[dict[str, int]] = {"Tier2": 3, "Tier3": 5, "Tier4": 5, "Tier5": 5, "Tier6": 5, "Tier7": 5}
DUNGEON_TIME_PER_RUN: Final[float] = 0.25 # 15분

# ── 5. 스킬 정의 (GAME_SPEC 3-2 / 4-1) ──────────────────────
SKILLS: Final[dict[str, dict[str, list[dict]]]] = {
    "양손검": {
        "3티어 기본셋": [
            {"cmd": "평타", "name": "평타", "crit": True, "levels": [{"lv": 1, "cd": 0, "mp": 0, "dmg": 100}]},
            {"cmd": "Q", "name": "가벼운 손놀림", "crit": True, "levels": [{"lv": 1, "cd": 5.0, "mp": 15, "dmg": 200}]},
            {"cmd": "W", "name": "대지 가르기", "crit": False, "levels": [{"lv": 1, "cd": 12.0, "mp": 30, "dmg": 250}]},
            {"cmd": "E", "name": "휘몰이", "crit": False, "levels": [{"lv": 1, "cd": 15.0, "mp": 25, "dmg": 300}]},
            {"cmd": "R", "name": "적진으로", "crit": False, "levels": [{"lv": 1, "cd": 40.0, "mp": 100, "dmg": 400}]},
        ],
    },
    "한손검": {
        "3티어 기본셋": [
            {"cmd": "평타", "name": "평타", "crit": True, "levels": [{"lv": 1, "cd": 0, "mp": 0, "dmg": 100}]},
            {"cmd": "Q", "name": "성스러운 일격", "crit": True, "levels": [{"lv": 1, "cd": 6.0, "mp": 10, "dmg": 150}]},
            {"cmd": "W", "name": "가호의 빛", "crit": False, "levels": [{"lv": 1, "cd": 12.0, "mp": 20, "dmg": 200}]},
            {"cmd": "E", "name": "폭주하는 광휘", "crit": False, "levels": [{"lv": 1, "cd": 20.0, "mp": 30, "dmg": 250}]},
            {"cmd": "R", "name": "광휘의 심판", "crit": False, "levels": [{"lv": 1, "cd": 45.0, "mp": 100, "dmg": 500}]},
        ],
    },
    "활": {
        "1티어 폭탄화살셋": [
            {"cmd": "평타", "name": "평타", "crit": True, "levels": [{"lv": 1, "cd": 0, "mp": 0, "dmg": 100}]},
            {"cmd": "R", "name": "폭탄화살(1T)", "crit": False, "levels": [{"lv": 1, "cd": 45.0, "mp": 100, "dmg": 500}]},
        ],
        "3티어 기본셋": [
            {"cmd": "평타", "name": "평타", "crit": True, "levels": [{"lv": 1, "cd": 0, "mp": 0, "dmg": 100}]},
            {"cmd": "Q", "name": "충격 사격", "crit": True, "levels": [{"lv": 1, "cd": 5.0, "mp": 10, "dmg": 220}]},
            {"cmd": "W", "name": "연속 쏘기", "crit": False, "levels": [{"lv": 1, "cd": 12.0, "mp": 20, "dmg": 280}]},
            {"cmd": "E", "name": "급습", "crit": False, "levels": [{"lv": 1, "cd": 20.0, "mp": 35, "dmg": 350}]},
            {"cmd": "R", "name": "발묶음", "crit": False, "levels": [{"lv": 1, "cd": 45.0, "mp": 70, "dmg": 500}]},
        ],
    },
    "지팡이": {
        "3티어 기본셋": [
            {"cmd": "평타", "name": "평타", "crit": True, "levels": [{"lv": 1, "cd": 0, "mp": 0, "dmg": 100}]},
            {"cmd": "Q", "name": "얼음 화살", "crit": False, "levels": [{"lv": 1, "cd": 5.0, "mp": 18, "dmg": 200}]},
            {"cmd": "W", "name": "다후타의 손짓", "crit": False, "levels": [{"lv": 1, "cd": 15.0, "mp": 25, "dmg": 400}]},
            {"cmd": "E", "name": "심판의 낙뢰", "crit": False, "levels": [{"lv": 1, "cd": 40.0, "mp": 32, "dmg": 600}]},
            {"cmd": "R", "name": "방울방울", "crit": False, "levels": [{"lv": 1, "cd": 20.0, "mp": 45, "dmg": 300}]},
        ],
    },
    "단검": {
        "3티어 기본셋": [
            {"cmd": "평타", "name": "평타", "crit": True, "levels": [{"lv": 1, "cd": 0, "mp": 0, "dmg": 100}]},
            {"cmd": "Q", "name": "추격자의 발톱", "crit": True, "levels": [{"lv": 1, "cd": 6.0, "mp": 12, "dmg": 220}]},
            {"cmd": "W", "name": "침묵의 일격", "crit": False, "levels": [{"lv": 1, "cd": 13.0, "mp": 18, "dmg": 120}]},
            {"cmd": "E", "name": "사방의 비수", "crit": False, "levels": [{"lv": 1, "cd": 15.0, "mp": 25, "dmg": 250}]},
            {"cmd": "R", "name": "유혈의 장막", "crit": False, "levels": [{"lv": 1, "cd": 40.0, "mp": 70, "dmg": 500}]},
        ],
    },
}

# ── 6. 기타 상한 및 상수 (GAME_SPEC 1-3) ───────────────────
CAPS: Final[dict[str, float]] = {
    "MaxHpVary": 12000, "MaxMpVary": 2500, "MaxHpVaryper": 50, "MaxMpVaryper": 50,
    "AttackVary": 1500, "DefenseVary": 3000, "AttackVaryper": 50, "DefenseVaryper": 50,
    "AtkSpeedVaryper": 300, "CriVaryper": 80, "SkillCooldownAccVary": 100, "CriDamageVaryper": 300,
    "AddAttackVary": 300, "AddDefenseVary": 600, "DamageUpVaryper": 100, "DamageDownVaryper": 50,
    "PVEDamageUpVaryper": 100, "PVEDamageDownVaryper": 50,
}

ADD_OPT_WPN: Final[dict[str, list[int]]] = {"Tier1": [3, 3, 4, 4, 5, 6], "Tier2": [4, 4, 5, 6, 7, 8], "Tier3": [6, 7, 8, 9, 10, 12]}
ADD_OPT_ARM: Final[dict[str, list[int]]] = {"Tier1": [1, 1, 2, 2, 2, 3], "Tier2": [2, 2, 2, 3, 3, 4], "Tier3": [3, 3, 4, 4, 5, 6]}
ADD_OPT_RING: Final[dict[str, list[int]]] = {"Tier3": [1, 1, 2, 2, 2, 3]}

BASE_ATK_SPEED: Final[float] = 0.91
DEF_CONST: Final[float] = 500.0
WEAPON_TYPES: Final[list[str]] = ["양손검", "한손검", "활", "지팡이", "단검"]
SKILL_CMDS: Final[list[str]] = ["Q", "W", "E", "R"]
C: Final[dict[str, str]] = {"bg": "#060b14", "panel": "#0b1220", "border": "#162030", "bright": "#243550", "accent": "#e8b84b", "blue": "#4b8ce8", "green": "#4be8a0", "danger": "#e84b4b", "text": "#c8d8e8", "dim": "#7a9ab8", "muted": "#3a5068", "p1": "#e8b84b", "p2": "#4b8ce8"}
CMD_COLOR: Final[dict[str, str]] = {"평타": "#4a6070", "강화평타": "#e8e84b", "Q": "#4be8a0", "W": "#4b8ce8", "E": "#e84bb8", "R": "#e8b84b"}
GRADE_COLOR: Final[dict[str, str]] = {"일반": "#8a9bb0", "고급": "#4be8a0", "희귀": "#4b8ce8", "고대": "#c89040", "영웅": "#a04be8", "유일": "#e84b4b", "유물": "#e8b84b"}
TIER_COLOR: Final[dict[str, str]] = {"Tier1": "#8a9bb0", "Tier2": "#4be8a0", "Tier3": "#4b8ce8", "Tier4": "#c89040", "Tier5": "#a04be8", "Tier6": "#e84b4b", "Tier7": "#e8b84b"}
WEAPON_ICON_KEY: Final[dict[str, str]] = {"양손검": "greatsword", "한손검": "onehandsword", "활": "bow", "지팡이": "staff", "단검": "dagger"}
