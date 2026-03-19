"""
신규 몬스터 카드 13종 및 관련 드랍 전수 수정

[수정 1] Item.csv — 신규 카드 아이템 13종 추가
  T1: 17010010(거북), 17010011(게)
  T2: 17020003(거미), 17020005(두들링), 17020006(멧돼지), 17020007(벌),
      17020009(불곰), 17020011(오우거), 17020012(원혼), 17020014(흙정령)
  T3: 17030004(모르가리스), 17030005(페르눈), 17030006(피묻은손)

[수정 2] ItemMonsterCard.csv — 신규 카드 13종 추가

[수정 3] LootData.csv — 신규 카드 LootData 13종 추가 (OID 424009~424021)

[수정 4] LootDataSet.csv — 신규 카드 LootDataSet 13종 추가 (OID 424009~424021)

[수정 5] LootGroup.csv
  - 91021 DropProportion 교정: 150,000(1.5%) → 100,000(1%)
  - 신규 카드 LootGroup 13종 추가: 91022~91034 (각 DropProportion=100,000=1%)

[수정 6] Monster.csv — LootGroupCids 대규모 업데이트
  SET:     빈 필드에 새 loot 값 설정 (동물/곤충/원혼/오크족장/팬텀지휘관/분신체)
  APPEND:  기존 loot에 카드 그룹 추가 (망자/팬텀/피묻은손/보스)
  REPLACE: 흙 정령 카드 교체 (바위정령91015·이끼정령91016 → 흙정령91031)

기준: 기획서 몬스터_카드_아이템_목록.xlsx + 유저 지시 (카드 드랍 확률 1%)
"""

import csv, os
from datetime import datetime

CSV_DIR = "C:/AI_simulator/게임 데이터 전체.csv"
LOG_DIR = "C:/AI_simulator/AI csv 수정 로그"

# ─────────────────────────────────────────────────────────────────────────────
# 데이터 정의
# ─────────────────────────────────────────────────────────────────────────────

# (카드 OID, Comment, DescName, Tier, Grade, SortOrder prefix)
# SortOrder = prefix + OID (T1→9, T2→8, T3→7)
NEW_CARDS = [
    # T1 카드
    ("17010010", "거북 카드",      "거북",      "Tier1", "Common",   "9"),
    ("17010011", "게 카드",        "게",        "Tier1", "Common",   "9"),
    # T2 카드
    ("17020003", "거미 카드",      "거미",      "Tier2", "Common",   "8"),
    ("17020005", "두들링 카드",    "두들링",    "Tier2", "Common",   "8"),
    ("17020006", "멧돼지 카드",    "멧돼지",    "Tier2", "Common",   "8"),
    ("17020007", "벌 카드",        "벌",        "Tier2", "Common",   "8"),
    ("17020009", "불곰 카드",      "불곰",      "Tier2", "Common",   "8"),
    ("17020011", "오우거 카드",    "오우거",    "Tier2", "Common",   "8"),
    ("17020012", "원혼 카드",      "원혼",      "Tier2", "Common",   "8"),
    ("17020014", "흙정령 카드",    "흙정령",    "Tier2", "Common",   "8"),
    # T3 카드
    ("17030004", "모르가리스 카드","모르가리스","Tier3", "Uncommon", "7"),
    ("17030005", "페르눈 카드",    "페르눈",    "Tier3", "Uncommon", "7"),
    ("17030006", "피묻은손 카드",  "피묻은손",  "Tier3", "Uncommon", "7"),
]

# 카드 OID → LootData/LootDataSet OID (424009~424021)
CARD_LD_OID = {c[0]: str(424009 + i) for i, c in enumerate(NEW_CARDS)}

# 카드 OID → LootGroup OID (91022~91034)
CARD_LG_OID = {c[0]: str(91022 + i) for i, c in enumerate(NEW_CARDS)}

def item_grade(tier):
    return "Uncommon" if tier == "Tier3" else "Common"


