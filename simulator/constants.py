"""모든 정적 데이터 (v2026-03-19 기획서 배포용 HTML 확정 수치 반영)"""
from __future__ import annotations
from typing import Final

# ── 레벨 및 성장 테이블 (HTML 기획서 앵커 기준) ───────────────────
# 기획서 기준: 10레벨(2h), 20레벨(6h), 30레벨(12h), 60레벨(330h), 100레벨(1200h)
LEVEL_TABLE: Final[list[dict]] = [
    {"level": i + 1, "max_hp": 1500 + i * 100, "max_mp": 360 + i * 20, "regen_hp": 5, "regen_mp": 3}
    for i in range(100)
]
MP_REGEN_INTERVAL: Final[float] = 15.0

# ── 경제 / 드랍 시스템 (HTML 확정안) ──────────────────────────────
# 전리품 드랍률 (동일 티어 15%, 하위 티어 2%)
DROP_RATE_SAME_TIER: Final[float] = 15.0 
DROP_RATE_LOWER_TIER: Final[float] = 2.0
DROP_RATE_BOSS_ITEM: Final[float] = 0.75 # 0.5~1.0% 평균

# 제작 요구량 (무기 1파츠 기준 - HTML 5-2 섹션)
# 전리품 수량 = 목표시간(분) x 3
CRAFT_SPOILS_REQ: Final[dict[str, int]] = {
    "Tier1": 0,
    "Tier2": 60,    # 20분 사냥
    "Tier3": 180,   # 1시간 사냥
    "Tier4": 900,   # 5시간 사냥
    "Tier5": 4500,  # 25시간 사냥
    "Tier6": 22500, # 125시간 사냥
    "Tier7": 112500,# 625시간 사냥
}

# 가공물 요구량 (무기 1파츠 기준 - HTML 5-2 섹션)
# 가공물 수량 = 목표시간 x 0.6
CRAFT_PROCESSED_REQ: Final[dict[str, int]] = {
    "Tier1": 3,
    "Tier2": 12,
    "Tier3": 36,
    "Tier4": 180,
    "Tier5": 900,
    "Tier6": 4500,
    "Tier7": 22500,
}

# 던전 코어 시스템 (HTML 6-1 섹션)
CRAFT_CORE_REQ: Final[dict[str, int]] = {
    "Tier2": 3, "Tier3": 15, "Tier4": 45, "Tier5": 150, "Tier6": 450, "Tier7": 1500
}
DUNGEON_CORE_PER_RUN: Final[int] = 5 # 평균 5개 (3~7개)
DUNGEON_TIME_PER_RUN: Final[float] = 0.25 # 15분

# ── 성장 밸런스 기준 (XP) ──────────────────────────────────────────
# 기준 사냥 효율: 분당 10마리 처치 기준
BASE_XP_PER_MIN: Final[float] = 500.0 # T1 Normal 필드 기준
MASTERY_XP_PER_MIN: Final[float] = 300.0 # 고정

# 숙련도 요구량 (HTML 2-2 섹션)
MASTERY_TIER_REQ: Final[dict[str, int]] = {
    "Tier1": 36000,   # 2h
    "Tier2": 72000,   # 4h
    "Tier3": 108000,  # 6h
    "Tier4": 324000,  # 18h
    "Tier5": 1080000, # 60h
    "Tier6": 1440000, # 80h
    "Tier7": 2880000, # 160h
}

# ── 티어 / 등급 (전투 스탯) ────────────────────────────────────────
TIERS: Final[list[str]] = ["Tier1", "Tier2", "Tier3", "Tier4", "Tier5", "Tier6", "Tier7"]
GRADES: Final[list[str]] = ["일반", "고급", "희귀", "고대", "영웅", "유일", "유물"]
GRADE_ORDER: Final[dict[str, int]] = {g: i for i, g in enumerate(GRADES)}
TIER_MAX_GRADE: Final[dict[str, str]] = {"Tier1": "고급", "Tier2": "희귀", "Tier3": "고대", "Tier4": "영웅", "Tier5": "유일", "Tier6": "유물", "Tier7": "유물"}

