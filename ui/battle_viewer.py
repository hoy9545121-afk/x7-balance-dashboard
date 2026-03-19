"""전투 비주얼 아레나 — 방치형 게임 스타일 (PVE / PVP 공통)"""
from __future__ import annotations

import dataclasses
import hashlib
import json
import time

import streamlit as st

from simulator.calc import player_hp
from simulator.constants import CMD_COLOR
from simulator.models import MonsterConfig, PlayerConfig, PveResult, PvpResult

# ── 이모지 매핑 ───────────────────────────────────────────
_PLAYER_EMOJI: dict[str, str] = {
    "양손검": "🗡️",
    "한손검": "🛡️",
    "활":   "🏹",
    "지팡이": "🔮",
    "단검":  "🔪",
}
_MONSTER_EMOJI: dict[str, str] = {
    "Normal":    "🐺",
    "Strong":    "🐗",
    "Commander": "🐉",
    "Elite":     "💀",
    "Hero":      "👹",
    "Boss":      "👺",
}
_SPEED_MAP: dict[str, float] = {"x1": 0.9, "x2": 0.45, "x5": 0.12, "x10": 0.04}

# ── CSS ───────────────────────────────────────────────────
_CSS = """
<style>
@keyframes dmg-float {
  0%   { opacity:1; transform:translateY(0)    scale(1.0); }
  55%  { opacity:1; transform:translateY(-45px) scale(1.2); }
  100% { opacity:0; transform:translateY(-80px) scale(0.7); }
}
@keyframes monster-hit {
  0%,100% { transform:translateX(0)  rotate(0deg); }
  20%     { transform:translateX(-16px) rotate(-7deg); }
  40%     { transform:translateX(16px)  rotate( 7deg); }
  60%     { transform:translateX(-9px)  rotate(-3deg); }
  80%     { transform:translateX( 9px)  rotate( 3deg); }
}
@keyframes p2-hit {
  0%,100% { transform:translateX(0); }
  25%     { transform:translateX(14px) rotate(5deg); }
  75%     { transform:translateX(-14px) rotate(-5deg); }
}
@keyframes player-swing {
  0%   { transform:translateX(0)   rotate(0deg); }
  35%  { transform:translateX(24px) rotate(-18deg); }
  100% { transform:translateX(0)   rotate(0deg); }
}
@keyframes p2-swing {
  0%   { transform:translateX(0)    rotate(0deg); }
  35%  { transform:translateX(-24px) rotate(18deg); }
  100% { transform:translateX(0)    rotate(0deg); }
}
@keyframes kill-flash {
  0%   { box-shadow: inset 0 0  0px  0px rgba(232,184,75,0.00); }
  25%  { box-shadow: inset 0 0 80px 30px rgba(232,184,75,0.40); }
  100% { box-shadow: inset 0 0  0px  0px rgba(232,184,75,0.00); }
}
@keyframes kill-rise {
  0%   { opacity:0; transform:translateY(10px)  scale(0.6); }
  20%  { opacity:1; transform:translateY(-18px) scale(1.5); }
  70%  { opacity:1; transform:translateY(-38px) scale(1.1); }
  100% { opacity:0; transform:translateY(-65px) scale(0.8); }
}
@keyframes spawn-pop {
  0%   { transform:scale(0.3) rotate(-20deg); opacity:0; }
  60%  { transform:scale(1.2) rotate(5deg);  opacity:1; }
  100% { transform:scale(1.0) rotate(0deg);  opacity:1; }
}
.battle-arena {
  background: linear-gradient(180deg,#050a14 0%,#081018 65%,#0c1525 100%);
  border:1px solid #1e3048; border-radius:14px;
  padding:20px 28px; display:flex; align-items:center;
  justify-content:space-between; min-height:210px;
  overflow:hidden; position:relative;
}
.arena-kill  { animation: kill-flash 0.9s ease; }
.arena-spawn { animation: none; }
.c-player  { font-size:68px; display:block; animation:player-swing 0.45s ease;
              filter:drop-shadow(0 0 14px #e8b84baa); }
.c-player2 { font-size:68px; display:block; animation:p2-swing 0.45s ease;
              filter:drop-shadow(0 0 14px #4b8ce8aa); }
.c-player-idle  { font-size:68px; display:block;
                  filter:drop-shadow(0 0 8px #e8b84b55); }
.c-player2-idle { font-size:68px; display:block;
                  filter:drop-shadow(0 0 8px #4b8ce855); }
.c-monster { font-size:88px; display:block; animation:monster-hit 0.45s ease;
              filter:drop-shadow(0 0 16px #e84b4baa); }
.c-monster-spawn { font-size:88px; display:block; animation:spawn-pop 0.5s ease;
                   filter:drop-shadow(0 0 20px #e84b4bcc); }
.c-monster-dead  { font-size:88px; display:block; opacity:0.25;
                   filter:grayscale(100%); }
.c-p2      { font-size:80px; display:block; animation:p2-swing 0.45s ease;
              filter:drop-shadow(0 0 14px #4b8ce8aa); }
.c-p1-def  { font-size:80px; display:block; animation:p2-hit 0.45s ease; }
.c-p2-def  { font-size:80px; display:block; animation:p2-hit 0.45s ease; }
.c-mon-def { font-size:88px; display:block; animation:monster-hit 0.45s ease; }
.action-center { flex:1; text-align:center; padding:0 16px; min-width:0; }
.skill-label { font-size:15px; font-weight:700; display:block; margin-bottom:6px; }
.dmg-number  { font-size:42px; font-weight:900; color:#e84b4b;
               text-shadow:0 0 28px #e84b4b99; display:block;
               animation:dmg-float 0.65s ease-out; letter-spacing:-1px; }
.kill-text   { font-size:32px; font-weight:900; color:#e8b84b;
               text-shadow:0 0 30px #e8b84bcc; display:block;
               animation:kill-rise 0.9s ease-out; }
.wave-info   { font-size:13px; font-weight:700; display:block;
               margin-bottom:4px; letter-spacing:0.05em; }
.time-badge  { font-size:11px; color:#354555; display:block; margin-top:6px; }
.char-lbl-p1  { font-size:10px; color:#e8b84b; margin-top:3px; font-weight:600; }
.char-lbl-p2  { font-size:10px; color:#4b8ce8; margin-top:3px; font-weight:600; }
.char-lbl-mon { font-size:10px; color:#e84b4b; margin-top:3px; font-weight:600; }
</style>
"""


