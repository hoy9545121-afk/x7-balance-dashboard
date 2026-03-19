# tools/merge_armor_options.py
# 새 옵션 리스트 CSV와 기존 스탯값 CSV를 합쳐 generate_armor_balance.py용 CSV를 생성
# Input1: 방어구_옵션_밸런싱_최종_V2.csv  — 티어/옵션별 스탯 수치
# Input2: 능력치 점검 - 드랍 & 옵션 리스트 (1).csv  — 아이템-옵션 배정 (신규)
# Output: 방어구_옵션_밸런싱_최종_V3.csv  — 합쳐진 결과

import csv, re

OLD_CSV = r"C:\Users\hoy5343\Downloads\방어구_옵션_밸런싱_최종_V2.csv"
NEW_CSV = r"C:\Users\hoy5343\Downloads\능력치 점검 - 드랍 & 옵션 리스트 (3).csv"
OUT_CSV = r"C:\Users\hoy5343\Downloads\방어구_옵션_밸런싱_최종_V3.csv"


def extract_key(raw):
    """'DamageDownVaryper (받는 피해 감소)' → 'DamageDownVaryper'"""
    m = re.match(r"^(\S+)\s+\(", raw.strip())
    return m.group(1) if m else raw.strip()


def parse_options(raw):
    """패시브1 필드에서 (key, korean) 쌍 목록 추출.
    'DamageDownVaryper (받는 피해 감소)MaxHpVary (최대 생명력)'
    → [('DamageDownVaryper', '받는 피해 감소'), ('MaxHpVary', '최대 생명력')]
    """
    return re.findall(r"(\S+)\s+\(([^)]+)\)", raw.strip())


# 획득 방법 이름 정규화 (공백 있는 경우 처리)
ACQ_NORM = {"기본 제작": "기본제작"}


# ── Step 1: 기존 CSV에서 스탯 수치 룩업 빌드 ──────────────────────────────
# {(tier, stat_key): ["0강값", "1강값", ..., "5강값"]}
stat_vals = {}
with open(OLD_CSV, encoding="utf-8-sig") as f:
    for row in csv.DictReader(f):
        tier = row["티어"]
        key  = extract_key(row["옵션명"])
        lk   = (tier, key)
        if lk not in stat_vals:
            stat_vals[lk] = [row.get(f"{k}강", "") for k in range(6)]

print(f"  스탯 룩업: {len(stat_vals)}개 (tier, key) 쌍 로드")


# ── Step 2: 신규 옵션 리스트 CSV 파싱 ────────────────────────────────────
# 주의: CSV 헤더 레이블이 뒤바뀜
#   "티어" 컬럼 → 실제 획득 방법 (기본 제작, 던전코어 ...)
#   "획득" 컬럼 → 실제 티어 (1T, 2T, 3T)
new_rows = []
missing = []
item_group = 0

with open(NEW_CSV, encoding="utf-8-sig") as f:
    for row in csv.DictReader(f):
        item_group += 1
        raw_acq = row["티어"]
        acq  = ACQ_NORM.get(raw_acq, raw_acq)
        tier = row["획득"]
        mat  = row["재질"]
        part = row["파츠"]

        options = []
        for field in ["패시브1", "패시브2"]:
            val = row[field].strip()
            if val and val != "-":
                options.extend(parse_options(val))

        # 중복 키 집계: 같은 키가 2번 나오면 수치 2배
        from collections import Counter, OrderedDict
        key_count = Counter(k for k, _ in options)
        seen = set()
        deduped = []
        for key, kr in options:
            if key not in seen:
                deduped.append((key, kr, key_count[key]))
                seen.add(key)

        for key, kr, cnt in deduped:
            lk = (tier, key)
            if lk in stat_vals:
                raw = stat_vals[lk]
            else:
                print(f"  ⚠ 스탯 없음: {lk}")
                missing.append(lk)
                raw = [""] * 6

            # cnt > 1 이면 수치 배수 적용
            if cnt > 1:
                vals = [str(int(v) * cnt) if v.strip() else "" for v in raw]
                label = f"{key} ({kr}) ×{cnt}"
            else:
                vals = raw
                label = f"{key} ({kr})"

            new_rows.append({
                "티어":  tier,
                "획득":  acq,
                "재질":  mat,
                "파츠":  part,
                "옵션명": label,
                "그룹":  str(item_group),
                "0강": vals[0], "1강": vals[1], "2강": vals[2],
                "3강": vals[3], "4강": vals[4], "5강": vals[5],
            })


# ── Step 3: 결과 CSV 저장 ────────────────────────────────────────────────
cols = ["티어", "획득", "재질", "파츠", "옵션명", "그룹",
        "0강", "1강", "2강", "3강", "4강", "5강"]
with open(OUT_CSV, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    w.writerows(new_rows)

print(f"✅ {len(new_rows)}행 저장 → {OUT_CSV}")
if missing:
    print(f"⚠ 누락 스탯 키: {set(missing)}")
else:
    print("  누락 없음")
