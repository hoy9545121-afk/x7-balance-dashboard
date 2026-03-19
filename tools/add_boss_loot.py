"""
보스 완제품 드랍 CSV 수정
X7_장비_제작_및_드랍.xlsx 기준으로 LootData / LootDataSet / LootGroup / Monster.csv 갱신

[추가 내용]
  LootData  (500110~500127): 보스 드랍 완제품 아이템 18개
  LootDataSet (500110, 500111): 2T/3T 보스 드랍 세트 2개
  LootGroup   (500110, 500111): 2T 1%, 3T 0.5% 드랍 그룹

[Monster 수정]
  2T 보스 5종 → 500110 추가
  3T 보스 4종 → 500111 추가
"""

import csv, os, re
from datetime import datetime

CSV_DIR  = "C:/AI_simulator/게임 데이터 전체.csv"
LOG_DIR  = "C:/AI_simulator/AI csv 수정 로그"
os.makedirs(LOG_DIR, exist_ok=True)

# ─────────────────────────────────────────────────────────────
# 수정 데이터 정의
# ─────────────────────────────────────────────────────────────

# LootData 신규 행: (oid, cid, comment, loot_cat, value, enh, grade, min_c, max_c)
NEW_LOOT_DATA = [
    # ── 2T 보스 드랍 완제품 ───────────────────────────────
    (500110, 500110, "2T 판금 신발(드랍)",  "Item", 12020022, 0, "Common", 1, 1),
    (500111, 500111, "2T 가죽 신발(드랍)",  "Item", 12020023, 0, "Common", 1, 1),
    (500112, 500112, "2T 천 신발(드랍)",    "Item", 12020024, 0, "Common", 1, 1),
    # ── 3T 보스 드랍 완제품 (투구) ───────────────────────
    (500113, 500113, "3T 판금 투구(드랍)",  "Item", 12030025, 0, "Common", 1, 1),
    (500114, 500114, "3T 가죽 투구(드랍)",  "Item", 12030026, 0, "Common", 1, 1),
    (500115, 500115, "3T 천 투구(드랍)",    "Item", 12030027, 0, "Common", 1, 1),
    # ── 3T 보스 드랍 완제품 (갑옷) ───────────────────────
    (500116, 500116, "3T 판금 갑옷(드랍)",  "Item", 12030028, 0, "Common", 1, 1),
    (500117, 500117, "3T 가죽 갑옷(드랍)",  "Item", 12030029, 0, "Common", 1, 1),
    (500118, 500118, "3T 천 갑옷(드랍)",    "Item", 12030030, 0, "Common", 1, 1),
    # ── 3T 보스 드랍 완제품 (신발 v1 — 판금/가죽/천) ────
    (500119, 500119, "3T 판금 신발_1(드랍)","Item", 12030031, 0, "Common", 1, 1),
    (500120, 500120, "3T 가죽 신발_1(드랍)","Item", 12030032, 0, "Common", 1, 1),
    (500121, 500121, "3T 천 신발_1(드랍)",  "Item", 12030033, 0, "Common", 1, 1),
    # ── 3T 보스 드랍 완제품 (신발 v2) ────────────────────
    (500122, 500122, "3T 판금 신발_2(드랍)","Item", 12030034, 0, "Common", 1, 1),
    (500123, 500123, "3T 가죽 신발_2(드랍)","Item", 12030035, 0, "Common", 1, 1),
    (500124, 500124, "3T 천 신발_2(드랍)",  "Item", 12030036, 0, "Common", 1, 1),
    # ── 3T 보스 드랍 완제품 (신발 v3) ────────────────────
    (500125, 500125, "3T 판금 신발_3(드랍)","Item", 12030037, 0, "Common", 1, 1),
    (500126, 500126, "3T 가죽 신발_3(드랍)","Item", 12030038, 0, "Common", 1, 1),
    (500127, 500127, "3T 천 신발_3(드랍)",  "Item", 12030039, 0, "Common", 1, 1),
]

# LootDataSet 신규 행: (oid, cid, comment, loot_data_cids_str, proportions_str)
ITEMS_2T = [500110, 500111, 500112]
ITEMS_3T = list(range(500113, 500128))   # 500113~500127 (15개)
PROPS_2T = [100] * len(ITEMS_2T)
PROPS_3T = [100] * len(ITEMS_3T)

def fmt_arr(lst):
    return "[" + ",".join(str(x) for x in lst) + "]"

NEW_LOOT_DATASET = [
    (500110, 500110, "2T 보스 완제품 드랍 세트", fmt_arr(ITEMS_2T), fmt_arr(PROPS_2T)),
    (500111, 500111, "3T 보스 완제품 드랍 세트", fmt_arr(ITEMS_3T), fmt_arr(PROPS_3T)),
]