# ── 헬퍼 ─────────────────────────────────────────────────

def _config_hash(*cfgs) -> str:
    data = "".join(json.dumps(dataclasses.asdict(c), sort_keys=True) for c in cfgs)
    return hashlib.md5(data.encode()).hexdigest()[:10]


def _hp_bar_html(label: str, current: float, maximum: float, base_color: str) -> str:
    pct = max(0, min(100, round(current / maximum * 100) if maximum > 0 else 0))
    bc = base_color if pct > 60 else ("#e8a030" if pct > 30 else "#e84b4b")
    return (
        f"<div style='flex:1; min-width:0; padding:0 8px;'>"
        f"<div style='font-size:11px; color:#7090b0; margin-bottom:3px;'>"
        f"{label} &nbsp;<span style='color:{bc}; font-weight:700;'>{pct}%</span></div>"
        f"<div style='background:#0d1a28; border-radius:4px; height:14px; overflow:hidden;"
        f"border:1px solid #1e3048; margin-bottom:3px;'>"
        f"<div style='width:{pct}%; background:linear-gradient(90deg,{bc},{bc}88);"
        f"height:100%;'></div></div>"
        f"<div style='font-size:10px; color:#3a5068;'>{int(current):,} / {int(maximum):,}</div>"
        f"</div>"
    )