# ─────────────────────────────────────────────────────────────────────────────
# Monster.csv 변경 정의
# ─────────────────────────────────────────────────────────────────────────────

# [SET] 빈 LootGroupCids 필드에 신규 값 설정
MONSTER_SET = {
    # ── 동물/곤충 계열 ────────────────────────────────────────────────────────
    "10001101": "[91023]",               # 이니스 바위게     (게 카드)
    "10001102": "[91022]",               # 이니스 악어거북   (거북 카드)
    "10002101": "[91026]",               # 솔즈리드 멧돼지 Male
    "10002102": "[91026]",               # 솔즈리드 멧돼지 Female
    "10002103": "[91026]",               # 새끼 솔즈리드 멧돼지
    "10002301": "[91026]",               # 난폭한 솔즈리드 멧돼지 Strong
    "10002104": "[91028]",               # 배고픈 갈색 불곰 Male
    "10002105": "[91028]",               # 배고픈 갈색 불곰 Female
    "10002106": "[91028]",               # 배고픈 새끼 갈색 불곰
    "10002302": "[91028]",               # 성난 갈색 불곰 Strong
    "10002107": "[91022]",               # 백월만 바위 거북 T2
    "10002303": "[91023]",               # 백월만 거대 게 T2 Strong
    "11002101": "[91025]",               # 두들링 염탐꾼
    "11002102": "[91025]",               # 두들링 주술사
    "11002103": "[91025]",               # 두들링 전사
    "11102101": "[91027]",               # 육식성 말벌
    "11102102": "[91027]",               # 호위 벌
    "11102501": "[91027]",               # 여왕 벌 Commander
    "11102103": "[91024]",               # 새끼 평원 거미
    "11102104": "[91024]",               # 평원 거미
    "11102302": "[91024]",               # 난폭한 평원 거미 Strong
    # ── 원혼 계열 (T2 필드 언데드, 현재 loot 없음) ────────────────────────────
    "10402101": "[91030]",               # 돌격대원 원혼 Normal
    "10402102": "[91030]",               # 수습 의무병 원혼 Normal
    "10402103": "[91030]",               # 선원 원혼 Normal
    "10402104": "[91030]",               # 정찰대원 원혼 Normal
    "10402340": "[91030]",               # 돌격대장 원혼 Strong
    "10402705": "[91030]",               # 지휘관 원혼 Commander
    "10502101": "[91030]",               # 원한 어린 유령 Normal
    # ── T1 오크 족장 Hero (현재 loot 없음) ────────────────────────────────────
    "10301801": "[91009]",               # 오크 족장 T1 (오크 카드)
    # ── 팬텀 지휘관 T3 Commander (현재 loot 없음) ─────────────────────────────
    "10703701": "[500007,500005,91030]", # 성채 지휘관 원혼 (T3 무기재료+하위+원혼카드)
    # ── 모르가리스 분신체 Commander (현재 loot 없음) ──────────────────────────
    "90003701": "[91032]",               # 모르가리스 분신체
}

# [APPEND] 기존 LootGroupCids에 그룹 ID 추가
MONSTER_APPEND = {
    # 망자 계열: [500007,500005] → +91030
    "10503101": "91030",
    "10503102": "91030",
    # 팬텀 계열: [500007,500005,91018] → +91030
    "10703101": "91030",
    "10703102": "91030",
    "10703103": "91030",
    # 피 묻은 손 계열: [500008,500006] → +91034
    "10803101": "91034",
    "10803102": "91034",
    "10803103": "91034",
    "10803104": "91034",
    "10803301": "91034",
    "10803302": "91034",
    # 보스: [500111] → +카드
    "90003903": "91032",  # 모르가리스 본체
    "90003902": "91033",  # 페르눈
    # 오우거 던전: [2021] → +91029
    "10902802": "91029",
}

