"""시뮬레이션 엔진 (Updated with Skill Set Selection)"""
from __future__ import annotations
import heapq
import math
from .constants import SKILLS, CAPS, MP_REGEN_INTERVAL, MASTERY_XP_PER_MIN
from .models import PlayerConfig, MonsterConfig, SimResult, SoloBattleResult, PveResult, PvpResult
from .calc import (
    player_final_atk, player_final_def, player_hp, player_atk_speed,
    player_mp, player_regen_mp,
    effective_cd, single_hit_dmg, monster_stats,
    required_xp, monster_xp, drop_expectation,
)

MON_ATK_INTERVAL: float = 1.0


def get_skill_list(cfg: PlayerConfig) -> list[dict]:
    """사용자가 선택한 스킬셋을 반환."""
    w_type = cfg.weapon_type
    s_set = cfg.skill_set_name
    # 해당 무기에 해당 스킬셋이 없으면 기본셋 시도
    if w_type in SKILLS:
        return SKILLS[w_type].get(s_set, list(SKILLS[w_type].values())[0])
    return []


def run_sim(
    cfg: PlayerConfig,
    target_def: float,
    dmg_up: float,
    dmg_down: float,
    mode_up: float,
    mode_down: float,
) -> SimResult:
    atk = player_final_atk(cfg)
    base_spd = player_atk_speed(cfg)
    acc = cfg.skill_accel
    max_mp = float(player_mp(cfg))
    regen_mp = float(player_regen_mp(cfg))

    skill_list = get_skill_list(cfg)
    cooldowns: dict[str, float] = {s["cmd"]: 0.0 for s in skill_list if s["cmd"] != "평타"}
    auto = next((s for s in skill_list if s["cmd"] == "평타"), {"cmd": "평타", "name": "평타", "crit": True, "levels": [{"lv": 1, "cd": 0, "mp": 0, "dmg": 100}]})

    t, p_mp, last_regen_t = 0.0, max_mp, 0.0
    base_aa_dmg = single_hit_dmg(atk, target_def, dmg_up, dmg_down, mode_up, mode_down, 100.0, auto["crit"], cfg.crit_chance, cfg.crit_dmg)
    base_aa_dps = base_aa_dmg * base_spd
    
    total_dmg, actual_aa_dmg_total, skill_buff_dmg = 0.0, 0.0, 0.0
    timeline, events, active_buffs = [], [], []

    while t < 120.0:
        active_buffs = [b for b in active_buffs if t < b["expires"]]
        b_atk_p = sum(b["value"] for b in active_buffs if b["type"] == "atk_pct")
        b_spd_p = sum(b["value"] for b in active_buffs if b["type"] == "atk_speed")
        b_crit_p = sum(b["value"] for b in active_buffs if b["type"] == "crit_chance")
        b_crit_d = sum(b["value"] for b in active_buffs if b["type"] == "crit_dmg")
        b_dmg_up = sum(b["value"] for b in active_buffs if b["type"] == "dmg_up")

        c_atk, c_crit_p, c_crit_d, c_dmg_up = atk * (1.0 + b_atk_p / 100.0), cfg.crit_chance + b_crit_p, cfg.crit_dmg + b_crit_d, dmg_up + b_dmg_up
        effective_spd = base_spd * (1.0 + b_spd_p / 100.0)
        interval = 1.0 / effective_spd

        while t >= last_regen_t + MP_REGEN_INTERVAL:
            last_regen_t += MP_REGEN_INTERVAL
            p_mp = min(p_mp + regen_mp, max_mp)

        used = False
        for cmd in ["R", "W", "E", "Q"]:
            if cooldowns.get(cmd, 0) <= 0:
                sk = next((s for s in skill_list if s["cmd"] == cmd), None)
                if not sk: continue
                lv_idx = min(cfg.skill_levels.get(cmd, 1) - 1, len(sk["levels"]) - 1)
                ld = sk["levels"][lv_idx]
                if p_mp < ld["mp"]: continue
                
                dmg = single_hit_dmg(c_atk, target_def, c_dmg_up, dmg_down, mode_up, mode_down, ld["dmg"], sk["crit"], c_crit_p, c_crit_d)
                base_dmg_val = single_hit_dmg(atk, target_def, dmg_up, dmg_down, mode_up, mode_down, ld["dmg"], sk["crit"], cfg.crit_chance, cfg.crit_dmg)
                p_mp -= ld["mp"]; total_dmg += dmg; skill_buff_dmg += (dmg - base_dmg_val)
                events.append({"t": round(t, 2), "cmd": cmd, "name": sk["name"], "dmg": round(dmg), "total_dmg": round(total_dmg), "mp": round(p_mp)})
                
                if sk.get("buffs"):
                    for buf in sk["buffs"]: active_buffs.append({"type": buf["type"], "expires": t + buf["duration"][lv_idx], "value": buf["value"][lv_idx]})
                elif sk.get("buff"):
                    buf = sk["buff"]; active_buffs.append({"type": buf["type"], "expires": t + buf["duration"][lv_idx], "value": buf["value"][lv_idx]})
                cooldowns[cmd] = effective_cd(ld["cd"], acc); used = True; break

        if not used:
            enh_val = 0.0
            for i, b in enumerate(active_buffs):
                if b["type"] == "enhanced_attack": enh_val = b["value"]; active_buffs.pop(i); break
            auto_coeff = enh_val if enh_val > 0 else 100.0
            dmg = single_hit_dmg(c_atk, target_def, c_dmg_up, dmg_down, mode_up, mode_down, auto_coeff, auto["crit"], c_crit_p, c_crit_d)
            total_dmg += dmg; actual_aa_dmg_total += dmg
            events.append({"t": round(t, 2), "cmd": "강화평타" if enh_val > 0 else "평타", "name": auto["name"] if enh_val <= 0 else "강화 평타", "dmg": round(dmg), "total_dmg": round(total_dmg), "mp": round(p_mp)})

        t += interval
        for k in cooldowns: cooldowns[k] = max(0.0, cooldowns[k] - interval)
        if math.floor(t) > len(timeline): timeline.append({"sec": int(t), "total_dmg": round(total_dmg), "dps": round(total_dmg / t)})

    buff_contribution = (actual_aa_dmg_total - (base_aa_dps * t)) + skill_buff_dmg
    return SimResult(avg_dps=total_dmg/120.0, timeline=timeline, events=events, buff_dmg=max(0.0, buff_contribution))