def _skill_stats_html(
    events: list[dict],
    attacker_filter: str | None = None,
    label_color: str = "#e8b84b",
    label: str = "",
) -> str:
    """스킬별 피해 통계 HTML 블록. attacker_filter로 P1/P2 분리 가능."""
    from collections import defaultdict

    bucket: dict[str, dict] = defaultdict(lambda: {"name": "", "count": 0, "total": 0})
    for ev in events:
        if attacker_filter and ev.get("attacker") != attacker_filter:
            continue
        cmd = ev["cmd"]
        bucket[cmd]["name"] = ev["name"]
        bucket[cmd]["count"] += 1
        bucket[cmd]["total"] += ev["dmg"]

    if not bucket:
        return ""

    grand = sum(v["total"] for v in bucket.values())
    if grand == 0:
        return ""

    # 총 피해 내림차순 정렬
    rows_html = ""
    for cmd, s in sorted(bucket.items(), key=lambda x: x[1]["total"], reverse=True):
        pct = s["total"] / grand * 100
        avg = round(s["total"] / s["count"]) if s["count"] else 0
        c = CMD_COLOR.get(cmd, "#c0d4e8")
        bar_w = max(2, int(pct * 0.65))   # 최대 ~65px
        rows_html += (
            f"<tr style='border-bottom:1px solid #0d1520;'>"
            f"<td style='padding:4px 8px;'>"
            f"  <span style='color:{c}; font-weight:700; font-size:11px;"
            f"background:{c}18; border-radius:3px; padding:1px 5px;'>{cmd}</span>"
            f"  <span style='color:#c0d4e8; margin-left:4px;'>{s['name']}</span>"
            f"</td>"
            f"<td style='text-align:right; color:#7090b0; padding:4px 8px;'>{s['count']}회</td>"
            f"<td style='text-align:right; color:#e84b4b; font-weight:700; padding:4px 8px;'>"
            f"  {s['total']:,}"
            f"</td>"
            f"<td style='text-align:right; color:#607080; padding:4px 8px;'>{avg:,}</td>"
            f"<td style='padding:4px 8px;'>"
            f"  <div style='display:flex; align-items:center; gap:4px;'>"
            f"    <div style='width:{bar_w}px; height:7px; background:{c};"
            f"border-radius:2px; flex-shrink:0;'></div>"
            f"    <span style='color:{c}; font-size:10px;'>{pct:.1f}%</span>"
            f"  </div>"
            f"</td>"
            f"</tr>"
        )

    header = (
        f"<div style='color:{label_color}; font-weight:700; font-size:12px;"
        f"margin-bottom:5px; padding-left:2px;'>{label}</div>"
    ) if label else ""

    return (
        header
        + f"<div style='background:#050a10; border:1px solid #141e2a;"
        f"border-radius:8px; overflow:hidden; font-size:12px; font-family:monospace;'>"
        f"<table style='width:100%; border-collapse:collapse;'>"
        f"<thead><tr style='color:#354555; background:#080e18; font-size:10px;'>"
        f"<th style='text-align:left; padding:4px 8px;'>스킬</th>"
        f"<th style='text-align:right; padding:4px 8px;'>횟수</th>"
        f"<th style='text-align:right; padding:4px 8px;'>총 피해</th>"
        f"<th style='text-align:right; padding:4px 8px;'>평균</th>"
        f"<th style='padding:4px 8px;'>비중</th>"
        f"</tr></thead>"
        f"<tbody>{rows_html}</tbody>"
        f"<tfoot><tr style='background:#080e18; color:#607080;'>"
        f"<td colspan='2' style='padding:4px 8px;'>합계</td>"
        f"<td style='text-align:right; color:#e84b4b; font-weight:700; padding:4px 8px;'>"
        f"{grand:,}</td>"
        f"<td colspan='2' style='padding:4px 8px; color:#405060;'>"
        f"타격 {sum(v['count'] for v in bucket.values())}회</td>"
        f"</tr></tfoot>"
        f"</table></div>"
    )


def _log_html(events: list[dict], current_idx: int, n_show: int = 7) -> str:
    start = max(0, current_idx - n_show + 1)
    lines = []
    for i, ev in enumerate(events[start: current_idx + 1]):
        is_last = i == min(n_show, current_idx - start + 1) - 1
        c = CMD_COLOR.get(ev["cmd"], "#c0d4e8")
        actor = ev.get("actor", "player")
        # support both PVP ("attacker") and PVE ("side") event formats
        attacker = ev.get("attacker") or ev.get("side", "")
        if actor == "monster":
            a_color = "#e84b4b"
            attacker_lbl = "MON"
        elif attacker == "P1":
            a_color = "#e8b84b"
            attacker_lbl = "P1"
        else:
            a_color = "#4b8ce8"
            attacker_lbl = attacker
        attacker_str = (
            f"<span style='color:{a_color}; font-weight:700;'>[{attacker_lbl}]</span> "
            if attacker_lbl else ""
        )
        alpha = "ff" if is_last else "88"
        lines.append(
            f"<div style='color:#c8d8e8{alpha}; line-height:1.75;'>"
            f"<span style='color:#354555;'>[{ev['t']:4.1f}s]</span> "
            f"{attacker_str}"
            f"<span style='color:{c}; font-weight:700;'>{ev['name']}</span>"
            f"<span style='color:#354555;'>({ev['cmd']})</span>"
            f" → <span style='color:#e84b4b;'>💥 {ev['dmg']:,}</span>"
            f"</div>"
        )
    inner = "".join(lines) or "<span style='color:#354555;'>전투 로그 없음</span>"
    return (
        f"<div style='background:#050a10; border:1px solid #141e2a; border-radius:8px;"
        f"padding:10px 14px; font-family:monospace; font-size:12px; min-height:110px;"
        f"max-height:160px; overflow-y:auto;'>{inner}</div>"
    )