WPN_BASE: Final[dict] = {"Tier1": 60, "Tier2": 80, "Tier3": 120, "Tier4": 180, "Tier5": 260, "Tier6": 360, "Tier7": 480}
WPN_GRADE: Final[dict] = {"일반": 0, "고급": 20, "희귀": 40, "고대": 60, "영웅": 80, "유일": 100, "유물": 120}
WPN_ENH: Final[dict] = {"Tier1": 8, "Tier2": 10, "Tier3": 12, "Tier4": 14, "Tier5": 16, "Tier6": 18, "Tier7": 20}

ARM_BASE: Final[dict] = {"Tier1": 30, "Tier2": 40, "Tier3": 60, "Tier4": 90, "Tier5": 130, "Tier6": 180, "Tier7": 240}
ARM_GRADE: Final[dict] = {"일반": 0, "고급": 10, "희귀": 20, "고대": 30, "영웅": 40, "유일": 50, "유물": 55}
ARM_ENH: Final[dict] = {"Tier1": 4, "Tier2": 5, "Tier3": 6, "Tier4": 7, "Tier5": 8, "Tier6": 9, "Tier7": 10}

# ── 나머지 색상 및 설정 (유지) ─────────────────────────────────────
GRADE_COLOR: Final[dict[str, str]] = {"일반": "#8a9bb0", "고급": "#4be8a0", "희귀": "#4b8ce8", "고대": "#c89040", "영웅": "#a04be8", "유일": "#e84b4b", "유물": "#e8b84b"}
TIER_COLOR: Final[dict[str, str]] = {"Tier1": "#8a9bb0", "Tier2": "#4be8a0", "Tier3": "#4b8ce8", "Tier4": "#c89040", "Tier5": "#a04be8", "Tier6": "#e84b4b", "Tier7": "#e8b84b"}
CAPS: Final[dict[str, float]] = {"MaxHpVary": 12000, "MaxMpVary": 2500, "MaxHpVaryper": 50, "MaxMpVaryper": 50, "AttackVary": 1500, "DefenseVary": 3000, "AttackVaryper": 50, "DefenseVaryper": 50, "AtkSpeedVaryper": 300, "CriVaryper": 80, "SkillCooldownAccVary": 100, "CriDamageVaryper": 300, "AddAttackVary": 300, "AddDefenseVary": 600, "DamageUpVaryper": 100, "DamageDownVaryper": 50, "PVEDamageUpVaryper": 100, "PVEDamageDownVaryper": 50}
DEF_CONST: Final[float] = 500.0
WEAPON_TYPES: Final[list[str]] = ["양손검", "한손검", "활", "지팡이", "단검"]
SKILL_CMDS: Final[list[str]] = ["Q", "W", "E", "R"]
C: Final[dict[str, str]] = {"bg": "#060b14", "panel": "#0b1220", "border": "#162030", "bright": "#243550", "accent": "#e8b84b", "blue": "#4b8ce8", "green": "#4be8a0", "danger": "#e84b4b", "text": "#c8d8e8", "dim": "#7a9ab8", "muted": "#3a5068", "p1": "#e8b84b", "p2": "#4b8ce8"}
CMD_COLOR: Final[dict[str, str]] = {"평타": "#4a6070", "강화평타": "#e8e84b", "Q": "#4be8a0", "W": "#4b8ce8", "E": "#e84bb8", "R": "#e8b84b"}
WEAPON_ICON_KEY: Final[dict[str, str]] = {"양손검": "greatsword", "한손검": "onehandsword", "활": "bow", "지팡이": "staff", "단검": "dagger"}