def run_solo_pve_sim(cfg: PlayerConfig, monster: MonsterConfig) -> SoloBattleResult:
    mon = monster_stats(monster)
    mon_max_hp, mon_atk_val, mon_def_val = float(mon["hp"]), float(mon["atk"]), float(mon["def"])
    p_max_hp, p_max_mp, p_regen_mp = player_hp(cfg), float(player_mp(cfg)), float(player_regen_mp(cfg))
    p_def, p_atk, p_base_spd, acc = float(player_final_def(cfg)), float(player_final_atk(cfg)), player_atk_speed(cfg), cfg.skill_accel

    skill_list = get_skill_list(cfg)
    auto = next((s for s in skill_list if s["cmd"] == "평타"), {"cmd": "평타", "name": "평타", "crit": True, "levels": [{"lv": 1, "cd": 0, "mp": 0, "dmg": 100}]})
    base_aa_dmg = single_hit_dmg(p_atk, mon_def_val, cfg.dmg_up, 0.0, cfg.pve_dmg_up, 0.0, 100.0, auto["crit"], cfg.crit_chance, cfg.crit_dmg)
    base_aa_dps = base_aa_dmg * p_base_spd
    
    cooldown_expiry: dict[str, float] = {s["cmd"]: 0.0 for s in skill_list if s["cmd"] != "평타"}
    p_hp, p_mp, mon_hp = float(p_max_hp), p_max_mp, float(mon_max_hp)
    kills, deaths, total_p_dmg, total_m_dmg = 0, 0, 0, 0
    actual_aa_dmg_total, skill_buff_dmg = 0.0, 0.0
    
    events, active_buffs = [], []
    ctr, queue = 0, []
    heapq.heappush(queue, (0.0, ctr, "player")); ctr += 1
    heapq.heappush(queue, (MON_ATK_INTERVAL, ctr, "monster")); ctr += 1
    heapq.heappush(queue, (MP_REGEN_INTERVAL, ctr, "mp_regen")); ctr += 1

    while queue:
        t, _, actor = heapq.heappop(queue)
        if t >= 120.0: break

        if actor == "mp_regen":
            p_mp = min(p_mp + p_regen_mp, p_max_mp)
            heapq.heappush(queue, (t + MP_REGEN_INTERVAL, ctr, "mp_regen")); ctr += 1
        elif actor == "player":
            active_buffs = [b for b in active_buffs if t < b["expires"]]
            b_atk_p = sum(b["value"] for b in active_buffs if b["type"] == "atk_pct")
            b_spd_p = sum(b["value"] for b in active_buffs if b["type"] == "atk_speed")
            b_crit_p = sum(b["value"] for b in active_buffs if b["type"] == "crit_chance")
            b_crit_d = sum(b["value"] for b in active_buffs if b["type"] == "crit_dmg")
            b_dmg_up = sum(b["value"] for b in active_buffs if b["type"] == "dmg_up")

            c_atk, c_crit_p, c_crit_d, c_dmg_up = p_atk * (1.0 + b_atk_p / 100.0), cfg.crit_chance + b_crit_p, cfg.crit_dmg + b_crit_d, cfg.dmg_up + b_dmg_up
            p_interval = 1.0 / (p_base_spd * (1.0 + b_spd_p / 100.0))

            used = False
            for cmd in ["R", "W", "E", "Q"]:
                if cooldown_expiry.get(cmd, 0.0) <= t + 1e-9:
                    sk = next((s for s in skill_list if s["cmd"] == cmd), None)
                    if not sk: continue
                    lv_idx = min(cfg.skill_levels.get(cmd, 1) - 1, len(sk["levels"]) - 1)
                    ld = sk["levels"][lv_idx]
                    if p_mp < ld["mp"]: continue
                    
                    dmg = single_hit_dmg(c_atk, mon_def_val, c_dmg_up, 0.0, cfg.pve_dmg_up, 0.0, ld["dmg"], sk["crit"], c_crit_p, c_crit_d)
                    base_dmg = single_hit_dmg(p_atk, mon_def_val, cfg.dmg_up, 0.0, cfg.pve_dmg_up, 0.0, ld["dmg"], sk["crit"], cfg.crit_chance, cfg.crit_dmg)
                    p_mp -= ld["mp"]; mon_hp -= dmg; total_p_dmg += int(dmg); skill_buff_dmg += (dmg - base_dmg)
                    is_kill = mon_hp <= 0
                    if is_kill: kills += 1; mon_hp = mon_max_hp
                    events.append({"t": round(t, 2), "actor": "player", "cmd": cmd, "name": sk["name"], "dmg": round(dmg), "is_kill": is_kill, "player_died": False, "player_hp": round(p_hp), "mon_hp": round(max(0.0, mon_hp)), "player_kills": kills, "player_deaths": deaths, "player_mp": round(p_mp)})
                    
                    if sk.get("buffs"):
                        for buf in sk["buffs"]: active_buffs.append({"type": buf["type"], "expires": t + buf["duration"][lv_idx], "value": buf["value"][lv_idx]})
                    elif sk.get("buff"):
                        buf = sk["buff"]; active_buffs.append({"type": buf["type"], "expires": t + buf["duration"][lv_idx], "value": buf["value"][lv_idx]})
                    cooldown_expiry[cmd] = t + effective_cd(ld["cd"], acc); used = True; break

            if not used:
                enh_val = 0.0
                for i, b in enumerate(active_buffs):
                    if b["type"] == "enhanced_attack": enh_val = b["value"]; active_buffs.pop(i); break
                auto_coeff = enh_val if enh_val > 0 else 100.0
                dmg = single_hit_dmg(c_atk, mon_def_val, c_dmg_up, 0.0, cfg.pve_dmg_up, 0.0, auto_coeff, auto["crit"], c_crit_p, c_crit_d)
                base_dmg = single_hit_dmg(p_atk, mon_def_val, cfg.dmg_up, 0.0, cfg.pve_dmg_up, 0.0, 100.0, auto["crit"], cfg.crit_chance, cfg.crit_dmg)
                mon_hp -= dmg; total_p_dmg += int(dmg); actual_aa_dmg_total += dmg
                is_kill = mon_hp <= 0
                if is_kill: kills += 1; mon_hp = mon_max_hp
                events.append({"t": round(t, 2), "actor": "player", "cmd": "평타", "name": auto["name"] if auto_coeff == 100 else "강화 평타", "dmg": round(dmg), "is_kill": is_kill, "player_died": False, "player_hp": round(p_hp), "mon_hp": round(max(0.0, mon_hp)), "player_kills": kills, "player_deaths": deaths, "player_mp": round(p_mp)})
            heapq.heappush(queue, (t + p_interval, ctr, "player")); ctr += 1
        else:
            def_bonus = sum(b["value"] for b in active_buffs if b["type"] == "def_pct")
            dmg = single_hit_dmg(mon_atk_val, p_def * (1.0 + def_bonus / 100.0), 0.0, float(cfg.dmg_down), 0.0, float(cfg.pve_dmg_down), 100, False, 0.0, 0.0)
            p_hp -= dmg; total_m_dmg += int(dmg)
            if p_hp <= 0: deaths += 1; p_hp = float(p_max_hp)
            events.append({"t": round(t, 2), "actor": "monster", "cmd": "ATK", "name": "몬스터 공격", "dmg": round(dmg), "is_kill": False, "player_died": p_hp <= 0, "player_hp": round(p_hp), "mon_hp": round(max(0.0, mon_hp)), "player_kills": kills, "player_deaths": deaths, "player_mp": round(p_mp)})
            heapq.heappush(queue, (t + MON_ATK_INTERVAL, ctr, "monster")); ctr += 1

    final_t = min(t, 120.0)
    txp = kills * monster_xp(monster.tier, monster.grade)
    tmas = (final_t / 60.0) * MASTERY_XP_PER_MIN
    edrops = drop_expectation(kills, monster.tier)
    xptnext = (txp / required_xp(cfg.level)) * 100.0
    buff_contribution = (actual_aa_dmg_total - (base_aa_dps * final_t)) + skill_buff_dmg

    return SoloBattleResult(
        events=events, kills=kills, deaths=deaths, total_player_dmg=total_p_dmg, total_mon_dmg=total_m_dmg, 
        avg_dps=total_p_dmg/120.0, mon_max_hp=mon_max_hp, mon_def=mon_def_val, player_max_hp=p_max_hp, 
        buff_dmg=max(0.0, buff_contribution),
        total_xp=txp, total_mastery=tmas, est_drops=edrops, xp_to_next=xptnext
    )