# LootGroup 신규 행: (oid, cid, comment, is_dup, loot_cnt, dataset_cids, props, drop_prop)
# DropProportion: 10000000=100%, 100000=1%, 50000=0.5%
NEW_LOOT_GROUP = [
    (500110, 500110, "2T 보스 완제품 드랍", "FALSE", 1, "[500110]", "[100]", 100000),
    (500111, 500111, "3T 보스 완제품 드랍", "FALSE", 1, "[500111]", "[100]",  50000),
]

# Monster.csv 수정: {OID: loot_group_cid_to_add}
MONSTER_UPDATES = {
    # ── 2T 보스 (신발 완제품 드랍) ──
    "10302801": 500110,   # 오크 족장 (Hero, Tier2 필드)
    "90002901": 500110,   # 말카바돈 (Boss, Tier2 필드 레이드)
    "90002903": 500110,   # 분노의 잔재 말카바돈 (Boss, Tier2 1인 던전)
    "10702804": 500110,   # 팬텀 대장 (Hero, Tier2 1인 던전-A)
    "10702805": 500110,   # 팬텀 대장 (Hero, Tier2 1인 던전-B)
    # ── 3T 보스 (투구/갑옷/신발 완제품 드랍) ──
    "90003901": 500111,   # 스칼니토스 (Boss, Tier3 필드 레이드)
    "90002904": 500111,   # 격노의 잔재 말카바돈 (Boss, Tier3 1인 던전)
    "90003902": 500111,   # 하얀 모래의 페르눈 (Boss, Tier3)
    "90003903": 500111,   # 영혼을 거두는 모르가리스 (Boss, Tier3)
}