# [REPLACE] LootGroupCids 내 특정 ID 교체
MONSTER_REPLACE = {
    "10102106": ("91015", "91031"),  # 흙 정령: 바위정령카드 → 흙정령카드
    "10102305": ("91016", "91031"),  # 흙 정령 선공: 이끼정령카드 → 흙정령카드
}


# ─────────────────────────────────────────────────────────────────────────────
# 유틸 함수
# ─────────────────────────────────────────────────────────────────────────────

def read_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = list(reader)
    return headers, rows


def write_csv(path, headers, rows):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    os.replace(tmp, path)


# ─────────────────────────────────────────────────────────────────────────────
# [수정 1] Item.csv
# ─────────────────────────────────────────────────────────────────────────────
print("\n[수정 1] Item.csv — 신규 카드 아이템 추가")
item_path = f"{CSV_DIR}/Item.csv"
headers, rows = read_csv(item_path)
existing_oids = {r[0] for r in rows}
added_items = []

for oid, comment, descname, tier, grade, sort_pfx in NEW_CARDS:
    if oid in existing_oids:
        print(f"  ⏭  {oid}: 이미 존재, 건너뜀")
        continue
    sort_order = sort_pfx + oid
    new_row = [
        oid, oid, "Dev", comment, descname,
        "관련된 세트 효과 정보가 없습니다.",
        "MonsterCard", "0", tier, grade,
        "1", "0", "1", "1", "1", sort_order,
        "FALSE", "0", "0", "", "", "FALSE", "", "0", "999",
    ]
    rows.append(new_row)
    added_items.append(oid)
    print(f"  ✅ {oid} {comment} ({tier} {grade}) SortOrder={sort_order}")

write_csv(item_path, headers, rows)
print(f"  → {len(added_items)}종 추가")


# ─────────────────────────────────────────────────────────────────────────────
# [수정 2] ItemMonsterCard.csv
# ─────────────────────────────────────────────────────────────────────────────
print("\n[수정 2] ItemMonsterCard.csv — 신규 카드 추가")
imc_path = f"{CSV_DIR}/ItemMonsterCard.csv"
headers, rows = read_csv(imc_path)
existing_oids = {r[0] for r in rows}
added_imc = []

for oid, comment, descname, tier, grade, _ in NEW_CARDS:
    if oid in existing_oids:
        print(f"  ⏭  {oid}: 이미 존재, 건너뜀")
        continue
    rows.append([oid, oid, comment, "All", "1"])
    added_imc.append(oid)
    print(f"  ✅ {oid} {comment}")

write_csv(imc_path, headers, rows)
print(f"  → {len(added_imc)}종 추가")


# ─────────────────────────────────────────────────────────────────────────────
# [수정 3] LootData.csv
# ─────────────────────────────────────────────────────────────────────────────
print("\n[수정 3] LootData.csv — 신규 카드 LootData 추가")
ld_path = f"{CSV_DIR}/LootData.csv"
headers, rows = read_csv(ld_path)
existing_oids = {r[0] for r in rows}
added_ld = []

for card_oid, comment, descname, tier, grade, _ in NEW_CARDS:
    ld_oid = CARD_LD_OID[card_oid]
    if ld_oid in existing_oids:
        print(f"  ⏭  {ld_oid}: 이미 존재, 건너뜀")
        continue
    g = item_grade(tier)
    rows.append([ld_oid, ld_oid, comment, "Item", card_oid, "0", g, "1", "1"])
    added_ld.append(ld_oid)
    print(f"  ✅ {ld_oid} {comment} ItemCid={card_oid} Grade={g}")

write_csv(ld_path, headers, rows)
print(f"  → {len(added_ld)}종 추가")


# ─────────────────────────────────────────────────────────────────────────────
# [수정 4] LootDataSet.csv
# ─────────────────────────────────────────────────────────────────────────────
print("\n[수정 4] LootDataSet.csv — 신규 카드 LootDataSet 추가")
lds_path = f"{CSV_DIR}/LootDataSet.csv"
headers, rows = read_csv(lds_path)
existing_oids = {r[0] for r in rows}
added_lds = []

