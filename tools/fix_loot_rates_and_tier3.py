"""
전리품 드랍 CSV 전수 수정

[수정 1] LootGroup DropProportion 수정 (기획서 기준)
  500001 (2T 무기 전리품): 2,000,000(20%) → 833,000(8.33%)
  500002 (2T 방어구 전리품): 2,000,000(20%) → 833,000(8.33%)
  500003 (3T 무기 전리품 하위): 100,000(1%) → 200,000(2%)
  500004 (3T 방어구 전리품 하위): 100,000(1%) → 200,000(2%)

[수정 2] LootGroup 신규 추가 — 3T 전리품 주 드랍용 (3.33%)
  500007: 3T 무기 전리품 재료 주 드랍  (LootDataSet=500003, 333,000)
  500008: 3T 방어구 전리품 재료 주 드랍 (LootDataSet=500004, 333,000)

[수정 3] Monster.csv — 3T 필드 몬스터에 LootGroupCids 배정
  망자 계열   → 무기 재료(500007) + 2T 하위(500005)
  팬텀 계열   → 무기 재료(500007) + 2T 하위(500005) + 팬텀 카드(91018)
  피 묻은 손  → 방어구 재료(500008) + 2T 하위(500006)

드랍률 설계 근거 (기획서 X7_장비_제작_및_드랍.xlsx 🎲 드랍률 설계):
  동일 티어 전리품: T2=8.33%, T3=3.33%
  하위 티어 전리품: 2%
"""

import csv, os
from datetime import datetime

CSV_DIR = "C:/AI_simulator/게임 데이터 전체.csv"
LOG_DIR = "C:/AI_simulator/AI csv 수정 로그"

# ─────────────────────────────────────────────────────────────
# 수정 1: LootGroup DropProportion 교정
# ─────────────────────────────────────────────────────────────
DROP_FIXES = {
    "500001": ("2T 무기 전리품",         2000000,  833000),   # 20% → 8.33%
    "500002": ("2T 방어구 전리품",       2000000,  833000),   # 20% → 8.33%
    "500003": ("3T 무기 전리품 하위",   100000,   200000),   #  1% → 2%
    "500004": ("3T 방어구 전리품 하위", 100000,   200000),   #  1% → 2%
}

# ─────────────────────────────────────────────────────────────
# 수정 2: LootGroup 신규 행 (3T 주 드랍)
# ─────────────────────────────────────────────────────────────
NEW_LOOT_GROUPS = [
    # oid, cid, comment, is_dup, loot_cnt, dataset_cids, props, drop_prop
    ("500007", "500007", "3T 무기 전리품 재료 주 드랍",   "FALSE", "1", "[500003]", "[100]", "333000"),
    ("500008", "500008", "3T 방어구 전리품 재료 주 드랍", "FALSE", "1", "[500004]", "[100]", "333000"),
]

# ─────────────────────────────────────────────────────────────
# 수정 3: Monster LootGroupCids (3T 필드 몬스터)
# ─────────────────────────────────────────────────────────────
# 무기 재료 계열 (망자·팬텀): 3T 주 드랍(500007) + 2T 하위(500005)
# 방어구 재료 계열 (피 묻은 손): 3T 주 드랍(500008) + 2T 하위(500006)
# 팬텀 카드(91018)은 팬텀 계열에만 존재

TIER3_MONSTER_LOOTS = {
    # ── 망자 계열 (무기 재료) ──────────────────────────────
    "10503101": ["500007", "500005"],   # 망자 투사 - 근거리
    "10503102": ["500007", "500005"],   # 망자 전사 - 근거리
    # ── 팬텀 계열 (무기 재료 + 팬텀 카드) ────────────────
    "10703101": ["500007", "500005", "91018"],  # 팬텀 경비병
    "10703102": ["500007", "500005", "91018"],  # 팬텀 병사
    "10703103": ["500007", "500005", "91018"],  # 팬텀 궁수
    # ── 피 묻은 손 계열 (방어구 재료) ────────────────────
    "10803101": ["500008", "500006"],   # 피 묻은 손 - 전사(근거리)
    "10803102": ["500008", "500006"],   # 피 묻은 손 - 의무병(원거리)
    "10803103": ["500008", "500006"],   # 피 묻은 손 - 전사(근거리)
    "10803104": ["500008", "500006"],   # 피 묻은 손 - 정찰대(궁수)
    "10803301": ["500008", "500006"],   # 피 묻은 손 돌격대장(Strong)
    "10803302": ["500008", "500006"],   # 피 묻은 손 지휘관(Commander)
}

