"""CSV 교차검증 수정: LootGroup + StatModified"""
import csv

BASE = r"C:\AI_simulator\게임 데이터 전체_원본.csv"

# 1. LootGroup.csv: 500001/500002 드랍률 2,000,000 → 833,000
path = BASE + r"\LootGroup.csv"
rows = []
with open(path, 'r', encoding='utf-8-sig') as f:
    rows = list(csv.reader(f))

changed = 0
for row in rows[1:]:
    if len(row) > 0 and row[0] in ('500001', '500002'):
        last = len(row) - 1
        if row[last] == '2000000':
            row[last] = '833000'
            print(f"  LootGroup {row[0]}: 2000000 → 833000")
            changed += 1

with open(path, 'w', encoding='utf-8-sig', newline='') as f:
    csv.writer(f).writerows(rows)
print(f"LootGroup.csv: {changed}개 수정 완료\n")

# 2. StatModified.csv: 고대/영웅 Comment 라벨 교정
path = BASE + r"\StatModified.csv"
rows = []
with open(path, 'r', encoding='utf-8-sig') as f:
    rows = list(csv.reader(f))

fixes = {
    '2104': '무기_고대 등급 능력치',
    '2105': '무기_영웅 등급 능력치',
    '2204': '방어구_고대 등급 능력치',
    '2205': '방어구_영웅 등급 능력치',
}

changed = 0
for row in rows[1:]:
    if len(row) > 0 and row[0] in fixes:
        old = row[2]
        row[2] = fixes[row[0]]
        print(f"  StatModified CID {row[0]}: \"{old}\" → \"{row[2]}\"")
        changed += 1

with open(path, 'w', encoding='utf-8-sig', newline='') as f:
    csv.writer(f).writerows(rows)
print(f"StatModified.csv: {changed}개 Comment 교정 완료")