# ─────────────────────────────────────────────────────────────
# 헬퍼
# ─────────────────────────────────────────────────────────────
def append_csv(path, headers, new_rows):
    """CSV 파일 끝에 신규 행 추가. 이미 OID 존재 시 건너뜀."""
    existing_oids = set()
    with open(path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing_oids.add(row["OID"])

    added = []
    with open(path, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        for row in new_rows:
            oid = str(row[0])
            if oid in existing_oids:
                print(f"  ⏭  {oid} 이미 존재 — 건너뜀")
            else:
                writer.writerow(row)
                added.append(oid)
                print(f"  ✅ 추가: {oid} {row[2]}")
    return added


def add_loot_group_to_monster(monster_csv, oid_str, loot_grp_cid):
    """Monster.csv 특정 OID 행의 LootGroupCids 컬럼에 loot_grp_cid 추가"""
    rows = []
    changed = False
    with open(monster_csv, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            if row["OID"] == oid_str:
                cur = row["LootGroupCids"].strip()
                new_cid = str(loot_grp_cid)
                if not cur or cur == "":
                    row["LootGroupCids"] = f"[{new_cid}]"
                else:
                    # '[a,b,c]' → 파싱 후 추가
                    inner = cur.strip("[]")
                    existing = [x.strip() for x in inner.split(",") if x.strip()]
                    if new_cid not in existing:
                        existing.append(new_cid)
                        row["LootGroupCids"] = "[" + ",".join(existing) + "]"
                    else:
                        print(f"  ⏭  OID={oid_str}: {new_cid} 이미 포함")
                        rows.append(row)
                        continue
                print(f"  ✅ OID={oid_str}: LootGroupCids → {row['LootGroupCids']}")
                changed = True
            rows.append(row)

    if changed:
        tmp = monster_csv + ".tmp"
        with open(tmp, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        os.replace(tmp, monster_csv)
    return changed


# ─────────────────────────────────────────────────────────────
# STEP 1: LootData.csv
# ─────────────────────────────────────────────────────────────
print("\n[STEP 1] LootData.csv 신규 행 추가")
ld_path = f"{CSV_DIR}/LootData.csv"
ld_headers = ["OID","Cid","Comment","LootCategory","Value","ItemEnhanceStep","ItemGradeStep","MinCount","MaxCount"]
ld_added = append_csv(ld_path, ld_headers, NEW_LOOT_DATA)
print(f"  → {len(ld_added)}행 추가")

# STEP 2: LootDataSet.csv
print("\n[STEP 2] LootDataSet.csv 신규 행 추가")
lds_path = f"{CSV_DIR}/LootDataSet.csv"
lds_headers = ["OID","Cid","Comment","LootDataCids","Proportions"]
lds_added = append_csv(lds_path, lds_headers, NEW_LOOT_DATASET)
print(f"  → {len(lds_added)}행 추가")

# STEP 3: LootGroup.csv
print("\n[STEP 3] LootGroup.csv 신규 행 추가")
lg_path = f"{CSV_DIR}/LootGroup.csv"
lg_headers = ["OID","Cid","Comment","IsDuplicate","LootCount","LootDataSetCids","Proportions","DropProportion"]
lg_added = append_csv(lg_path, lg_headers, NEW_LOOT_GROUP)
print(f"  → {len(lg_added)}행 추가")

# STEP 4: Monster.csv
print("\n[STEP 4] Monster.csv LootGroupCids 갱신")
mon_path = f"{CSV_DIR}/Monster.csv"
mon_changes = []
for oid_str, grp_cid in sorted(MONSTER_UPDATES.items()):
    ok = add_loot_group_to_monster(mon_path, oid_str, grp_cid)
    if ok:
        mon_changes.append((oid_str, grp_cid))
print(f"  → {len(mon_changes)}개 몬스터 수정")

# ─────────────────────────────────────────────────────────────
# STEP 5: 수정 사항 로그 저장
# ─────────────────────────────────────────────────────────────
log_path = f"{LOG_DIR}/드랍_CSV_수정_로그.md"
today = datetime.now().strftime("%Y-%m-%d %H:%M")

log_lines = [
    f"# 드랍 CSV 수정 로그",
    f"",
    f"**수정일**: {today}",
    f"**기준 문서**: `기획서/X7_장비_제작_및_드랍.xlsx` — 🎲 드랍률 설계 / 📋 장비 아이템 리스트",
    f"",
    f"---",
    f"",
    f"## 개요",
    f"",
    f"보스 몬스터가 완제품 장비를 직접 드랍하는 기능이 누락되어 있음을 확인하고 신규 추가.",
    f"- **2T 보스 완제품 드랍**: 1.0% (DropProportion = 100,000)",
    f"- **3T 보스 완제품 드랍**: 0.5% (DropProportion = 50,000)",
    f"- 드랍 시 1개 확정, 아이템 풀에서 균등 랜덤 선택",
    f"",
    f"---",
    f"",
    f"## 수정 파일 목록",
    f"",
    f"| 파일 | 변경 | 내용 |",
    f"|------|------|------|",
    f"| `LootData.csv` | +18행 | 2T 신발 3종 + 3T 투구/갑옷/신발×3×3종 = 18개 LootData |",
    f"| `LootDataSet.csv` | +2행 | 2T 보스 드랍 세트(3종) / 3T 보스 드랍 세트(15종) |",
    f"| `LootGroup.csv` | +2행 | 2T 보스 완제품 드랍 1% / 3T 보스 완제품 드랍 0.5% |",
    f"| `Monster.csv` | 9개 OID 수정 | 2T 보스 5종 / 3T 보스 4종 LootGroupCids 추가 |",
    f"",
    f"---",
    f"",
    f"## 1. LootData.csv 추가 행 (OID 500110 ~ 500127)",
    f"",
    f"| OID | 아이템 이름 | 장비 CID |",
    f"|-----|-------------|----------|",
]
for oid, cid, comment, cat, value, enh, grade, mn, mx in NEW_LOOT_DATA:
    log_lines.append(f"| {oid} | {comment} | {value} |")

log_lines += [
    f"",
    f"---",
    f"",
    f"## 2. LootDataSet.csv 추가 행 (OID 500110 ~ 500111)",
    f"",
    f"| OID | 이름 | 포함 LootData CID 목록 |",
    f"|-----|------|------------------------|",
    f"| 500110 | 2T 보스 완제품 드랍 세트 | {fmt_arr(ITEMS_2T)} (3종) |",
    f"| 500111 | 3T 보스 완제품 드랍 세트 | {fmt_arr(ITEMS_3T)} (15종) |",
    f"",
    f"---",
    f"",
    f"## 3. LootGroup.csv 추가 행 (OID 500110 ~ 500111)",
    f"",
    f"| OID | 이름 | DropProportion | 확률 |",
    f"|-----|------|----------------|------|",
    f"| 500110 | 2T 보스 완제품 드랍 | 100,000 | 1.00% |",
    f"| 500111 | 3T 보스 완제품 드랍 | 50,000 | 0.50% |",
    f"",
    f"---",
    f"",
    f"## 4. Monster.csv 수정 (LootGroupCids 추가)",
    f"",
    f"| OID | 몬스터 이름 | 티어 | 등급 | 추가 LootGroup |",
    f"|-----|-------------|------|------|----------------|",
    f"| 10302801 | 오크 족장 | Tier2 | Hero  | 500110 (2T 보스 완제품 1%) |",
    f"| 90002901 | 말카바돈 (필드) | Tier2 | Boss  | 500110 |",
    f"| 90002903 | 분노의 잔재 말카바돈 (던전) | Tier2 | Boss  | 500110 |",
    f"| 10702804 | 팬텀 대장 1인던전-A | Tier2 | Hero  | 500110 |",
    f"| 10702805 | 팬텀 대장 1인던전-B | Tier2 | Hero  | 500110 |",
    f"| 90003901 | 스칼니토스 (필드 레이드) | Tier3 | Boss  | 500111 (3T 보스 완제품 0.5%) |",
    f"| 90002904 | 격노의 잔재 말카바돈 (던전) | Tier3 | Boss  | 500111 |",
    f"| 90003902 | 하얀 모래의 페르눈 | Tier3 | Boss  | 500111 |",
    f"| 90003903 | 영혼을 거두는 모르가리스 | Tier3 | Boss  | 500111 |",
    f"",
    f"---",
    f"",
    f"## 5. 드랍 구조 다이어그램",
    f"",
    f"```",
    f"[Monster]",
    f"  └─ LootGroupCids",
    f"       ├─ 500110 (2T 보스 완제품 드랍, DropProp=100000=1%)",
    f"       │    └─ LootDataSetCids: [500110]",
    f"       │         └─ LootDataCids: [500110, 500111, 500112]  ← 균등 랜덤",
    f"       │              ├─ 500110 → CID 12020022 (2T 판금 신발)",
    f"       │              ├─ 500111 → CID 12020023 (2T 가죽 신발)",
    f"       │              └─ 500112 → CID 12020024 (2T 천 신발)",
    f"       │",
    f"       └─ 500111 (3T 보스 완제품 드랍, DropProp=50000=0.5%)",
    f"            └─ LootDataSetCids: [500111]",
    f"                 └─ LootDataCids: [500113 ~ 500127]  ← 15종 균등 랜덤",
    f"                      ├─ 500113 → CID 12030025 (3T 판금 투구)",
    f"                      ├─ 500114 → CID 12030026 (3T 가죽 투구)",
    f"                      ├─ 500115 → CID 12030027 (3T 천 투구)",
    f"                      ├─ 500116 → CID 12030028 (3T 판금 갑옷)",
    f"                      ├─ 500117 → CID 12030029 (3T 가죽 갑옷)",
    f"                      ├─ 500118 → CID 12030030 (3T 천 갑옷)",
    f"                      ├─ 500119 → CID 12030031 (3T 판금 신발_1)",
    f"                      ├─ 500120 → CID 12030032 (3T 가죽 신발_1)",
    f"                      ├─ 500121 → CID 12030033 (3T 천 신발_1)",
    f"                      ├─ 500122 → CID 12030034 (3T 판금 신발_2)",
    f"                      ├─ 500123 → CID 12030035 (3T 가죽 신발_2)",
    f"                      ├─ 500124 → CID 12030036 (3T 천 신발_2)",
    f"                      ├─ 500125 → CID 12030037 (3T 판금 신발_3)",
    f"                      ├─ 500126 → CID 12030038 (3T 가죽 신발_3)",
    f"                      └─ 500127 → CID 12030039 (3T 천 신발_3)",
    f"```",
    f"",
    f"---",
    f"",
    f"## 6. 설계 근거",
    f"",
    f"- **2T 보스 드랍 아이템**: 신발 3종만 드랍 (판금/가죽/천) — 기획서 📋 장비 아이템 리스트 row37~39",
    f"- **3T 보스 드랍 아이템**: 투구 3종 + 갑옷 3종 + 신발 9종 = 15종 — row64~78",
    f"- **드랍 확률**: 기획서 🎲 드랍률 설계 \"보스 완제품 드랍 0.5~1%\"",
    f"  - 2T: 1.0% (낮은 티어, 더 자주 접근 가능한 보스)",
    f"  - 3T: 0.5% (높은 티어, 레이드 난이도 반영)",
    f"- **아이템 풀**: 재질 무관 균등 배분 (Proportions 모두 100)",
    f"  유저가 원하는 재질(판금/가죽/천)을 특정할 수 없으므로 도박성 강화",
    f"",
]

with open(log_path, "w", encoding="utf-8") as f:
    f.write("\n".join(log_lines))

print(f"\n[STEP 5] 수정 로그 저장 → {log_path}")
print("\n" + "=" * 50)
print("✅ 드랍 CSV 수정 완료")
print(f"  LootData    +{len(ld_added)}행  (OID 500110~500127)")
print(f"  LootDataSet +{len(lds_added)}행  (OID 500110~500111)")
print(f"  LootGroup   +{len(lg_added)}행  (OID 500110~500111)")
print(f"  Monster      {len(mon_changes)}개 몬스터 수정")
print(f"  로그 → {log_path}")