# ── PVE 이벤트 빌더 (독립 전투) ──────────────────────────

def _build_pve_timeline(result: PveResult) -> list[dict]:
    """P1 / P2 독립 이벤트를 시간순으로 합친다. 각 이벤트에 'side' 필드 추가."""
    p1_evs = [{"side": "P1", **e} for e in result.solo1.events]
    p2_evs = [{"side": "P2", **e} for e in result.solo2.events]
    return sorted(p1_evs + p2_evs, key=lambda e: e["t"])


def _get_side_state(events: list[dict], up_to: int, side: str) -> dict:
    """events[0..up_to] 중 해당 side의 마지막 상태를 반환."""
    state: dict = {
        "player_hp": None, "mon_hp": None,
        "player_kills": 0, "player_deaths": 0,
        "last_ev": None,
    }
    for i in range(up_to + 1):
        ev = events[i]
        if ev["side"] == side:
            state["player_hp"] = ev["player_hp"]
            state["mon_hp"] = ev["mon_hp"]
            state["player_kills"] = ev["player_kills"]
            state["player_deaths"] = ev["player_deaths"]
            state["last_ev"] = ev
    return state


# ── 솔로 아레나 HTML (플레이어 1명 vs 몬스터) ─────────────

def _arena_solo_html(
    player_emoji: str,
    mon_emoji: str,
    side: str,
    side_color: str,
    p_max_hp: float,
    mon_max_hp: float,
    state: dict,
    flip: bool,          # True → P2 배치 (몬스터 왼쪽, 플레이어 오른쪽)
) -> str:
    ev = state["last_ev"]
    p_hp = float(state["player_hp"]) if state["player_hp"] is not None else p_max_hp
    m_hp = float(state["mon_hp"]) if state["mon_hp"] is not None else mon_max_hp
    kills = state["player_kills"]
    deaths = state["player_deaths"]

    actor = ev.get("actor", "player") if ev else "player"
    is_kill = ev.get("is_kill", False) if ev else False
    player_died = ev.get("player_died", False) if ev else False

    # ── CSS 클래스 선택 ─────────────────────────────────
    idle_p = "c-player2-idle" if flip else "c-player-idle"
    swing_p = "c-player2" if flip else "c-player"
    hit_p   = "c-p2-def"  if flip else "c-p1-def"
    if player_died:
        p_cls = "c-monster-dead"
    elif actor == "player":
        p_cls = swing_p
    elif actor == "monster":
        p_cls = hit_p
    else:
        p_cls = idle_p

    if is_kill:
        m_cls = "c-monster-dead"
        arena_extra = "arena-kill"
    elif actor == "monster":
        m_cls = "c-mon-def"
        arena_extra = ""
    else:
        m_cls = "c-monster" if ev else idle_p
        arena_extra = ""

    # ── 중앙 정보 ───────────────────────────────────────
    if ev is None:
        center = "<span style='color:#354555; font-size:12px;'>대기중...</span>"
    elif is_kill:
        center = (
            f"<span class='kill-text'>💀 KILL #{kills}!</span>"
            f"<span class='time-badge'>[{ev['t']:.1f}s]</span>"
        )
    elif player_died:
        center = (
            f"<span style='font-size:16px; color:#e84b4b; font-weight:900; display:block;"
            f"animation:kill-rise 0.9s ease-out;'>💀 사망</span>"
            f"<span class='time-badge'>[{ev['t']:.1f}s]</span>"
        )
    else:
        skill_color = CMD_COLOR.get(ev["cmd"], "#c0d4e8")
        dmg_color   = "#6bb8e8" if actor == "monster" else "#e84b4b"
        icon        = "🛡" if actor == "monster" else "💥"
        center = (
            f"<span class='skill-label' style='color:{skill_color};'>{ev['name']}</span>"
            f"<span class='dmg-number' style='font-size:30px; color:{dmg_color};'>"
            f"{icon} {ev['dmg']:,}</span>"
            f"<span class='time-badge'>[{ev['t']:.1f}s]</span>"
        )

    # ── HP 바 ───────────────────────────────────────────
    p_pct = max(0, min(100, round(p_hp / p_max_hp * 100) if p_max_hp > 0 else 0))
    m_pct = max(0, min(100, round(m_hp / mon_max_hp * 100) if mon_max_hp > 0 else 0))
    p_bc  = "#4be8a0" if p_pct > 60 else ("#e8a030" if p_pct > 30 else "#e84b4b")
    m_bc  = "#4be8a0" if m_pct > 60 else ("#e8a030" if m_pct > 30 else "#e84b4b")
    hp_html = (
        f"<div style='margin-bottom:4px;'>"
        f"<div style='display:flex; justify-content:space-between; font-size:10px;"
        f"color:#7090b0; margin-bottom:2px;'>"
        f"<span style='color:{side_color}; font-weight:600;'>{side} HP</span>"
        f"<span style='color:{p_bc};'>{int(p_hp):,} / {int(p_max_hp):,}</span></div>"
        f"<div style='background:#0d1a28; border-radius:3px; height:7px; overflow:hidden;"
        f"border:1px solid #1e3048;'>"
        f"<div style='width:{p_pct}%; background:linear-gradient(90deg,{p_bc},{p_bc}88);"
        f"height:100%;'></div></div></div>"
        f"<div style='margin-bottom:8px;'>"
        f"<div style='display:flex; justify-content:space-between; font-size:10px;"
        f"color:#7090b0; margin-bottom:2px;'>"
        f"<span style='color:#e84b4b;'>👹 Monster HP</span>"
        f"<span style='color:{m_bc};'>{int(m_hp):,} / {int(mon_max_hp):,}</span></div>"
        f"<div style='background:#0d1a28; border-radius:3px; height:7px; overflow:hidden;"
        f"border:1px solid #1e3048;'>"
        f"<div style='width:{m_pct}%; background:linear-gradient(90deg,{m_bc},{m_bc}88);"
        f"height:100%;'></div></div></div>"
    )

    # ── 화살표 색상 ─────────────────────────────────────
    p_arr = CMD_COLOR.get(ev["cmd"], side_color) if (ev and actor == "player") else "#1e3048"
    m_arr = "#e84b4b" if (ev and actor == "monster") else "#1e3048"

    # ── 캐릭터 블록 ─────────────────────────────────────
    p_block = (
        f"<div style='text-align:center; min-width:72px;'>"
        f"<span class='{p_cls}'>{player_emoji}</span>"
        f"<div style='font-size:9px; color:{side_color}; font-weight:600; margin-top:2px;'>{side}</div>"
        f"<div style='font-size:9px; color:#607080;'>☠️ {deaths}사망</div></div>"
    )
    m_block = (
        f"<div style='text-align:center; min-width:72px;'>"
        f"<span class='{m_cls}'>{mon_emoji}</span>"
        f"<div style='font-size:9px; color:#e84b4b; margin-top:2px;'>👹 Monster</div>"
        f"<div style='font-size:9px; color:#e8b84b; font-weight:600;'>🏆 {kills}킬</div></div>"
    )
    center_block = f"<div style='flex:1; text-align:center; padding:0 6px;'>{center}</div>"

    if not flip:
        arr_r = f"<div style='font-size:16px; color:{p_arr}; padding:0 2px; font-weight:900;'>▶▶</div>"
        arr_l = f"<div style='font-size:16px; color:{m_arr}; padding:0 2px; font-weight:900;'>◀◀</div>"
        body = p_block + arr_r + center_block + arr_l + m_block
    else:
        arr_r = f"<div style='font-size:16px; color:{m_arr}; padding:0 2px; font-weight:900;'>▶▶</div>"
        arr_l = f"<div style='font-size:16px; color:{p_arr}; padding:0 2px; font-weight:900;'>◀◀</div>"
        body = m_block + arr_r + center_block + arr_l + p_block

    return (
        hp_html
        + f"<div class='battle-arena {arena_extra}'"
        f" style='min-height:155px; padding:12px 14px;'>"
        + body + f"</div>"
    )


