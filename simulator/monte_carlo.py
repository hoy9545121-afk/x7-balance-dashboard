"""몬테카를로 시뮬레이션 엔진 (제작 루트 확장)"""
import random
import statistics
import numpy as np
import math
from .engine import run_solo_pve_sim
from .models import PlayerConfig, MonsterConfig, MonteCarloSummary, MonteCarloBucket
from .constants import (
    DROP_RATE_WPN, MON_XP_BASE, MON_DIFF_XP_MULT, MASTERY_XP_PER_MIN,
    CRAFT_SPOILS_REQ, CRAFT_CORE_REQ, DUNGEON_CORE_PER_RUN, DUNGEON_TIME_PER_RUN
)

class MonteCarloEngine:
    """몬테카를로 파밍 시뮬레이션 엔진 (V4 - 필드/던전 루트 선택)"""
    
    @staticmethod
    def run_time_sim(cfg: PlayerConfig, monster: MonsterConfig, hours: float = 1.0, iterations: int = 1000, route: str = "필드(전리품)") -> MonteCarloSummary:
        """지정된 시간 동안의 파밍 결과를 시뮬레이션."""
        
        # 1. 공통 기초 성능 측정 (필드 효율 기준)
        battle = run_solo_pve_sim(cfg, monster)
        if battle.kills == 0 and route == "필드(전리품)":
            return MonteCarloSummary(sim_count=iterations, sim_hours=hours)
            
        item_results = []
        xp_total = 0.0
        mastery_total = (hours * 60.0) * MASTERY_XP_PER_MIN
        
        if route == "필드(전리품)":
            # [루트 A] 필드 드랍 방식
            kills_per_hour = (battle.kills / 2.0) * 60.0
            total_kills_in_period = int(kills_per_hour * hours)
            drop_rate = DROP_RATE_WPN.get(monster.tier, 0.0) / 100.0
            xp_per_kill = MON_XP_BASE.get(monster.tier, 10) * MON_DIFF_XP_MULT.get(monster.grade, 1.0)
            
            for _ in range(iterations):
                obtained = np.random.binomial(total_kills_in_period, drop_rate)
                item_results.append(int(obtained))
            xp_total = total_kills_in_period * xp_per_kill
            
        else:
            # [루트 B] 던전 코어 방식 (확률이 아닌 고정 보상 + 시간 소모)
            runs_per_hour = 1.0 / DUNGEON_TIME_PER_RUN # 시간당 약 4회
            total_runs = int(runs_per_hour * hours)
            cores_per_run = DUNGEON_CORE_PER_RUN.get(monster.tier, 5)
            
            # 던전은 고정 보상이므로 변동성이 적으나, 클리어 타임의 편차를 가정하여 10% 변동성 부여
            for _ in range(iterations):
                # 던전 클리어 성공률 95% 가정
                actual_runs = sum(1 for _ in range(total_runs) if random.random() < 0.95)
                item_results.append(actual_runs * cores_per_run)
            
            # 던전은 마리당 XP가 아닌 클리어 XP가 크므로 필드 대비 1.5배 보정
            xp_total = (battle.kills / 2.0 * 60.0 * hours) * 1.5 * MON_XP_BASE.get(monster.tier, 10)

        # 결과 집계 및 구간 생성
        item_results.sort()
        min_i, max_i = item_results[0], item_results[-1]
        range_size = max(1, math.ceil((max_i - min_i) / 5))
        
        buckets = []
        current_min = (min_i // range_size) * range_size
        while current_min <= max_i:
            current_max = current_min + range_size - 1
            label = f"{current_min}~{current_max}개" if range_size > 1 else f"{current_min}개"
            count = sum(1 for x in item_results if current_min <= x <= current_max)
            if count > 0:
                buckets.append(MonteCarloBucket(range_label=label, probability=(count / iterations) * 100.0, count=count))
            current_min += range_size

        return MonteCarloSummary(
            sim_count=iterations, sim_hours=hours, min_items=min_i, max_items=max_i,
            avg_items=statistics.mean(item_results), p50_items=int(statistics.median(item_results)),
            p95_items=int(np.percentile(item_results, 5)),
            avg_xp=xp_total, avg_mastery=mastery_total,
            buckets=buckets, item_distribution=item_results
        )
