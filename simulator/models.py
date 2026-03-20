"""데이터 모델 (dataclass)"""
from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class EquipSlot:
    tier: str = "Tier3"
    grade: str = "일반"
    enh: int = 0
    add_opt: int = 0  # 추가 옵션 (0: 없음, 1~6: 해당 단계 수치 적용)


@dataclass
class PlayerConfig:
    weapon_type: str = "양손검"
    level: int = 30

    # 장비
    weapon: EquipSlot = field(default_factory=lambda: EquipSlot("Tier3", "일반", 0))
    helmet: EquipSlot = field(default_factory=lambda: EquipSlot("Tier3", "일반", 0))   # 투구
    chest:  EquipSlot = field(default_factory=lambda: EquipSlot("Tier3", "일반", 0))   # 갑옷
    gloves: EquipSlot = field(default_factory=lambda: EquipSlot("Tier3", "일반", 0))   # 장갑
    boots:  EquipSlot = field(default_factory=lambda: EquipSlot("Tier3", "일반", 0))   # 신발
    ring1: EquipSlot = field(default_factory=lambda: EquipSlot("Tier3", "일반", 0))   # 반지1
    ring2: EquipSlot = field(default_factory=lambda: EquipSlot("Tier3", "일반", 0))   # 반지2
    neck: EquipSlot = field(default_factory=lambda: EquipSlot("Tier3", "일반", 0))
    ear: EquipSlot = field(default_factory=lambda: EquipSlot("Tier3", "일반", 0))

    # 능력치 보정
    atk_vary: float = 0.0       # 공격력% (캡 50)
    add_atk: float = 0.0        # 추가 공격력 (캡 300)
    def_vary: float = 0.0       # 방어력% (캡 50)
    add_def: float = 0.0        # 추가 방어력 (캡 600)
    dmg_up: float = 0.0         # 주는 대미지↑ (캡 100)
    dmg_down: float = 0.0       # 받는 대미지↓ (캡 50)
    pve_dmg_up: float = 0.0     # PVE 대미지↑ (캡 100)
    pve_dmg_down: float = 0.0   # PVE 대미지↓ (캡 50)
    pvp_dmg_up: float = 0.0     # PVP 대미지↑ (캡 100)
    pvp_dmg_down: float = 0.0   # PVP 대미지↓ (캡 50)
    crit_chance: float = 20.0   # 치명타 확률 (캡 80)
    crit_dmg: float = 50.0      # 치명타 대미지↑ (캡 300)
    skill_accel: float = 0.0    # 스킬 가속 (캡 100)
    atk_spd: float = 0.0        # 공격 속도↑ (캡 300)

    # 스킬 설정
    skill_set_name: str = "3티어 기본셋"  # 선택된 스킬셋 이름
    skill_levels: dict[str, int] = field(
        default_factory=lambda: {"Q": 1, "W": 1, "E": 1, "R": 1}
    )


@dataclass
class MonsterConfig:
    tier: str = "Tier3"
    grade: str = "Normal"


@dataclass
class SimResult:
    avg_dps: float
    timeline: list[dict]   # [{"sec": t, "total_dmg": d, "dps": d}, ...]
    events: list[dict] = field(default_factory=list)  # 세부 히트 로그 [{"t", "cmd", "name", "dmg", "total_dmg"}]
    buff_dmg: float = 0.0  # 버프 기여분


@dataclass
class SoloBattleResult:
    """단독 PVE 전투 결과 (몬스터 반격 포함, 리스폰/부활 반복)"""
    events: list[dict]      # 시간순 이벤트 (player/monster 모두)
    kills: int              # 플레이어가 몬스터 처치한 횟수
    deaths: int             # 플레이어 사망 횟수
    total_player_dmg: int   # 플레이어가 준 총 피해
    total_mon_dmg: int      # 몬스터에게 받은 총 피해
    avg_dps: float          # 플레이어 DPS (60s 기준)
    mon_max_hp: float       # 몬스터 최대 HP
    mon_def: float          # 몬스터 방어력
    player_max_hp: int      # 플레이어 최대 HP
    buff_dmg: float = 0.0   # 버프 기여분
    
    # 경제/성장 데이터 추가
    total_xp: float = 0.0        # 획득한 총 경험치
    total_mastery: float = 0.0   # 획득한 총 숙련도
    est_drops: float = 0.0       # 예상 장비 재료 드랍 개수
    xp_to_next: float = 0.0      # 다음 레벨까지 남은 경험치 비율 (%)


@dataclass
class FarmGoal:
    """파밍 목표 설정"""
    target_items: int = 100      # 100개 획득 목표
    monster_tier: str = "Tier2"  # 몬스터 티어
    monster_grade: str = "Normal"
    player_level: int = 20

@dataclass
class PeriodSummary:
    """고정 시간 파밍 결과 요약 (기간 기반)"""
    sim_count: int
    sim_hours: float             # 시뮬레이션 기준 시간

    min_items: int = 0
    max_items: int = 0
    avg_items: float = 0.0
    p50_items: int = 0
    p5_items: int = 0            # 5th percentile — 운이 나빠도 이만큼은 획득

    avg_xp: float = 0.0
    avg_mastery: float = 0.0
    item_distribution: list[int] = field(default_factory=list)


@dataclass
class MonteCarloBucket:
    """확률 분포 구간"""
    range_label: str
    probability: float   # 0~100 %
    count: int = 0


@dataclass
class MonteCarloSummary:
    """N회 반복 시뮬레이션 결과 요약 (기간 기반 아이템 획득)"""
    sim_count: int               # 반복 횟수
    sim_hours: float = 0.0       # 시뮬레이션 기간 (시간)

    min_items: int = 0
    max_items: int = 0
    avg_items: float = 0.0
    p50_items: int = 0
    p95_items: int = 0           # 5th percentile — 운이 나빠도 이만큼은 획득

    avg_xp: float = 0.0
    avg_mastery: float = 0.0

    buckets: list = field(default_factory=list)          # list[MonteCarloBucket]
    item_distribution: list[int] = field(default_factory=list)

@dataclass
class PveResult:
    solo1: SoloBattleResult
    solo2: SoloBattleResult
    mon_hp: float
    mon_def: float
    ttk1: float   # seconds (inf if dps == 0)
    ttk2: float
    kills1: int   # kills in 60s
    kills2: int


@dataclass
class PvpResult:
    p1_sim: SimResult   # P1 attacking P2
    p2_sim: SimResult   # P2 attacking P1
    ttk1: float         # time for P1 to kill P2
    ttk2: float         # time for P2 to kill P1
    winner: str         # "P1", "P2", "무승부"
    hp_timeline: list[dict]   # [{"sec": t, "P1 HP": v, "P2 HP": v}, ...]