# ── PVE 아레나 렌더러 (독립 전투) ─────────────────────────

def render_pve_battle_arena(
    result: PveResult,
    p1: PlayerConfig,
    p2: PlayerConfig,
    monster: MonsterConfig,
) -> None:
    """PVE 전투 비주얼 아레나 — P1 / P2 각자 독립 몬스터와 전투."""

    cfg_hash = _config_hash(p1, p2, monster)
    if st.session_state.get("pve_hash") != cfg_hash:
        st.session_state["pve_hash"] = cfg_hash
        st.session_state["pve_idx"] = 0
        st.session_state["pve_playing"] = True

    events = _build_pve_timeline(result)
    if not events:
        st.info("전투 이벤트가 없습니다.")
        return

    max_idx = len(events) - 1

    st.markdown(
        "<span style='color:#e8b84b; font-size:17px; font-weight:700;'>⚔ 전투 아레나</span>",
        unsafe_allow_html=True,
    )

    speed, playing, skip, reset = _render_controls("pve", max_idx)
    if reset:
        st.session_state["pve_idx"] = 0
        st.session_state["pve_playing"] = False
    if skip:
        st.session_state["pve_idx"] = max_idx
        st.session_state["pve_playing"] = False

    idx = min(st.session_state.get("pve_idx", 0), max_idx)

    p1_state = _get_side_state(events, idx, "P1")
    p2_state = _get_side_state(events, idx, "P2")

    p1_max_hp  = result.solo1.player_max_hp
    p2_max_hp  = result.solo2.player_max_hp
    mon_max_hp = result.solo1.mon_max_hp

    p1_emoji  = _PLAYER_EMOJI.get(p1.weapon_type, "⚔️")
    p2_emoji  = _PLAYER_EMOJI.get(p2.weapon_type, "⚔️")
    mon_emoji = _MONSTER_EMOJI.get(monster.grade, "👹")

    # ── CSS 한 번 주입 ────────────────────────────────────
    st.markdown(_CSS, unsafe_allow_html=True)

    # ── 2열 독립 아레나 ───────────────────────────────────
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            _arena_solo_html(
                p1_emoji, mon_emoji, "P1", "#e8b84b",
                p1_max_hp, mon_max_hp, p1_state, flip=False,
            ),
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            _arena_solo_html(
                p2_emoji, mon_emoji, "P2", "#4b8ce8",
                p2_max_hp, mon_max_hp, p2_state, flip=True,
            ),
            unsafe_allow_html=True,
        )

    # ── 진행 바 ──────────────────────────────────────────
    ev = events[idx]
    p1k = p1_state["player_kills"]
    p2k = p2_state["player_kills"]
    p1d = p1_state["player_deaths"]
    p2d = p2_state["player_deaths"]
    pct_done = idx / max_idx if max_idx > 0 else 1.0
    st.progress(
        pct_done,
        text=(
            f"⚔ {idx+1}/{max_idx+1}타 · {ev['t']:.1f}s"
            f"  |  P1 🏆{p1k}킬 ☠️{p1d}사  |  P2 🏆{p2k}킬 ☠️{p2d}사"
        ),
    )

    # ── 배틀 로그 ────────────────────────────────────────
    st.markdown(_log_html(events, idx), unsafe_allow_html=True)

    # ── 120초 종료 시 스킬 통계 ───────────────────────────
    if idx == max_idx:
        st.markdown(
            "<div style='color:#e8b84b; font-size:14px; font-weight:700;"
            "margin:14px 0 6px;'>📊 120초 전투 결과 통계</div>",
            unsafe_allow_html=True,
        )
        col_s1, col_s2 = st.columns(2)
        p1_atk = [e for e in events if e["side"] == "P1" and e.get("actor") == "player"]
        p2_atk = [e for e in events if e["side"] == "P2" and e.get("actor") == "player"]
        with col_s1:
            st.markdown(
                _skill_stats_html(p1_atk, label_color="#e8b84b", label="⚔ P1 공격"),
                unsafe_allow_html=True,
            )
        with col_s2:
            st.markdown(
                _skill_stats_html(p2_atk, label_color="#4b8ce8", label="🔮 P2 공격"),
                unsafe_allow_html=True,
            )

    # ── 자동 재생 ────────────────────────────────────────
    if st.session_state.get("pve_playing"):
        if idx < max_idx:
            time.sleep(_SPEED_MAP.get(speed, 0.45))
            st.session_state["pve_idx"] = idx + 1
            st.rerun()
        else:
            st.session_state["pve_playing"] = False


