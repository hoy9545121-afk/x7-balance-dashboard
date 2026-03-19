"""
드랍 CSV 보정 스크립트

[보정 1] Monster.csv — T3 필드 몬스터 loot 완전 설정
  - 카드만 들어간 몬스터들을 재료+카드 조합으로 덮어씀
  - 흙 정령 (10102106/10102305): [500006,91031] 신규 설정
  - 오우거 던전 (10902802): [2021,91029] 복원
  - 보스 페르눈/모르가리스: [500111,카드] 복원

[보정 2] LootGroup.csv — DropProportion 교정 (기획서 기준)
  - 500001 (T2 무기재료 주): 2,000,000(20%) → 833,000(8.33%)
  - 500002 (T2 방어구재료 주): 2,000,000(20%) → 833,000(8.33%)
  - 500003 (T3 무기재료 하위): 100,000(1%) → 200,000(2%)
  - 500004 (T3 방어구재료 하위): 100,000(1%) → 200,000(2%)
"""

import csv, os
from datetime import datetime

CSV_DIR = "C:/AI_simulator/게임 데이터 전체.csv"
LOG_DIR = "C:/AI_simulator/AI csv 수정 로그"


# ─────────────────────────────────────────────────────────────────────────────
# [보정 1] Monster.csv 강제 덮어쓰기 (FORCE SET)
# ─────────────────────────────────────────────────────────────────────────────
MONSTER_FORCE = {
    # ── 망자 계열: T3 무기재료 주(3.33%) + 하위(2%) + 원혼카드(1%) ────────────
    "10503101": "[500007,500005,91030]",
    "10503102": "[500007,500005,91030]",
    # ── 팬텀 계열: T3 무기재료 + 팬텀카드 + 원혼카드 ─────────────────────────
    "10703101": "[500007,500005,91018,91030]",
    "10703102": "[500007,500005,91018,91030]",
    "10703103": "[500007,500005,91018,91030]",
    # ── 피 묻은 손 계열: T3 방어구재료 주(3.33%) + 하위(2%) + 카드(1%) ────────
    "10803101": "[500008,500006,91034]",
    "10803102": "[500008,500006,91034]",
    "10803103": "[500008,500006,91034]",
    "10803104": "[500008,500006,91034]",
    "10803301": "[500008,500006,91034]",
    "10803302": "[500008,500006,91034]",
    # ── 오우거 던전: 원래 던전 상자(2021) + 오우거카드(91029) ─────────────────
    "10902802": "[2021,91029]",
    # ── 보스: 완제품 드랍(500111) + 카드 ─────────────────────────────────────
    "90003902": "[500111,91033]",   # 페르눈
    "90003903": "[500111,91032]",   # 모르가리스
    # ── 흙 정령: T2 방어구재료 하위(2%) + 흙정령카드(1%) ─────────────────────
    "10102106": "[500006,91031]",   # 흙 정령 비선공
    "10102305": "[500006,91031]",   # 흙 정령 선공(Strong)
}

# ─────────────────────────────────────────────────────────────────────────────
# [보정 2] LootGroup DropProportion 교정
# ─────────────────────────────────────────────────────────────────────────────
LG_FIXES = {
    # OID: (설명, 기존 DropProp, 신규 DropProp)
    "500001": ("T2 무기재료 주 드랍",   2000000, 833000),  # 20% → 8.33%
    "500002": ("T2 방어구재료 주 드랍", 2000000, 833000),  # 20% → 8.33%
    "500003": ("T3 무기재료 하위",      100000,  200000),  #  1% → 2%
    "500004": ("T3 방어구재료 하위",    100000,  200000),  #  1% → 2%
}


# ─────────────────────────────────────────────────────────────────────────────
# 실행
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


# ── [보정 1] Monster.csv ──────────────────────────────────────────────────────
print("\n[보정 1] Monster.csv — FORCE SET")
mon_path = f"{CSV_DIR}/Monster.csv"
mon_changes = []
mon_rows = []