for card_oid, comment, descname, tier, grade, _ in NEW_CARDS:
    lds_oid = CARD_LD_OID[card_oid]   # LootDataSet OID = LootData OID
    ld_oid  = CARD_LD_OID[card_oid]
    if lds_oid in existing_oids:
        print(f"  ⏭  {lds_oid}: 이미 존재, 건너뜀")
        continue
    rows.append([lds_oid, lds_oid, comment, f"[{ld_oid}]", "[100]"])
    added_lds.append(lds_oid)
    print(f"  ✅ {lds_oid} {comment}")

write_csv(lds_path, headers, rows)
print(f"  → {len(added_lds)}종 추가")


# ─────────────────────────────────────────────────────────────────────────────
# [수정 5] LootGroup.csv
# ─────────────────────────────────────────────────────────────────────────────
print("\n[수정 5] LootGroup.csv — 91021 교정 + 신규 카드 LootGroup 추가")
lg_path = f"{CSV_DIR}/LootGroup.csv"
headers, rows = read_csv(lg_path)
existing_oids = {r[0] for r in rows}
fixed_lg = []
added_lg = []

for row in rows:
    if row[0] == "91021":
        cur_dp = row[7]
        if cur_dp == "150000":
            row[7] = "100000"
            print(f"  ✅ 91021 DropProportion: 150,000(1.5%) → 100,000(1%)")
            fixed_lg.append("91021")
        else:
            print(f"  ⚠️  91021 현재 DropProportion={cur_dp} (예상=150000), 건너뜀")

for card_oid, comment, descname, tier, grade, _ in NEW_CARDS:
    lg_oid  = CARD_LG_OID[card_oid]
    lds_oid = CARD_LD_OID[card_oid]
    if lg_oid in existing_oids:
        print(f"  ⏭  {lg_oid}: 이미 존재, 건너뜀")
        continue
    rows.append([lg_oid, lg_oid, comment, "FALSE", "1",
                 f"[{lds_oid}]", "[100]", "100000"])
    added_lg.append(lg_oid)
    print(f"  ✅ 신규: {lg_oid} {comment} → LDS={lds_oid} DropProp=100,000(1%)")

write_csv(lg_path, headers, rows)
print(f"  → {len(fixed_lg)}건 교정, {len(added_lg)}건 추가")


# ─────────────────────────────────────────────────────────────────────────────
# [수정 6] Monster.csv
# ─────────────────────────────────────────────────────────────────────────────
print("\n[수정 6] Monster.csv — LootGroupCids 대규모 업데이트")
mon_path = f"{CSV_DIR}/Monster.csv"
mon_changes = []
mon_rows = []