# ── PVP 아레나 ───────────────────────────────────────────

def _arena_pvp_html(
    attacker: str,
    p1_emoji: str, p2_emoji: str,
    p1_label: str, p2_label: str,
    skill_name: str, skill_color: str,
    damage: int, t: float,
) -> str:
    cls1 = "c-player" if attacker == "P1" else "c-p1-def"
    cls2 = "c-p2"     if attacker == "P2" else "c-p2-def"
    a_color = "#e8b84b" if attacker == "P1" else "#4b8ce8"
    return (
        _CSS
        + f"<div class='battle-arena'>"
        f"  <div style='text-align:center; min-width:120px;'>"
        f"    <span class='{cls1}'>{p1_emoji}</span>"
        f"    <div class='char-lbl-p1'>{p1_label}</div>"
        f"  </div>"
        f"  <div class='action-center'>"
        f"    <span class='skill-label' style='color:{skill_color};'>"
        f"    <span style='color:{a_color}; font-size:12px;'>{attacker}</span>"
        f"    ⚡ {skill_name}</span>"
        f"    <span class='dmg-number'>💥 {damage:,}</span>"
        f"    <span class='time-badge'>[{t:.1f}s]</span>"
        f"  </div>"
        f"  <div style='text-align:center; min-width:120px;'>"
        f"    <span class='{cls2}'>{p2_emoji}</span>"
        f"    <div class='char-lbl-p2'>{p2_label}</div>"
        f"  </div>"
        f"</div>"
    )