def pve_compare(p1: PlayerConfig, p2: PlayerConfig, monster: MonsterConfig) -> PveResult:
    solo1, solo2 = run_solo_pve_sim(p1, monster), run_solo_pve_sim(p2, monster)
    ttk1 = round(solo1.mon_max_hp / solo1.avg_dps, 2) if solo1.avg_dps > 0 else float("inf")
    ttk2 = round(solo2.mon_max_hp / solo2.avg_dps, 2) if solo2.avg_dps > 0 else float("inf")
    return PveResult(solo1=solo1, solo2=solo2, mon_hp=solo1.mon_max_hp, mon_def=solo1.mon_def, ttk1=ttk1, ttk2=ttk2, kills1=solo1.kills, kills2=solo2.kills)


def pvp_battle(p1: PlayerConfig, p2: PlayerConfig) -> PvpResult:
    hp1, hp2, def1, def2 = player_hp(p1), player_hp(p2), player_final_def(p1), player_final_def(p2)
    sim1 = run_sim(p1, def2, p1.dmg_up, p2.dmg_down, p1.pvp_dmg_up, p2.pvp_dmg_down)
    sim2 = run_sim(p2, def1, p2.dmg_up, p1.dmg_down, p2.pvp_dmg_up, p1.pvp_dmg_down)
    ttk1 = round(hp2 / sim1.avg_dps, 2) if sim1.avg_dps > 0 else float("inf")
    ttk2 = round(hp1 / sim2.avg_dps, 2) if sim2.avg_dps > 0 else float("inf")
    hp_timeline = []
    for i in range(max(len(sim1.timeline), len(sim2.timeline))):
        e1 = sim1.timeline[i] if i < len(sim1.timeline) else sim1.timeline[-1]
        e2 = sim2.timeline[i] if i < len(sim2.timeline) else sim2.timeline[-1]
        hp_timeline.append({"sec": e1["sec"], "P1 HP": max(0, hp1 - e2["total_dmg"]), "P2 HP": max(0, hp2 - e1["total_dmg"])})
    return PvpResult(p1_sim=sim1, p2_sim=sim2, ttk1=ttk1, ttk2=ttk2, winner="P1" if ttk1 < ttk2 else ("P2" if ttk2 < ttk1 else "무승부"), hp_timeline=hp_timeline)