with open(mon_path, encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for row in reader:
        oid = row["OID"]
        cur = row["LootGroupCids"].strip()

        if oid in MONSTER_REPLACE:
            old_id, new_id = MONSTER_REPLACE[oid]
            if old_id in cur:
                new_val = cur.replace(old_id, new_id)
                row["LootGroupCids"] = new_val
                print(f"  ✅ REPLACE {oid}: {cur} → {new_val}")
                mon_changes.append((oid, "replace", cur, new_val))
            else:
                print(f"  ⚠️  REPLACE {oid}: '{old_id}' 미발견 (현재={cur!r}), 건너뜀")

        elif oid in MONSTER_APPEND:
            add_id = MONSTER_APPEND[oid]
            if add_id in cur:
                print(f"  ⏭  APPEND {oid}: {add_id} 이미 존재 ({cur}), 건너뜀")
            elif not cur:
                # 예외: 비어 있으면 그냥 set
                new_val = f"[{add_id}]"
                row["LootGroupCids"] = new_val
                print(f"  ✅ APPEND(empty→set) {oid}: → {new_val}")
                mon_changes.append((oid, "append", cur, new_val))
            else:
                # [a,b,c] → [a,b,c,add_id]
                new_val = cur.rstrip("]") + f",{add_id}]"
                row["LootGroupCids"] = new_val
                print(f"  ✅ APPEND {oid}: {cur} → {new_val}")
                mon_changes.append((oid, "append", cur, new_val))

        elif oid in MONSTER_SET:
            new_val = MONSTER_SET[oid]
            if cur:
                print(f"  ⏭  SET {oid}: 이미 설정됨 ({cur}), 건너뜀")
            else:
                row["LootGroupCids"] = new_val
                print(f"  ✅ SET {oid}: → {new_val}")
                mon_changes.append((oid, "set", "", new_val))

        mon_rows.append(row)

if mon_changes:
    tmp = mon_path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(mon_rows)
    os.replace(tmp, mon_path)

print(f"  → {len(mon_changes)}개 몬스터 수정")


# ─────────────────────────────────────────────────────────────────────────────
# 수정 로그
# ─────────────────────────────────────────────────────────────────────────────
log_path = f"{LOG_DIR}/카드_드랍_수정_로그.md"
today = datetime.now().strftime("%Y-%m-%d %H:%M")

lines = [
    f"# 카드 드랍 전수 수정 — {today}",
    f"",
    f"## 개요",
    f"",
    f"신규 몬스터 카드 13종 추가 및 Monster.csv LootGroupCids 대규모 업데이트.",
    f"카드 드랍 확률은 모두 1% (DropProportion=100,000/10,000,000).",
    f"",
    f"## 신규 카드 목록",
    f"",
    f"| 카드 OID | 카드명 | 티어 | 등급 | LootData OID | LootGroup OID |",
    f"|---------|--------|------|------|-------------|--------------|",
]
for card_oid, comment, descname, tier, grade, _ in NEW_CARDS:
    ld = CARD_LD_OID[card_oid]
    lg = CARD_LG_OID[card_oid]
    lines.append(f"| {card_oid} | {comment} | {tier} | {grade} | {ld} | {lg} |")

lines += [
    f"",
    f"## LootGroup 91021 교정",
    f"",
    f"91021 DropProportion 150,000(1.5%) → 100,000(1%)  ",
    f"**근거**: 유저 지시 — 몬스터 카드 드랍 확률 무조건 1%",
    f"",
    f"## Monster.csv 변경 내역",
    f"",
    f"| OID | 유형 | 기존 | 변경 후 |",
    f"|-----|------|------|---------|",
]
for oid, ctype, old, new in mon_changes:
    lines.append(f"| {oid} | {ctype} | {old or '(없음)'} | {new} |")

lines += [
    f"",
    f"## 수정 요약",
    f"",
    f"| 대상 | 수정 건수 |",
    f"|------|---------|",
    f"| Item.csv 신규 카드 | {len(added_items)} |",
    f"| ItemMonsterCard.csv 신규 | {len(added_imc)} |",
    f"| LootData.csv 신규 | {len(added_ld)} |",
    f"| LootDataSet.csv 신규 | {len(added_lds)} |",
    f"| LootGroup.csv 교정 | {len(fixed_lg)} |",
    f"| LootGroup.csv 신규 | {len(added_lg)} |",
    f"| Monster.csv 수정 | {len(mon_changes)} |",
]

os.makedirs(LOG_DIR, exist_ok=True)
with open(log_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"\n[로그] {log_path}")
print("\n" + "=" * 60)
print("✅ 카드 드랍 전수 수정 완료")
print(f"  Item.csv 신규 카드:            {len(added_items)}종")
print(f"  ItemMonsterCard.csv 신규:      {len(added_imc)}종")
print(f"  LootData.csv 신규:             {len(added_ld)}종")
print(f"  LootDataSet.csv 신규:          {len(added_lds)}종")
print(f"  LootGroup.csv 교정/추가:       {len(fixed_lg)}/{len(added_lg)}건")
print(f"  Monster.csv 수정:              {len(mon_changes)}개")