def _merge_pvp_events(result: PvpResult, hp1: int, hp2: int) -> list[dict]:
    """P1/P2 이벤트를 시간순으로 합치고 HP 추적. 어느 쪽 HP가 0이 되면 즉시 종료."""
    p1_evs = [{"attacker": "P1", **e} for e in result.p1_sim.events]
    p2_evs = [{"attacker": "P2", **e} for e in result.p2_sim.events]
    merged = sorted(p1_evs + p2_evs, key=lambda e: e["t"])

    out: list[dict] = []
    p1_dealt = 0
    p2_dealt = 0
    for ev in merged:
        if ev["attacker"] == "P1":
            p1_dealt = ev["total_dmg"]
        else:
            p2_dealt = ev["total_dmg"]
        ev["p1_hp"] = max(0, hp1 - p2_dealt)
        ev["p2_hp"] = max(0, hp2 - p1_dealt)
        ev["battle_over"] = (ev["p1_hp"] == 0 or ev["p2_hp"] == 0)
        out.append(ev)
        if ev["battle_over"]:
            break  # 첫 번째 사망 이후는 재생하지 않음
    return out


def _render_controls(key_prefix: str, max_idx: int) -> tuple[str, bool, bool, bool]:
    c_play, c_speed, c_skip, c_reset = st.columns([1, 4, 1, 1])
    with c_play:
        playing = st.session_state.get(f"{key_prefix}_playing", False)
        idx = st.session_state.get(f"{key_prefix}_idx", 0)
        if st.button("⏸" if playing else "▶", key=f"{key_prefix}_play_btn",
                     use_container_width=True):
            if playing:
                st.session_state[f"{key_prefix}_playing"] = False
                playing = False
            else:
                if idx >= max_idx:
                    st.session_state[f"{key_prefix}_idx"] = 0
                st.session_state[f"{key_prefix}_playing"] = True
                playing = True
    with c_speed:
        speed = st.radio(
            "속도", ["x1", "x2", "x5", "x10"],
            index=1, horizontal=True,
            key=f"{key_prefix}_speed",
            label_visibility="collapsed",
        )
    with c_skip:
        skip = st.button("⏭", key=f"{key_prefix}_skip",
                         use_container_width=True, help="마지막 프레임으로")
    with c_reset:
        reset = st.button("↺", key=f"{key_prefix}_reset",
                          use_container_width=True, help="처음부터 다시")
    return speed, playing, skip, reset


