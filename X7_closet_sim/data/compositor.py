"""PNG 레이어 합성 — Pillow alpha_composite 기반
레이어 순서: shadow → cape_back → base → armor → helmet → cape_front → weapon → effect
"""
from __future__ import annotations
from io import BytesIO
from pathlib import Path

import streamlit as st

try:
    from PIL import Image
    PIL_OK = True
except ImportError:
    PIL_OK = False

# ── 에셋 경로 해결 ────────────────────────────────────────────────
# 1순위: 앱 디렉터리 안의 assets/
# 2순위: 부모 디렉터리의 리소스/assets/ (로컬 개발용)
_SCRIPT_DIR = Path(__file__).parent.parent   # X7_closet_sim/
_CANDIDATES = [
    _SCRIPT_DIR / "assets",
    _SCRIPT_DIR.parent / "리소스" / "assets",
]
ASSETS_DIR: Path = next((p for p in _CANDIDATES if p.exists()), _CANDIDATES[0])

CANVAS_W, CANVAS_H = 400, 560   # 모든 스프라이트의 공통 크기


# ── 파일 로더 (Streamlit 캐시) ────────────────────────────────────
@st.cache_data(show_spinner=False)
def _load_bytes(path: str) -> bytes | None:
    try:
        return Path(path).read_bytes()
    except (FileNotFoundError, OSError):
        return None


def _open(path: Path) -> "Image.Image | None":
    if not PIL_OK:
        return None
    data = _load_bytes(str(path))
    if data is None:
        return None
    try:
        img = Image.open(BytesIO(data)).convert("RGBA")
        # 크기가 다르면 캔버스에 맞춤 (없는 부분은 투명)
        if img.size != (CANVAS_W, CANVAS_H):
            canvas = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
            canvas.paste(img, (0, 0))
            return canvas
        return img
    except Exception:
        return None


def _paste(comp: "Image.Image", layer: "Image.Image | None") -> "Image.Image":
    if layer is None:
        return comp
    return Image.alpha_composite(comp, layer)


# ── 경로 빌더 ────────────────────────────────────────────────────
def _chroma_suffix(idx: int) -> str:
    return "" if idx <= 0 else f"_c{idx + 1}"


def _item_path(slot: str, item_id: str, pose: str, chroma_idx: int) -> Path:
    cS = _chroma_suffix(chroma_idx)
    return ASSETS_DIR / slot / f"{item_id}_{pose}{cS}.png"


def _cape_path(item_id: str, pose: str, chroma_idx: int, side: str) -> Path:
    cS = _chroma_suffix(chroma_idx)
    return ASSETS_DIR / "cape" / f"{item_id}_{pose}{cS}_{side}.png"


def _effect_path(item_id: str, pose: str, chroma_idx: int) -> Path:
    cS = _chroma_suffix(chroma_idx)
    return ASSETS_DIR / "effect" / f"{item_id}_{pose}{cS}.png"


# ── 메인 합성 함수 ────────────────────────────────────────────────
def composite_preview(
    pose: str,
    weapon:  tuple[str, int] | None,  # (item_id, chroma_idx)
    armor:   tuple[str, int] | None,
    helmet:  tuple[str, int] | None,
    cape:    tuple[str, int] | None,
    show_weapon: bool = True,
) -> "Image.Image | None":
    """
    8개 레이어를 alpha_composite로 합성한 PIL Image 반환.
    PIL 미설치 또는 파일 없으면 None 반환.
    """
    if not PIL_OK:
        return None

    comp = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))

    # 1. Shadow
    comp = _paste(comp, _open(ASSETS_DIR / "base" / "shadow.png"))

    # 2. Cape back
    if cape:
        comp = _paste(comp, _open(_cape_path(cape[0], pose, cape[1], "back")))

    # 3. Base body (pose-aware)
    comp = _paste(comp, _open(ASSETS_DIR / "base" / f"body_{pose}.png"))

    # 4. Armor
    if armor:
        comp = _paste(comp, _open(_item_path("armor", armor[0], pose, armor[1])))

    # 5. Helmet
    if helmet:
        comp = _paste(comp, _open(_item_path("helmet", helmet[0], pose, helmet[1])))

    # 6. Cape front
    if cape:
        comp = _paste(comp, _open(_cape_path(cape[0], pose, cape[1], "front")))

    # 7. Weapon
    if weapon and show_weapon:
        comp = _paste(comp, _open(_item_path("weapon", weapon[0], pose, weapon[1])))

    # 8. Effect overlay
    #    우선순위: 무기 effect → 망토 effect
    if weapon and show_weapon:
        comp = _paste(comp, _open(_effect_path(weapon[0], pose, weapon[1])))
    elif cape:
        comp = _paste(comp, _open(_effect_path(cape[0], pose, cape[1])))

    return comp


def preview_to_bytes(img: "Image.Image") -> bytes:
    """PIL Image → PNG bytes (base64 인코딩 전 단계)."""
    buf = BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


# ── 아이콘 로더 ──────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_icon_bytes(item_id: str) -> bytes | None:
    return _load_bytes(str(ASSETS_DIR / "icons" / f"{item_id}.png"))


def assets_available() -> bool:
    """에셋 폴더가 존재하고 base body가 있으면 True."""
    return (ASSETS_DIR / "base" / "body_idle.png").exists()
