"""X7 스킨 UI — 클로젯 메인 렌더러"""
from __future__ import annotations
import base64

import streamlit as st

from data.items import (
    CATEGORIES, CAT_LABEL, CAT_SLOT,
    GRADE_COLOR, GRADE_LABEL_KO,
    Item, Chroma,
    none_item,
)
from data.compositor import (
    composite_preview, preview_to_bytes,
    load_icon_bytes, assets_available, PIL_OK, ASSETS_DIR,
)

# ═══════════════════════════════════════════════════════════════
#  CSS
# ═══════════════════════════════════════════════════════════════
_CSS = """
<style>
/* ── 전역 배경 / 폰트 ─── */
.stApp { background: #060b14 !important; }
.stApp * { font-family: "Segoe UI", "Malgun Gothic", sans-serif !important; }
.stApp header { background: transparent !important; }
div[data-testid="stDecoration"] { display: none; }
#MainMenu, footer { visibility: hidden; }
.block-container { padding-top: 1.4rem !important; padding-bottom: 0.5rem !important; }

/* ── 탭 ─── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: #0b1220;
    border-bottom: 1px solid #162030;
    gap: 0;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    color: #7a9ab8 !important;
    border-bottom: 2px solid transparent;
    padding: 10px 16px;
    font-size: 13px !important;
    letter-spacing: .4px;
    background: transparent !important;
    transition: all .18s;
}
[data-testid="stTabs"] [aria-selected="true"] {
    color: #d4af37 !important;
    border-bottom-color: #d4af37 !important;
    font-weight: 700 !important;
    background: rgba(212,175,55,.05) !important;
}
[data-testid="stTabs"] [data-baseweb="tab-highlight"] { display: none; }
[data-testid="stTabs"] [data-baseweb="tab-panel"] { padding: 0 !important; }

/* ── 버튼 기본 ─── */
[data-testid="stButton"] > button {
    background: linear-gradient(180deg,#111d2e,#0b1422) !important;
    border: 1px solid #1e3048 !important;
    color: #7a9ab8 !important;
    border-radius: 8px !important;
    transition: all .18s !important;
    font-size: 12px !important;
    letter-spacing: .4px !important;
}
[data-testid="stButton"] > button:hover {
    border-color: #243852 !important;
    color: #c8d8e8 !important;
    background: #152030 !important;
}

/* ── primary 버튼 ─── */
[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg,#1a6b3c,#0f4d2b) !important;
    border-color: rgba(16,185,129,.35) !important;
    color: #a7f3d0 !important;
    font-weight: 700 !important;
    font-size: 13.5px !important;
    letter-spacing: .6px !important;
    box-shadow: 0 3px 14px rgba(16,185,129,.18) !important;
}
[data-testid="stButton"] > button[kind="primary"]:hover {
    background: linear-gradient(135deg,#22924f,#196038) !important;
    box-shadow: 0 4px 20px rgba(16,185,129,.32) !important;
}

/* ── 구분선 ─── */
hr { border-color: #162030 !important; margin: 0.6rem 0 !important; }

/* ── 스크롤바 ─── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #060b14; }
::-webkit-scrollbar-thumb { background: #1e3048; border-radius: 4px; }

/* ── 탭 콘텐츠 상단 여백 ─── */
[data-testid="stTabsContent"] { padding-top: 12px !important; }
</style>
"""