with open(mon_path, encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for row in reader:
        oid = row["OID"]
        if oid in MONSTER_FORCE:
            old = row["LootGroupCids"].strip()
            new = MONSTER_FORCE[oid]
            if old == new:
                print(f"  ✔  {oid}: 이미 정확 ({old}), 건너뜀")
            else:
                row["LootGroupCids"] = new
                print(f"  ✅ {oid}: {old or '(없음)'!r} → {new}")
                mon_changes.append((oid, old, new))
        mon_rows.append(row)

if mon_changes:
    tmp = mon_path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(mon_rows)
    os.replace(tmp, mon_path)
print(f"  → {len(mon_changes)}개 수정")


# ── [보정 2] LootGroup.csv ────────────────────────────────────────────────────
print("\n[보정 2] LootGroup.csv — DropProportion 교정")
lg_path = f"{CSV_DIR}/LootGroup.csv"
headers, rows = read_csv(lg_path)
lg_changes = []

for row in rows:
    oid = row[0]
    if oid in LG_FIXES:
        name, old_dp, new_dp = LG_FIXES[oid]
        cur = int(row[7]) if row[7] else 0
        if cur == old_dp:
            row[7] = str(new_dp)
            pct_old = old_dp / 10000000 * 100
            pct_new = new_dp / 10000000 * 100
            print(f"  ✅ {oid} ({name}): {old_dp:,}({pct_old:.2f}%) → {new_dp:,}({pct_new:.2f}%)")
            lg_changes.append((oid, name, old_dp, new_dp))
        elif cur == new_dp:
            print(f"  ✔  {oid}: 이미 {new_dp:,}으로 설정됨, 건너뜀")
        else:
            print(f"  ⚠️  {oid}: 현재={cur:,} (예상={old_dp:,}) 불일치, 강제 교정")
            row[7] = str(new_dp)
            lg_changes.append((oid, name, cur, new_dp))

write_csv(lg_path, headers, rows)
print(f"  → {len(lg_changes)}건 교정")


# ─────────────────────────────────────────────────────────────────────────────
# 로그 업데이트
# ─────────────────────────────────────────────────────────────────────────────
log_path = f"{LOG_DIR}/카드_드랍_수정_로그.md"
today = datetime.now().strftime("%Y-%m-%d %H:%M")

append_lines = [
    f"\n---\n",
    f"## 보정 수정 — {today}\n",
    f"",
    f"### 보정 A: Monster.csv T3 몬스터 loot 완전 설정\n",
    f"",
    f"| OID | 기존 | 수정 후 |",
    f"|-----|------|---------|",
]
for oid, old, new in mon_changes:
    append_lines.append(f"| {oid} | {old or '(없음)'} | {new} |")

append_lines += [
    f"",
    f"**보정 사유**: 직전 스크립트에서 APPEND 대상 몬스터 LootGroupCids가 비어 있어",
    f"재료 그룹 없이 카드만 설정됨. 설계 기준에 맞게 전체 조합으로 강제 덮어씀.",
    f"",
    f"### 보정 B: LootGroup DropProportion 교정 (기획서 기준)\n",
    f"",
    f"| OID | 이름 | 기존 DropProp | 수정 DropProp | 기존 확률 | 수정 확률 |",
    f"|-----|------|-------------|-------------|---------|---------|",
]
for oid, name, old, new in lg_changes:
    append_lines.append(
        f"| {oid} | {name} | {old:,} | {new:,} | {old/10000000*100:.2f}% | {new/10000000*100:.2f}% |"
    )

append_lines += [
    f"",
    f"**근거**: 기획서 드랍률 설계 — T2 전리품 8.33%, 하위 티어 2%",
]

with open(log_path, "a", encoding="utf-8") as f:
    f.write("\n".join(append_lines))

print(f"\n[로그] {log_path}")
print("\n" + "=" * 55)
print("✅ 보정 완료")
print(f"  Monster.csv: {len(mon_changes)}개 수정")
print(f"  LootGroup.csv: {len(lg_changes)}건 교정")