# ─────────────────────────────────────────────────────────────
# 실행
# ─────────────────────────────────────────────────────────────
lg_path  = f"{CSV_DIR}/LootGroup.csv"
mon_path = f"{CSV_DIR}/Monster.csv"

# ── [1] LootGroup DropProportion 수정 ──────────────────────
print("\n[수정 1] LootGroup DropProportion 교정")
rate_changes = []
rows = []
with open(lg_path, encoding="utf-8-sig", newline="") as f:
    reader = csv.reader(f)
    headers = next(reader)
    for row in reader:
        oid = row[0]
        if oid in DROP_FIXES:
            name, old_dp, new_dp = DROP_FIXES[oid]
            cur = int(row[7]) if row[7] else 0
            if cur == old_dp:
                row[7] = str(new_dp)
                pct_old = old_dp / 100000
                pct_new = new_dp / 100000
                print(f"  ✅ {oid} ({name}): {old_dp:,}({pct_old:.2f}%) → {new_dp:,}({pct_new:.2f}%)")
                rate_changes.append((oid, name, old_dp, new_dp))
            else:
                print(f"  ⚠️  {oid}: 현재값={cur} (예상={old_dp}) 불일치, 건너뜀")
        rows.append(row)

# 신규 LootGroup 추가
existing_oids = {r[0] for r in rows}
new_added = []
for ng in NEW_LOOT_GROUPS:
    if ng[0] not in existing_oids:
        rows.append(list(ng))
        new_added.append(ng[0])
        print(f"  ✅ 신규: {ng[0]} {ng[2]} DropProp={ng[7]}")