def render_pvp_battle_arena(
    result: PvpResult,
    p1: PlayerConfig,
    p2: PlayerConfig,
) -> None:
    hp1 = player_hp(p1)
    hp2 = player_hp(p2)

    cfg_hash = _config_hash(p1, p2)
    if st.session_state.get("pvp_hash") != cfg_hash:
        st.session_state["pvp_hash"] = cfg_hash
        st.session_state["pvp_idx"] = 0
        st.session_state["pvp_playing"] = True

    events = _merge_pvp_events(result, hp1, hp2)
    if not events:
        st.info("전투 이벤트가 없습니다.")
        return

    max_idx = len(events) - 1

    winner_color = {"P1": "#e8b84b", "P2": "#4b8ce8", "무승부": "#7a9ab8"}[result.winner]
    winner_label = {"P1": "⚔ P1 승리!", "P2": "🛡 P2 승리!", "무승부": "⚖ 무승부"}[result.winner]
    st.markdown(
        f"<div style='text-align:center; border:1px solid {winner_color}44;"
        f"border-radius:8px; padding:6px; margin-bottom:10px;"
        f"background:{winner_color}11;'>"
        f"<span style='color:{winner_color}; font-size:16px; font-weight:700;'>{winner_label}</span>"
        f"</div>",
        unsafe_allow_html=True,
    )

    speed, playing, skip, reset = _render_controls("pvp", max_idx)
    if skip:
        st.session_state["pvp_idx"] = max_idx
        st.session_state["pvp_playing"] = False
    if reset:
        st.session_state["pvp_idx"] = 0
        st.session_state["pvp_playing"] = False

    idx = min(st.session_state.get("pvp_idx", 0), max_idx)
    ev = events[idx]
    attacker = ev["attacker"]
    skill_color = CMD_COLOR.get(ev["cmd"], "#c0d4e8")
    p1_emoji = _PLAYER_EMOJI.get(p1.weapon_type, "⚔️")
    p2_emoji = _PLAYER_EMOJI.get(p2.weapon_type, "⚔️")
    p1_hp_now = ev.get("p1_hp", hp1)
    p2_hp_now = ev.get("p2_hp", hp2)
    battle_over = ev.get("battle_over", False)

    # ── HP 바 ─────────────────────────────────────────────
    hp_html = (
        "<div style='display:flex; align-items:center; margin-bottom:10px;'>"
        + _hp_bar_html(f"⚔ P1 Lv{p1.level}", p1_hp_now, hp1, "#e8b84b")
        + "<div style='font-size:14px; color:#1e3048; font-weight:700; padding:0 6px;'>VS</div>"
        + _hp_bar_html(f"🛡 P2 Lv{p2.level}", p2_hp_now, hp2, "#4b8ce8")
        + "</div>"
    )
    st.markdown(hp_html, unsafe_allow_html=True)

    # ── 아레나 (사망 시 특별 연출) ──────────────────────────
    if battle_over:
        dead = "P1" if p1_hp_now == 0 else "P2"
        winner = "P2" if dead == "P1" else "P1"
        w_color = "#4b8ce8" if winner == "P2" else "#e8b84b"
        d_color = "#e84b4b"
        # 사망 아레나
        p1_cls = "c-monster-dead" if dead == "P1" else "c-player-idle"
        p2_cls = "c-monster-dead" if dead == "P2" else "c-player2-idle"
        death_html = (
            _CSS
            + f"<div class='battle-arena arena-kill'>"
            f"  <div style='text-align:center; min-width:110px;'>"
            f"    <span class='{p1_cls}'>{p1_emoji}</span>"
            f"    <div class='char-lbl-p1'>P1</div>"
            f"  </div>"
            f"  <div class='action-center'>"
            f"    <span style='font-size:36px; font-weight:900; color:{w_color};"
            f"text-shadow:0 0 30px {w_color}cc; display:block;"
            f"animation:kill-rise 0.9s ease-out;'>🏆 {winner} 승리!</span>"
            f"    <span style='font-size:14px; color:{d_color}; display:block;"
            f"margin-top:6px;'>💀 {dead} 사망 [{ev['t']:.1f}s]</span>"
            f"  </div>"
            f"  <div style='text-align:center; min-width:110px;'>"
            f"    <span class='{p2_cls}'>{p2_emoji}</span>"
            f"    <div class='char-lbl-p2'>P2</div>"
            f"  </div>"
            f"</div>"
        )
        st.markdown(death_html, unsafe_allow_html=True)
        st.session_state["pvp_playing"] = False
    else:
        st.markdown(
            _arena_pvp_html(
                attacker,
                p1_emoji, p2_emoji,
                f"P1 · {p1.weapon_type}", f"P2 · {p2.weapon_type}",
                ev["name"], skill_color,
                ev["dmg"], ev["t"],
            ),
            unsafe_allow_html=True,
        )

    pct_done = idx / max_idx if max_idx > 0 else 1.0
    st.progress(pct_done, text=f"{idx + 1} / {max_idx + 1} 타 · {ev['t']:.1f}s")
    st.markdown(_log_html(events, idx), unsafe_allow_html=True)

    # ── 전투 종료 시 스킬 통계 ────────────────────────────
    if battle_over:
        st.markdown(
            "<div style='color:#e8b84b; font-size:14px; font-weight:700;"
            "margin:14px 0 6px;'>📊 전투 결과 통계</div>",
            unsafe_allow_html=True,
        )
        used_events = events[: idx + 1]
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown(
                _skill_stats_html(
                    used_events,
                    attacker_filter="P1",
                    label_color="#e8b84b",
                    label="⚔ P1 공격",
                ),
                unsafe_allow_html=True,
            )
        with col_s2:
            st.markdown(
                _skill_stats_html(
                    used_events,
                    attacker_filter="P2",
                    label_color="#4b8ce8",
                    label="🛡 P2 공격",
                ),
                unsafe_allow_html=True,
            )

    if st.session_state.get("pvp_playing") and not battle_over:
        if idx < max_idx:
            time.sleep(_SPEED_MAP.get(speed, 0.45))
            st.session_state["pvp_idx"] = idx + 1
            st.rerun()
        else:
            st.session_state["pvp_playing"] = False