# ── 스킬 정의 ────────────────────────────────────────────
SKILLS: Final[dict[str, dict[str, list[dict]]]] = {
    "양손검": {
        "1티어 세트": [{"cmd": "평타", "name": "평타", "crit": True, "levels": [{"lv": 1, "cd": 0, "mp": 0, "dmg": 100}]}, {"cmd": "Q", "name": "강타", "crit": True, "levels": [{"lv": 1, "cd": 0.1, "mp": 5, "dmg": 110}]}, {"cmd": "W", "name": "회전 베기", "crit": False, "levels": [{"lv": 1, "cd": 12.0, "mp": 15, "dmg": 280}]}, {"cmd": "E", "name": "내리치기", "crit": False, "levels": [{"lv": 1, "cd": 20.0, "mp": 20, "dmg": 330}]}, {"cmd": "R", "name": "용오름", "crit": False, "levels": [{"lv": 1, "cd": 45.0, "mp": 50, "dmg": 450}]}],
        "2티어 세트": [{"cmd": "평타", "name": "평타", "crit": True, "levels": [{"lv": 1, "cd": 0, "mp": 0, "dmg": 100}]}, {"cmd": "Q", "name": "몰아치기", "crit": True, "levels": [{"lv": 1, "cd": 8.0, "mp": 10, "dmg": 100}]}, {"cmd": "W", "name": "가르기", "crit": False, "levels": [{"lv": 1, "cd": 12.0, "mp": 20, "dmg": 250}]}, {"cmd": "E", "name": "충격파", "crit": False, "levels": [{"lv": 1, "cd": 20.0, "mp": 25, "dmg": 300}]}, {"cmd": "R", "name": "심판의 검", "crit": False, "levels": [{"lv": 1, "cd": 50.0, "mp": 60, "dmg": 400}]}],
        "3티어 세트": [{"cmd": "평타", "name": "평타", "crit": True, "levels": [{"lv": 1, "cd": 0, "mp": 0, "dmg": 100}]}, {"cmd": "Q", "name": "가벼운 손놀림", "crit": True, "levels": [{"lv": 1, "cd": 5.0, "mp": 15, "dmg": 200}]}, {"cmd": "W", "name": "대지 가르기", "crit": False, "levels": [{"lv": 1, "cd": 12.0, "mp": 30, "dmg": 250}]}, {"cmd": "E", "name": "휘몰이", "crit": False, "levels": [{"lv": 1, "cd": 15.0, "mp": 25, "dmg": 300}]}, {"cmd": "R", "name": "적진으로", "crit": False, "levels": [{"lv": 1, "cd": 40.0, "mp": 100, "dmg": 400}]}]
    },
    "한손검": {
        "1티어 세트": [{"cmd": "평타", "name": "평타", "crit": True, "levels": [{"lv": 1, "cd": 0, "mp": 0, "dmg": 100}]}, {"cmd": "Q", "name": "성스러운 일격", "crit": True, "levels": [{"lv": 1, "cd": 6.0, "mp": 5, "dmg": 130}]}, {"cmd": "W", "name": "가호", "crit": False, "levels": [{"lv": 1, "cd": 12.0, "mp": 10, "dmg": 160}]}, {"cmd": "E", "name": "반격", "crit": False, "levels": [{"lv": 1, "cd": 20.0, "mp": 15, "dmg": 200}]}, {"cmd": "R", "name": "정의의 심판", "crit": False, "levels": [{"lv": 1, "cd": 45.0, "mp": 40, "dmg": 350}]}],
        "2티어 세트": [{"cmd": "평타", "name": "평타", "crit": True, "levels": [{"lv": 1, "cd": 0, "mp": 0, "dmg": 100}]}, {"cmd": "Q", "name": "철벽의 반격", "crit": True, "levels": [{"lv": 1, "cd": 6.0, "mp": 8, "dmg": 140}]}, {"cmd": "W", "name": "광휘", "crit": False, "levels": [{"lv": 1, "cd": 15.0, "mp": 15, "dmg": 100}]}, {"cmd": "E", "name": "모두 쉿", "crit": False, "levels": [{"lv": 1, "cd": 25.0, "mp": 20, "dmg": 100}]}, {"cmd": "R", "name": "진공 폭발", "crit": False, "levels": [{"lv": 1, "cd": 50.0, "mp": 50, "dmg": 400}]}],
        "3티어 세트": [{"cmd": "평타", "name": "평타", "crit": True, "levels": [{"lv": 1, "cd": 0, "mp": 0, "dmg": 100}]}, {"cmd": "Q", "name": "신성한 일격", "crit": True, "levels": [{"lv": 1, "cd": 6.0, "mp": 10, "dmg": 150}]}, {"cmd": "W", "name": "가호의 빛", "crit": False, "levels": [{"lv": 1, "cd": 12.0, "mp": 20, "dmg": 100}]}, {"cmd": "E", "name": "폭주", "crit": False, "levels": [{"lv": 1, "cd": 18.0, "mp": 30, "dmg": 300}]}, {"cmd": "R", "name": "심판", "crit": False, "levels": [{"lv": 1, "cd": 45.0, "mp": 100, "dmg": 500}]}]
    },
    "활": {
        "1티어 세트": [{"cmd": "평타", "name": "평타", "crit": True, "levels": [{"lv": 1, "cd": 0, "mp": 0, "dmg": 100}]}, {"cmd": "Q", "name": "충격 사격", "crit": True, "levels": [{"lv": 1, "cd": 5.0, "mp": 5, "dmg": 180}]}, {"cmd": "W", "name": "연속 쏘기", "crit": False, "levels": [{"lv": 1, "cd": 12.0, "mp": 15, "dmg": 240}]}, {"cmd": "E", "name": "급습", "crit": False, "levels": [{"lv": 1, "cd": 20.0, "mp": 20, "dmg": 280}]}, {"cmd": "R", "name": "폭탄화살", "crit": False, "levels": [{"lv": 1, "cd": 50.0, "mp": 50, "dmg": 420}]}],
        "2티어 세트": [{"cmd": "평타", "name": "평타", "crit": True, "levels": [{"lv": 1, "cd": 0, "mp": 0, "dmg": 100}]}, {"cmd": "Q", "name": "섬광 화살", "crit": True, "levels": [{"lv": 1, "cd": 5.0, "mp": 10, "dmg": 200}]}, {"cmd": "W", "name": "연사", "crit": False, "levels": [{"lv": 1, "cd": 10.0, "mp": 20, "dmg": 260}]}, {"cmd": "E", "name": "바람의 상처", "crit": False, "levels": [{"lv": 1, "cd": 20.0, "mp": 25, "dmg": 100}]}, {"cmd": "R", "name": "저격", "crit": False, "levels": [{"lv": 1, "cd": 45.0, "mp": 80, "dmg": 480}]}],
        "3티어 세트": [{"cmd": "평타", "name": "평타", "crit": True, "levels": [{"lv": 1, "cd": 0, "mp": 0, "dmg": 100}]}, {"cmd": "Q", "name": "강화 사격", "crit": True, "levels": [{"lv": 1, "cd": 5.0, "mp": 15, "dmg": 220}]}, {"cmd": "W", "name": "멀티샷", "crit": False, "levels": [{"lv": 1, "cd": 12.0, "mp": 30, "dmg": 280}]}, {"cmd": "E", "name": "집중", "crit": False, "levels": [{"lv": 1, "cd": 20.0, "mp": 40, "dmg": 350}]}, {"cmd": "R", "name": "발묶음", "crit": False, "levels": [{"lv": 1, "cd": 45.0, "mp": 100, "dmg": 500}]}]
    },
    "지팡이": {
        "1티어 세트": [{"cmd": "평타", "name": "평타", "crit": True, "levels": [{"lv": 1, "cd": 0, "mp": 0, "dmg": 100}]}, {"cmd": "Q", "name": "불꽃 화살", "crit": False, "levels": [{"lv": 1, "cd": 8.0, "mp": 10, "dmg": 36}]}, {"cmd": "W", "name": "전기 충격", "crit": False, "levels": [{"lv": 1, "cd": 15.0, "mp": 20, "dmg": 200}]}, {"cmd": "E", "name": "얼음 송곳", "crit": False, "levels": [{"lv": 1, "cd": 20.0, "mp": 25, "dmg": 300}]}, {"cmd": "R", "name": "유성 낙하", "crit": False, "levels": [{"lv": 1, "cd": 50.0, "mp": 50, "dmg": 420}]}],
        "2티어 세트": [{"cmd": "평타", "name": "평타", "crit": True, "levels": [{"lv": 1, "cd": 0, "mp": 0, "dmg": 100}]}, {"cmd": "Q", "name": "불꽃 송곳", "crit": False, "levels": [{"lv": 1, "cd": 8.0, "mp": 12, "dmg": 20}]}, {"cmd": "W", "name": "얼음 화살", "crit": False, "levels": [{"lv": 1, "cd": 15.0, "mp": 25, "dmg": 150}]}, {"cmd": "E", "name": "번개", "crit": False, "levels": [{"lv": 1, "cd": 1.0, "mp": 30, "dmg": 100}]}, {"cmd": "R", "name": "눈보라", "crit": False, "levels": [{"lv": 1, "cd": 60.0, "mp": 60, "dmg": 100}]}],
        "3티어 세트": [{"cmd": "평타", "name": "평타", "crit": True, "levels": [{"lv": 1, "cd": 0, "mp": 0, "dmg": 100}]}, {"cmd": "Q", "name": "빙결", "crit": False, "levels": [{"lv": 1, "cd": 4.0, "mp": 20, "dmg": 200}]}, {"cmd": "W", "name": "다후타", "crit": False, "levels": [{"lv": 1, "cd": 15.0, "mp": 40, "dmg": 400}]}, {"cmd": "E", "name": "낙뢰", "crit": False, "levels": [{"lv": 1, "cd": 40.0, "mp": 50, "dmg": 600}]}, {"cmd": "R", "name": "방울", "crit": False, "levels": [{"lv": 1, "cd": 20.0, "mp": 100, "dmg": 300}]}]
    },
    "단검": {
        "1티어 세트": [{"cmd": "평타", "name": "평타", "crit": True, "levels": [{"lv": 1, "cd": 0, "mp": 0, "dmg": 100}]}, {"cmd": "Q", "name": "내리꽂기", "crit": True, "levels": [{"lv": 1, "cd": 5.0, "mp": 5, "dmg": 100}]}, {"cmd": "W", "name": "기습", "crit": False, "levels": [{"lv": 1, "cd": 0.1, "mp": 10, "dmg": 70}]}, {"cmd": "E", "name": "독 바르기", "crit": False, "levels": [{"lv": 1, "cd": 18.0, "mp": 15, "dmg": 180}]}, {"cmd": "R", "name": "분노", "crit": False, "levels": [{"lv": 1, "cd": 45.0, "mp": 40, "dmg": 60}]}],
        "2티어 세트": [{"cmd": "평타", "name": "평타", "crit": True, "levels": [{"lv": 1, "cd": 0, "mp": 0, "dmg": 100}]}, {"cmd": "Q", "name": "습격", "crit": True, "levels": [{"lv": 1, "cd": 6.0, "mp": 10, "dmg": 220}]}, {"cmd": "W", "name": "절단", "crit": False, "levels": [{"lv": 1, "cd": 10.0, "mp": 20, "dmg": 120}]}, {"cmd": "E", "name": "그림자 베기", "crit": False, "levels": [{"lv": 1, "cd": 15.0, "mp": 25, "dmg": 250}]}, {"cmd": "R", "name": "암살", "crit": False, "levels": [{"lv": 1, "cd": 40.0, "mp": 60, "dmg": 500}]}],
        "3티어 세트": [{"cmd": "평타", "name": "평타", "crit": True, "levels": [{"lv": 1, "cd": 0, "mp": 0, "dmg": 100}]}, {"cmd": "Q", "name": "추격", "crit": True, "levels": [{"lv": 1, "cd": 6.0, "mp": 15, "dmg": 220}]}, {"cmd": "W", "name": "침묵", "crit": False, "levels": [{"lv": 1, "cd": 13.0, "mp": 30, "dmg": 120}]}, {"cmd": "E", "name": "비수", "crit": False, "levels": [{"lv": 1, "cd": 15.0, "mp": 40, "dmg": 250}]}, {"cmd": "R", "name": "장막", "crit": False, "levels": [{"lv": 1, "cd": 40.0, "mp": 100, "dmg": 500}]}]
    },
}