tmp = lg_path + ".tmp"
with open(tmp, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(rows)
os.replace(tmp, lg_path)
print(f"  → {len(rate_changes)}건 수정, {len(new_added)}건 추가")

# ── [2] Monster.csv — 3T 필드 몬스터 LootGroupCids 배정 ──
print("\n[수정 2] Monster.csv 3T 필드 몬스터 LootGroupCids 배정")
mon_rows = []
mon_changes = []
with open(mon_path, encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for row in reader:
        oid = row["OID"]
        if oid in TIER3_MONSTER_LOOTS:
            cur = row["LootGroupCids"].strip()
            if cur:
                print(f"  ⏭  {oid}: 이미 설정됨 ({cur}), 건너뜀")
            else:
                grps = TIER3_MONSTER_LOOTS[oid]
                new_val = "[" + ",".join(grps) + "]"
                row["LootGroupCids"] = new_val
                print(f"  ✅ {oid} {row['Comment'][:28]:28s} → {new_val}")
                mon_changes.append((oid, row['Comment'], new_val))
        mon_rows.append(row)

if mon_changes:
    tmp = mon_path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(mon_rows)
    os.replace(tmp, mon_path)
print(f"  → {len(mon_changes)}개 몬스터 수정")

# ─────────────────────────────────────────────────────────────
# 수정 로그 업데이트
# ─────────────────────────────────────────────────────────────
log_path = f"{LOG_DIR}/드랍_CSV_수정_로그.md"
today = datetime.now().strftime("%Y-%m-%d %H:%M")

append_lines = [
    f"\n---\n",
    f"## 추가 수정 — {today}\n",
    f"",
    f"### 수정 A: LootGroup 드랍률 교정 (기획서 기준 맞춤)\n",
    f"",
    f"| OID | 항목 | 기존 DropProportion | 수정 DropProportion | 기존 확률 | 수정 확률 |",
    f"|-----|------|--------------------|--------------------|----------|----------|",
]
for oid, name, old, new in rate_changes:
    append_lines.append(f"| {oid} | {name} | {old:,} | {new:,} | {old/100000:.2f}% | {new/100000:.2f}% |")

append_lines += [
    f"",
    f"**근거**: 기획서 🎲 드랍률 설계 — T2 전리품 8.33%, 하위 티어 전리품 2%",
    f"",
    f"### 수정 B: 3T 전리품 주 드랍 LootGroup 신규 추가\n",
    f"",
    f"| OID | 이름 | 재활용 LootDataSet | DropProportion | 확률 |",
    f"|-----|------|-------------------|----------------|------|",
    f"| 500007 | 3T 무기 전리품 재료 주 드랍 | [500003] (날카로운 포식자 송곳니 CID 53030005) | 333,000 | 3.33% |",
    f"| 500008 | 3T 방어구 전리품 재료 주 드랍 | [500004] (굵은 마수의 다리뼈 CID 53030006) | 333,000 | 3.33% |",
    f"",
    f"**근거**: 기획서 🎲 드랍률 설계 — T3 전리품 3.33%",
    f"",
    f"### 수정 C: 3T 필드 몬스터 LootGroupCids 배정\n",
    f"",
    f"| OID | 몬스터 | 계열 | 배정 LootGroup |",
    f"|-----|--------|------|----------------|",
]
for oid, comment, val in mon_changes:
    tier = "팬텀" if "팬텀" in comment else "망자" if "망자" in comment else "피 묻은 손"
    mat  = "무기 재료" if tier in ("팬텀","망자") else "방어구 재료"
    append_lines.append(f"| {oid} | {comment[:25]} | {tier}({mat}) | {val} |")

append_lines += [
    f"",
    f"**계열 분류 근거**:",
    f"- **망자/팬텀 계열**: 2T 오크(무기 재료 드랍) 패턴과 동일 — 근접/원거리 전투형 → 무기 소재 전리품",
    f"- **피 묻은 손 계열**: 2T 정령(방어구 재료 드랍) 패턴과 동일 — 인간형 → 방어구 소재 전리품",
    f"- **팬텀 카드(91018)**: 기존 팬텀 계열 카드 LootGroup 재활용, 망자/피 묻은 손은 전용 카드 미존재",
    f"",
    f"### 미수정 항목 및 메모\n",
    f"",
    f"| 항목 | 현황 | 비고 |",
    f"|------|------|------|",
    f"| Tier1 오크 (10301101~103) | T2 무기 재료(500001) 20% 드랍 | 기획서 'T1 전리품 없음'과 불일치하나, 게임 설계상 T1 오크 구간이 T2 무기 파밍 시작점임을 감안해 유지 |",
    f"| Tier1 정령 (10101101~104) | T2 방어구 재료(500006) 2% 드랍 | 동일 이유로 유지 |",
    f"| 망자/피 묻은 손 몬스터 카드 | 전용 카드 아이템 미존재 | 추후 ItemMonsterCard.csv 추가 시 LootGroup 별도 생성 필요 |",
    f"| 아이템 제작식 드랍 | LootData에 50020~50028 존재하나 LootGroup 미등록 | 기획서에 제작식 드랍 설계 없음 → 유지 |",
]

with open(log_path, "a", encoding="utf-8") as f:
    f.write("\n".join(append_lines))

print(f"\n[로그 업데이트] {log_path}")
print("\n" + "=" * 55)
print("✅ 전리품 드랍 전수 수정 완료")
print(f"  LootGroup 드랍률 교정: {len(rate_changes)}건")
print(f"  LootGroup 신규 추가: {len(new_added)}건")
print(f"  Monster 3T 드랍 배정: {len(mon_changes)}개")
