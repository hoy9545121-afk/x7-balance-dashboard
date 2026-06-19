"""스킨 아이템 데이터 — 무기 / 갑옷 / 투구 / 망토"""
from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class Chroma:
    id: str
    name: str
    color: str      # hex  e.g. "#3b82f6"
    is_owned: bool = True


@dataclass
class Item:
    id: str
    name: str           # 한국어 (영문) 형식
    grade: str          # Normal | Rare | Special
    is_owned: bool
    chromas: list[Chroma] = field(default_factory=list)

    @property
    def name_ko(self) -> str:
        return self.name.split("(")[0].strip()

    @property
    def name_en(self) -> str:
        s = self.name
        if "(" in s:
            return s[s.index("(") + 1 : s.index(")")]
        return ""


# ── "미착용" 더미 아이템 ─────────────────────────────────────────
def none_item(category: str) -> dict:
    return {"id": f"none-{category}", "name": "미착용 (None)",
            "grade": None, "is_owned": True, "is_none": True, "chromas": []}


# ── 등급 색상 ────────────────────────────────────────────────────
GRADE_COLOR: dict[str, str] = {
    "Normal" : "#94a3b8",
    "Rare"   : "#4a9af7",
    "Special": "#b060f8",
}
GRADE_LABEL_KO: dict[str, str] = {
    "Normal" : "일반",
    "Rare"   : "희귀",
    "Special": "스페셜",
}


# ── 무기 ─────────────────────────────────────────────────────────
WEAPONS: list[Item] = [
    Item("w1", "빛나는 마력의 검 (Shining Magic Sword)", "Special", True, [
        Chroma("c1", "기본형 (Default)", "#3b82f6", True),
        Chroma("c2", "루비 (Ruby)",     "#ef4444", True),
        Chroma("c3", "흑요석 (Obsidian)","#1f2937", False),
    ]),
    Item("w2", "가디언의 거대 도끼 (Guardian's Great Axe)", "Rare", False, [
        Chroma("c4", "기본형 (Default)", "#10b981", True),
        Chroma("c5", "골드 (Gold)",     "#eab308", False),
    ]),
    Item("w3", "천공의 지팡이 (Sky Staff)", "Special", False, [
        Chroma("c11", "기본형 (Default)",  "#8b5cf6", True),
        Chroma("c12", "천공 (Sky Blue)",   "#38bdf8", False),
        Chroma("c13", "황혼 (Twilight)",   "#f59e0b", False),
    ]),
    Item("w4", "냉혹한 단검 (Frostbite Dagger)", "Normal", True, [
        Chroma("c14", "기본형 (Default)", "#94a3b8", True),
        Chroma("c15", "서리 (Frost)",    "#bae6fd", True),
    ]),
    Item("w5", "집행자의 대검 (Executioner's Greatsword)", "Rare", True, [
        Chroma("c16", "기본형 (Default)", "#b91c1c", True),
        Chroma("c17", "암흑 (Dark)",     "#1c1917", False),
    ]),
]

# ── 갑옷 ─────────────────────────────────────────────────────────
ARMORS: list[Item] = [
    Item("a1", "심판관의 철갑옷 (Judge's Iron Armor)", "Rare", True, [
        Chroma("ca1", "기본형 (Default)", "#4b5563", True),
        Chroma("ca2", "골드 (Gold)",     "#eab308", False),
    ]),
    Item("a2", "용기사의 비늘갑옷 (Dragon Knight Scale)", "Special", True, [
        Chroma("ca3", "기본형 (Default)",    "#dc2626", True),
        Chroma("ca4", "심해 (Deep Sea)",     "#0369a1", True),
        Chroma("ca5", "흑룡 (Black Dragon)", "#1a1a2e", False),
    ]),
    Item("a3", "달빛 천 갑옷 (Moonlight Cloth Armor)", "Normal", True, [
        Chroma("ca6", "기본형 (Default)", "#cbd5e1", True),
        Chroma("ca7", "새벽 (Dawn)",     "#fde68a", False),
    ]),
    Item("a4", "심해 잠수함 갑옷 (Abyss Diver Armor)", "Rare", False, [
        Chroma("ca8", "기본형 (Default)", "#0ea5e9", True),
        Chroma("ca9", "산호 (Coral)",    "#fb7185", False),
    ]),
]

# ── 투구 ─────────────────────────────────────────────────────────
HELMETS: list[Item] = [
    Item("h1", "성기사의 투구 (Paladin's Helmet)", "Normal", False, [
        Chroma("ch1", "기본형 (Default)", "#9ca3af", True),
    ]),
    Item("h2", "암흑 마법사의 두건 (Dark Mage Hood)", "Rare", True, [
        Chroma("ch2", "기본형 (Default)", "#1e1b4b", True),
        Chroma("ch3", "심홍 (Crimson)",   "#9f1239", True),
        Chroma("ch4", "심록 (Forest)",    "#14532d", False),
    ]),
    Item("h3", "천사의 왕관 (Angel's Crown)", "Special", False, [
        Chroma("ch5", "기본형 (Default)",      "#fef9c3", True),
        Chroma("ch6", "성스러운 (Holy Gold)",  "#d97706", False),
    ]),
    Item("h4", "태양신의 투구 (Sun God's Helm)", "Special", True, [
        Chroma("ch7", "기본형 (Default)", "#b45309", True),
        Chroma("ch8", "황금 (Gold)",      "#f59e0b", True),
        Chroma("ch9", "흑철 (Black Iron)","#292524", False),
    ]),
]

# ── 망토 ─────────────────────────────────────────────────────────
CAPES: list[Item] = [
    Item("ca1", "군주의 영광 망토 (Lord's Glory Cape)", "Special", True, [
        Chroma("cc1", "기본형 (Default)",  "#dc2626", True),
        Chroma("cc2", "에메랄드 (Emerald)","#059669", True),
    ]),
    Item("ca2", "어둠의 날개 망토 (Shadow Wing Cape)", "Rare", True, [
        Chroma("cc3", "기본형 (Default)",      "#1e293b", True),
        Chroma("cc4", "자정 (Midnight)",       "#0f172a", True),
        Chroma("cc5", "황금 날개 (Golden Wing)","#ca8a04", False),
    ]),
    Item("ca3", "불꽃 술사 망토 (Flame Sorcerer Cape)", "Normal", False, [
        Chroma("cc6", "기본형 (Default)", "#ea580c", True),
        Chroma("cc7", "빙화 (Ice Flame)", "#0ea5e9", False),
    ]),
    Item("ca4", "공허의 법의 (Void Sorcerer Robe)", "Special", False, [
        Chroma("cc8",  "기본형 (Default)", "#6d28d9", True),
        Chroma("cc9",  "심연 (Abyss)",    "#1e1b4b", False),
        Chroma("cc10", "빛 (Light)",       "#e9d5ff", False),
    ]),
]

# ── 카테고리 매핑 ────────────────────────────────────────────────
CATEGORIES: dict[str, list[Item]] = {
    "weapons": WEAPONS,
    "armors" : ARMORS,
    "helmets": HELMETS,
    "capes"  : CAPES,
}
CAT_LABEL: dict[str, str] = {
    "weapons": "⚔ 무기 (Weapon)",
    "armors" : "🛡 갑옷 (Armor)",
    "helmets": "🪖 투구 (Helmet)",
    "capes"  : "🧣 망토 (Cape)",
}
CAT_SLOT: dict[str, str] = {
    "weapons": "weapon",
    "armors" : "armor",
    "helmets": "helmet",
    "capes"  : "cape",
}