# ═══════════════════════════════════════════════════════════════
#  세션 초기화
# ═══════════════════════════════════════════════════════════════
def _init_state() -> None:
    defaults: dict = {
        "pose"        : "idle",
        "show_weapon" : True,
        "active_cat"  : "weapons",   # 마지막으로 아이템을 클릭한 카테고리
        "eq_weapons"  : "w1",
        "eq_armors"   : "a1",
        "eq_helmets"  : "h1",
        "eq_capes"    : "ca1",
        "ci_weapons"  : 0,
        "ci_armors"   : 0,
        "ci_helmets"  : 0,
        "ci_capes"    : 0,
        "none_armors" : False,
        "none_helmets": False,
        "none_capes"  : False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ═══════════════════════════════════════════════════════════════
#  헬퍼
# ═══════════════════════════════════════════════════════════════
def _b64(data: bytes) -> str:
    return base64.b64encode(data).decode()


def _icon_html(item_id: str, size: int = 52) -> str:
    data = load_icon_bytes(item_id)
    if data:
        return (
            f'<img src="data:image/png;base64,{_b64(data)}" '
            f'style="max-height:{size}px;max-width:{size}px;'
            f'object-fit:contain;image-rendering:crisp-edges">'
        )
    return f'<div style="width:{size}px;height:{size}px;background:#0a1422;border-radius:4px"></div>'


def _none_icon_html(size: int = 44) -> str:
    return (
        f'<svg viewBox="0 0 60 60" width="{size}" height="{size}">'
        '<line x1="15" y1="15" x2="45" y2="45" stroke="#3a506a" stroke-width="4" stroke-linecap="round"/>'
        '<line x1="45" y1="15" x2="15" y2="45" stroke="#3a506a" stroke-width="4" stroke-linecap="round"/>'
        '<circle cx="30" cy="30" r="20" fill="none" stroke="#3a506a" stroke-width="3"/>'
        '</svg>'
    )


def _current_slot(cat: str) -> tuple[str, int] | None:
    """현재 장착 정보를 (item_id, chroma_idx) 튜플로 반환. 미착용이면 None."""
    if st.session_state.get(f"none_{cat}", False):
        return None
    eq = st.session_state.get(f"eq_{cat}")
    ci = st.session_state.get(f"ci_{cat}", 0)
    return (eq, ci) if eq else None


# ═══════════════════════════════════════════════════════════════
#  아이템 카드
# ═══════════════════════════════════════════════════════════════
def _item_card(item: Item | dict, cat: str) -> None:
    is_none  = isinstance(item, dict)
    item_id  = item["id"]    if is_none else item.id
    name_ko  = "미착용 (None)" if is_none else item.name_ko
    grade    = None           if is_none else item.grade
    is_owned = True           if is_none else item.is_owned
    chromas  = []             if is_none else item.chromas

    none_key = f"none_{cat}"
    eq_key   = f"eq_{cat}"
    ci_key   = f"ci_{cat}"

    # 선택 여부
    if is_none:
        is_selected = st.session_state.get(none_key, False)
    else:
        is_selected = (
            not st.session_state.get(none_key, False)
            and st.session_state.get(eq_key) == item_id
        )

    grade_col  = GRADE_COLOR.get(grade, "#445566") if grade else "#445566"
    border_col = "#d4af37" if is_selected else ("#1a2840" if is_none else f"{grade_col}44")
    shadow     = "box-shadow:0 0 0 2px #d4af37,0 0 12px rgba(212,175,55,.2);" if is_selected else ""
    unowned_f  = "filter:grayscale(.75);opacity:.45;" if not is_owned else ""

    # 상단 등급 바
    top_bar = ""
    if grade == "Special":
        top_bar = (
            '<div style="position:absolute;top:0;left:0;right:0;height:3px;'
            'border-radius:9px 9px 0 0;background:linear-gradient(90deg,'
            'transparent 5%,#b060f8 25%,#e2a8ff 50%,#b060f8 75%,transparent 95%);'
            'box-shadow:0 2px 8px rgba(176,96,248,.3)"></div>'
        )
    elif grade == "Rare":
        top_bar = (
            f'<div style="position:absolute;top:0;left:0;right:0;height:3px;'
            f'border-radius:9px 9px 0 0;background:linear-gradient(90deg,'
            f'transparent,{grade_col} 35%,{grade_col} 65%,transparent);'
            f'box-shadow:0 2px 8px rgba(74,154,247,.3)"></div>'
        )
    elif grade == "Normal":
        top_bar = (
            '<div style="position:absolute;top:0;left:0;right:0;height:3px;'
            'border-radius:9px 9px 0 0;background:linear-gradient(90deg,'
            'transparent,#94a3b8 40%,#94a3b8 60%,transparent);opacity:.4"></div>'
        )

    badge_html = (
        f'<span style="font-size:8px;color:{grade_col};font-weight:700;'
        f'border:1px solid {grade_col};padding:1px 5px;border-radius:7px">'
        f'{grade}</span>'
        if grade
        else '<span style="font-size:8px;color:#3a5068">착용 해제</span>'
    )
    chroma_info = (
        f'<span style="font-size:8px;color:#3a5068">크로마 {len(chromas)}</span>'
        if chromas else ""
    )
    unowned_badge = (
        '<div style="position:absolute;top:5px;right:5px;background:rgba(4,7,15,.9);'
        'border:1px solid #2a3a52;color:#637283;font-size:7px;padding:1px 5px;'
        'border-radius:3px">미보유</div>'
        if not is_owned and not is_none else ""
    )
    icon_html = _none_icon_html() if is_none else _icon_html(item_id)

    st.markdown(
        f'<div style="background:#0d1422;border:1px solid {border_col};'
        f'border-radius:9px;padding:7px 7px 6px;{shadow}margin-bottom:3px;'
        f'position:relative;overflow:hidden">'
        f'{top_bar}{unowned_badge}'
        f'<div style="background:#090e1d;border-radius:6px;height:68px;'
        f'display:flex;align-items:center;justify-content:center;margin-bottom:5px;'
        f'border:1px solid rgba(255,255,255,.03);{unowned_f}">{icon_html}</div>'
        f'<div style="font-size:10px;line-height:1.4;color:#dde4f2;min-height:2.6em;'
        f'margin-bottom:4px;{unowned_f}">{name_ko}</div>'
        f'<div style="display:flex;justify-content:space-between;align-items:center">'
        f'{badge_html}{chroma_info}</div></div>',
        unsafe_allow_html=True,
    )

    if is_selected:
        st.markdown(
            '<p style="text-align:center;color:#d4af37;font-size:10px;'
            'margin:0 0 2px 0;font-weight:600">✓ 선택됨</p>',
            unsafe_allow_html=True,
        )
    else:
        btn_label = "👁 미리보기" if not is_owned and not is_none else "▶ 선택"
        if st.button(btn_label, key=f"sel_{cat}_{item_id}", use_container_width=True):
            if is_none:
                st.session_state[none_key] = True
            else:
                st.session_state[none_key] = False
                st.session_state[eq_key]   = item_id
                st.session_state[ci_key]   = 0
            st.session_state["active_cat"] = cat
            st.rerun()


# ═══════════════════════════════════════════════════════════════
#  크로마 팔레트
# ═══════════════════════════════════════════════════════════════
def _chroma_panel(cat: str) -> None:
    none_key = f"none_{cat}"
    eq_key   = f"eq_{cat}"
    ci_key   = f"ci_{cat}"

    st.markdown(
        '<div style="font-size:9.5px;letter-spacing:2.5px;color:#d4af37;'
        'text-transform:uppercase;margin-bottom:9px;display:flex;align-items:center;gap:8px">'
        'CHROMA PALETTE'
        '<div style="flex:1;height:1px;background:linear-gradient(90deg,'
        'rgba(212,175,55,.3),transparent)"></div></div>',
        unsafe_allow_html=True,
    )

    if st.session_state.get(none_key, False):
        st.markdown(
            '<p style="color:#3a5068;font-size:11.5px;padding:4px 0">'
            '미착용 상태에는 크로마가 없습니다.</p>',
            unsafe_allow_html=True,
        )
        return

    eq_id = st.session_state.get(eq_key)
    if not eq_id:
        st.markdown(
            '<p style="color:#3a5068;font-size:11.5px;padding:4px 0">'
            '아이템을 선택하면 크로마 목록이 표시됩니다.</p>',
            unsafe_allow_html=True,
        )
        return

    item: Item | None = next(
        (it for it in CATEGORIES[cat] if it.id == eq_id), None
    )
    if item is None or not item.chromas:
        st.markdown(
            '<p style="color:#3a5068;font-size:11.5px;padding:4px 0">'
            '크로마가 없습니다.</p>',
            unsafe_allow_html=True,
        )
        return

    cur_idx = st.session_state.get(ci_key, 0)
    n = len(item.chromas)
    cols = st.columns(min(n, 8))

    for i, ch in enumerate(item.chromas):
        with cols[i]:
            sel  = cur_idx == i
            ring = "box-shadow:0 0 0 2.5px #d4af37,0 0 10px rgba(212,175,55,.4);" if sel else ""
            lock = (
                '<div style="position:absolute;inset:0;border-radius:50%;'
                'background:rgba(4,7,15,.58);display:flex;align-items:center;'
                'justify-content:center"><span style="font-size:11px">🔒</span></div>'
                if not ch.is_owned else ""
            )
            st.markdown(
                f'<div style="width:40px;height:40px;border-radius:50%;margin:0 auto 4px;'
                f'background:radial-gradient(circle at 35% 30%,rgba(255,255,255,.55),'
                f'transparent 45%),{ch.color};border:2px solid rgba(255,255,255,.2);'
                f'{ring}position:relative;overflow:hidden">{lock}</div>'
                f'<div style="font-size:8.5px;color:#7a9ab8;text-align:center;'
                f'overflow:hidden;text-overflow:ellipsis;white-space:nowrap">'
                f'{ch.name.split("(")[0].strip()}</div>',
                unsafe_allow_html=True,
            )
            indicator = "●" if sel else "○"
            if st.button(indicator, key=f"ch_{cat}_{i}",
                         use_container_width=True, help=ch.name):
                st.session_state[ci_key] = i
                st.session_state["active_cat"] = cat
                st.rerun()


# ═══════════════════════════════════════════════════════════════
#  캐릭터 프리뷰
# ═══════════════════════════════════════════════════════════════
def _render_preview() -> None:
    pose        = st.session_state.pose
    show_weapon = st.session_state.show_weapon

    img = composite_preview(
        pose        = pose,
        weapon      = _current_slot("weapons"),
        armor       = _current_slot("armors"),
        helmet      = _current_slot("helmets"),
        cape        = _current_slot("capes"),
        show_weapon = show_weapon,
    )

    if img is not None:
        b64_str = _b64(preview_to_bytes(img))
        img_tag = (
            f'<img src="data:image/png;base64,{b64_str}" '
            'style="max-height:52vh;max-width:100%;object-fit:contain;'
            'image-rendering:crisp-edges;'
            'filter:drop-shadow(0 4px 16px rgba(0,0,0,.55))">'
        )
    elif not PIL_OK:
        img_tag = (
            '<div style="color:#3a5068;font-size:12px;text-align:center;padding:40px 0">'
            'Pillow 미설치<br><code>pip install Pillow</code></div>'
        )
    elif not assets_available():
        img_tag = (
            '<div style="color:#3a5068;font-size:12px;text-align:center;'
            'line-height:2;padding:30px 0">'
            f'에셋 없음 — <code>python setup_assets.py</code> 실행 필요<br>'
            f'<span style="font-size:10px">{ASSETS_DIR}</span></div>'
        )
    else:
        img_tag = '<div style="color:#3a5068;padding:40px 0;text-align:center">로딩 중…</div>'

    pose_label = "COMBAT" if pose == "combat" else "IDLE"
    weapon_label = "" if show_weapon else "  <span style='color:#e84b4b;font-size:9px'>무기 숨김</span>"

    st.markdown(
        f'<div style="'
        f'background:radial-gradient(ellipse at 50% 96%,rgba(212,175,55,.1) 0%,transparent 52%),'
        f'radial-gradient(ellipse at 65% 18%,rgba(79,142,247,.05) 0%,transparent 40%),'
        f'linear-gradient(190deg,#111e32 0%,#080d1e 100%);'
        f'border:1px solid #243852;border-radius:11px;'
        f'padding:20px 16px 14px;'
        f'display:flex;flex-direction:column;align-items:center;justify-content:center;'
        f'min-height:340px;position:relative;overflow:hidden;'
        f'box-shadow:inset 0 0 50px rgba(0,0,0,.4)">'
        # 광선
        f'<div style="position:absolute;bottom:-10%;left:50%;transform:translateX(-50%);'
        f'width:260%;height:140%;'
        f'background:conic-gradient(from 260deg at 50% 100%,'
        f'transparent 0deg,rgba(212,175,55,.018) 4deg,transparent 8deg,'
        f'transparent 18deg,rgba(212,175,55,.014) 22deg,transparent 26deg);'
        f'pointer-events:none"></div>'
        # 바닥 스테이지 빛
        f'<div style="position:absolute;bottom:12px;left:50%;transform:translateX(-50%);'
        f'width:40%;height:4px;'
        f'background:radial-gradient(ellipse,rgba(212,175,55,.22),transparent 72%);'
        f'filter:blur(8px)"></div>'
        # 포즈 배지
        f'<div style="position:absolute;top:10px;right:10px;'
        f'background:rgba(4,7,15,.8);border:1px solid #1e3048;border-radius:5px;'
        f'font-size:9px;color:#3a5068;letter-spacing:1.5px;padding:3px 8px">'
        f'{pose_label}{weapon_label}</div>'
        f'{img_tag}'
        f'</div>',
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════
#  정보 칩
# ═══════════════════════════════════════════════════════════════
def _info_chips() -> None:
    cat = st.session_state.active_cat
    eq  = st.session_state.get(f"eq_{cat}")
    ci  = st.session_state.get(f"ci_{cat}", 0)
    is_none = st.session_state.get(f"none_{cat}", False)

    item: Item | None = None
    if not is_none and eq:
        item = next((it for it in CATEGORIES[cat] if it.id == eq), None)

    chroma: Chroma | None = None
    if item and item.chromas and ci < len(item.chromas):
        chroma = item.chromas[ci]

    grade_col  = GRADE_COLOR.get(item.grade, "#94a3b8") if item else "#445566"
    grade_str  = f"{GRADE_LABEL_KO.get(item.grade, '')} ({item.grade})" if item else "—"
    chroma_str = f"{chroma.name.split('(')[0].strip()} · {chroma.color.upper()}" if chroma else "—"
    dot_col    = chroma.color if chroma else "#3a5068"
    name_str   = item.name_ko if item else "—"

    c1, c2 = st.columns(2)
    chip_style = (
        'background:rgba(4,7,15,.85);border:1px solid rgba(255,255,255,.05);'
        'border-left:2px solid rgba(212,175,55,.38);border-radius:5px;'
        'padding:7px 10px;font-size:11px;line-height:1.7;backdrop-filter:blur(8px)'
    )
    with c1:
        st.markdown(
            f'<div style="{chip_style}">'
            f'<div style="color:#3a5068;font-size:8.5px;letter-spacing:1.5px">외형 (APPEARANCE)</div>'
            f'<div style="font-weight:600;color:#dde4f2;overflow:hidden;'
            f'text-overflow:ellipsis;white-space:nowrap">{name_str}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f'<div style="{chip_style}">'
            f'<div style="color:#3a5068;font-size:8.5px;letter-spacing:1.5px">등급 / 크로마</div>'
            f'<div style="font-weight:600;color:{grade_col}">{grade_str}</div>'
            f'<div style="display:flex;align-items:center;gap:6px;margin-top:1px">'
            f'<div style="width:10px;height:10px;border-radius:50%;background:{dot_col};'
            f'border:1.5px solid rgba(255,255,255,.3);flex-shrink:0"></div>'
            f'<span style="color:#7a9ab8;font-size:9px;overflow:hidden;'
            f'text-overflow:ellipsis;white-space:nowrap">{chroma_str}</span>'
            f'</div></div>',
            unsafe_allow_html=True,
        )


# ═══════════════════════════════════════════════════════════════
#  보유 현황 + 미보유 체크
# ═══════════════════════════════════════════════════════════════
def _inventory_state() -> tuple[int, int, int, int, list[str]]:
    """owned_items, tot_items, owned_chromas, tot_chromas, unowned_names"""
    from data.items import WEAPONS, ARMORS, HELMETS, CAPES
    all_items = WEAPONS + ARMORS + HELMETS + CAPES
    total_items   = len(all_items)
    owned_items   = sum(1 for it in all_items if it.is_owned)
    total_chromas = sum(len(it.chromas) for it in all_items)
    owned_chromas = sum(sum(1 for c in it.chromas if c.is_owned) for it in all_items)

    unowned: list[str] = []
    for cat in ("weapons", "armors", "helmets", "capes"):
        if st.session_state.get(f"none_{cat}", False):
            continue
        eq_id = st.session_state.get(f"eq_{cat}")
        if not eq_id:
            continue
        item = next((it for it in CATEGORIES[cat] if it.id == eq_id), None)
        if item and not item.is_owned:
            unowned.append(item.name_ko)
        ci = st.session_state.get(f"ci_{cat}", 0)
        if item and item.chromas and ci < len(item.chromas):
            ch = item.chromas[ci]
            if not ch.is_owned:
                unowned.append(f'{item.name_ko} 크로마 "{ch.name.split("(")[0].strip()}"')

    return owned_items, total_items, owned_chromas, total_chromas, unowned


# ═══════════════════════════════════════════════════════════════
#  메인 렌더러
# ═══════════════════════════════════════════════════════════════
def render_closet() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)
    _init_state()

    # ── 헤더 ────────────────────────────────────────────────────
    h_col, badge_col = st.columns([3, 1])
    with h_col:
        st.markdown(
            '<h2 style="color:#d4af37;letter-spacing:2px;font-size:1.35rem;margin:0 0 2px 0">'
            '✦ 스킨 UI  '
            '<span style="color:#3a5068;font-size:.62em;letter-spacing:1.5px;font-weight:400">'
            'SKIN UI — CLOSET</span></h2>',
            unsafe_allow_html=True,
        )
    with badge_col:
        st.markdown(
            '<div style="text-align:right;padding-top:6px">'
            '<span style="font-size:10px;color:#3a5068;letter-spacing:2.5px;'
            'border:1px solid rgba(212,175,55,.1);background:rgba(212,175,55,.03);'
            'padding:3px 10px;border-radius:3px">CHROMA SYSTEM PROTOTYPE</span>'
            '</div>',
            unsafe_allow_html=True,
        )
    st.markdown('<hr>', unsafe_allow_html=True)

    # ── 메인 레이아웃 ─────────────────────────────────────────────
    col_left, col_right = st.columns([40, 60], gap="large")

    # ════════════════════════════════════════════════════════════
    #  왼쪽 — 캐릭터 프리뷰 + 컨트롤
    # ════════════════════════════════════════════════════════════
    with col_left:
        _render_preview()

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        _info_chips()
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        # 포즈 / 무기 버튼
        bc1, bc2 = st.columns(2)
        with bc1:
            is_combat = st.session_state.pose == "combat"
            if st.button(
                "🧍 대기 자세" if is_combat else "⚔ 전투 자세",
                key="pose_btn", use_container_width=True,
            ):
                st.session_state.pose = "idle" if is_combat else "combat"
                st.rerun()
        with bc2:
            show_w = st.session_state.show_weapon
            if st.button(
                "🚫 무기 숨김" if show_w else "👁 무기 표시",
                key="weapon_btn", use_container_width=True,
            ):
                st.session_state.show_weapon = not show_w
                st.rerun()

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        # 적용 버튼
        owned_i, tot_i, owned_c, tot_c, unowned = _inventory_state()
        if st.button("✔  적용 (Apply)", key="apply_btn",
                     use_container_width=True, type="primary"):
            if unowned:
                st.error(f"미보유 아이템이 있습니다 — {' / '.join(unowned)}")
            else:
                st.success("외형이 적용되었습니다! ✔")

        # 보유 현황 패널
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        preview_warn = (
            '<div style="background:rgba(232,75,75,.07);border:1px solid rgba(232,75,75,.28);'
            'border-radius:6px;padding:6px 10px;font-size:10px;color:#fca5a5;margin-top:6px">'
            '⚠  미보유 아이템 착용 중 — PREVIEW 모드</div>'
            if unowned else ""
        )
        st.markdown(
            f'<div style="background:#0b1220;border:1px solid #162030;border-radius:8px;'
            f'padding:11px 14px">'
            f'<div style="color:#3a5068;font-size:8.5px;letter-spacing:2px;margin-bottom:6px">'
            f'보유 현황 (INVENTORY)</div>'
            f'<div style="display:flex;gap:20px">'
            f'<div><span style="color:#d4af37;font-weight:700;font-size:1.15em">{owned_i}</span>'
            f'<span style="color:#3a5068;font-size:11px"> / {tot_i} 외형</span></div>'
            f'<div><span style="color:#4b8ce8;font-weight:700;font-size:1.15em">{owned_c}</span>'
            f'<span style="color:#3a5068;font-size:11px"> / {tot_c} 크로마</span></div>'
            f'</div></div>'
            f'{preview_warn}',
            unsafe_allow_html=True,
        )

    # ════════════════════════════════════════════════════════════
    #  오른쪽 — 탭 + 아이템 그리드 + 크로마 팔레트
    # ════════════════════════════════════════════════════════════
    with col_right:
        tab_labels = list(CAT_LABEL.values())
        tab_keys   = list(CAT_LABEL.keys())
        tabs = st.tabs(tab_labels)

        for tab, cat in zip(tabs, tab_keys):
            with tab:
                items_to_show: list = []
                if cat != "weapons":
                    items_to_show.append(none_item(cat))
                items_to_show.extend(CATEGORIES[cat])

                # 4열 아이템 그리드
                COLS = 4
                for row_start in range(0, len(items_to_show), COLS):
                    row_items = items_to_show[row_start : row_start + COLS]
                    grid_cols = st.columns(COLS)
                    for gc, item in zip(grid_cols, row_items):
                        with gc:
                            _item_card(item, cat)

                st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

                # 크로마 팔레트 (탭 내부)
                _chroma_panel(cat)
