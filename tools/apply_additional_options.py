"""
추가옵션(AddVary) CSV 데이터 생성 스크립트
- StatModified.csv    : T2/T3 무기·방어구, T3 반지 옵션 수치 추가
- ItemAdditionalOption.csv : 티어별 옵션 그룹 추가
- ItemEquipment.csv   : T1방어구 / T2~T3 무기·방어구 / T3 장신구 AdditionalOpt 채우기

출력: 게임 데이터 전체_수정.csv/
원본: 게임 데이터 전체_원본.csv/ (변경 없음)
"""

import csv, os, math, shutil

SRC = r'C:\AI_simulator\게임 데이터 전체_원본.csv'
DST = r'C:\AI_simulator\게임 데이터 전체_수정.csv'
os.makedirs(DST, exist_ok=True)

def read_csv(fp):
    with open(fp, encoding='utf-8-sig', newline='') as f:
        return list(csv.reader(f))

def write_csv(fp, rows):
    with open(fp, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerows(rows)

# ── 옵션 값 계산 (FLOOR) ───────────────────────────────────────────────────
PCTS = [0.05, 0.06, 0.07, 0.08, 0.09, 0.10]
def opt_vals(base):
    return [math.floor(base * p) for p in PCTS]

# 확률 가중치: 10:10:10:20:20:30 (design spec)
PROBS = '[100,100,100,200,200,300]'

# ── StatModified 신규 항목 정의 ────────────────────────────────────────────
# CID 체계: 8[slot][tier]0[n]
#   slot: 0=무기ATK, 1=방어구DEF, 2=반지ATK
#   tier: 2=T2, 3=T3
# 기존 T1 무기: 80101~80106

NEW_STAT_MODIFIED = []

def add_sm_entries(cid_base, tier_label, slot_label, category, base_stat):
    vals = opt_vals(base_stat)
    entries = []
    for i, v in enumerate(vals, 1):
        cid = cid_base * 10 + i   # e.g. 8020*10+1 = 80201
        entries.append([
            str(cid), str(cid),
            f'{tier_label} {slot_label} 추가 옵션_{i:02d}',
            category,
            str(v)
        ])
    return entries

# 무기 AddAttackVary
NEW_STAT_MODIFIED += add_sm_entries(8020, 'T2', '무기',     'AttackVary',          80)   # 80201~80206
NEW_STAT_MODIFIED += add_sm_entries(8030, 'T3', '무기',     'AttackVary',         120)   # 80301~80306

# 방어구 AddPhysicalDefenseVary
NEW_STAT_MODIFIED += add_sm_entries(8110, 'T1', '방어구',   'PhysicalDefenseVary',  30)  # 81101~81106
NEW_STAT_MODIFIED += add_sm_entries(8120, 'T2', '방어구',   'PhysicalDefenseVary',  40)  # 81201~81206
NEW_STAT_MODIFIED += add_sm_entries(8130, 'T3', '방어구/목걸이/귀걸이', 'PhysicalDefenseVary', 60)  # 81301~81306

# 반지 AddAttackVary (T3)
NEW_STAT_MODIFIED += add_sm_entries(8230, 'T3', '반지',     'AttackVary',           30)  # 82301~82306

# ── ItemAdditionalOption 신규 항목 ─────────────────────────────────────────
def sm_cid_list(cid_base):
    return '[' + ','.join(str(cid_base*10+i) for i in range(1,7)) + ']'

NEW_IAO = [
    # OID, Cid, Milestone, Comment, StatModifiedCids, Probs
    ['1200', '1200', 'Dev', 'T2 무기 AddATK',            sm_cid_list(8020), PROBS],
    ['1300', '1300', 'Dev', 'T3 무기 AddATK',            sm_cid_list(8030), PROBS],
    ['1110', '1110', 'Dev', 'T1 방어구 AddDEF',          sm_cid_list(8110), PROBS],
    ['1120', '1120', 'Dev', 'T2 방어구 AddDEF',          sm_cid_list(8120), PROBS],
    ['1130', '1130', 'Dev', 'T3 방어구/목걸이/귀걸이 AddDEF', sm_cid_list(8130), PROBS],
    ['1330', '1330', 'Dev', 'T3 반지 AddATK',            sm_cid_list(8230), PROBS],
]

# ── ItemEquipment AdditionalOpt 매핑 ──────────────────────────────────────
# Cid prefix → ItemAdditionalOption Cid
IE_MAP = {
    # T1 무기: 이미 [1100] 으로 설정됨 (변경 안함)
    '1102': '[1200]',  # T2 무기 (전리품·던전코어)
    '1103': '[1300]',  # T3 무기 (전리품·던전코어·드랍)
    '1201': '[1110]',  # T1 방어구 (기본템)
    '1202': '[1120]',  # T2 방어구
    '1203': '[1130]',  # T3 방어구
    '1303': '[1330]',  # T3 반지 (CID 13030001)
    '1303_neck': '[1130]',   # T3 목걸이 (13030002) → 방어 옵션
    '1303_ear':  '[1130]',   # T3 귀걸이 (13030003) → 방어 옵션
}

# 장신구 CID별 매핑 (Category 기반)
ACCESSORY_MAP = {
    '13030001': ('[1330]', 'Ring'),
    '13030002': ('[1130]', 'Necklace'),
    '13030003': ('[1130]', 'Earring'),
}

# ═══════════════════════════════════════════════════════════════════════════
# 1. StatModified.csv 수정
# ═══════════════════════════════════════════════════════════════════════════
sm_rows = read_csv(os.path.join(SRC, 'StatModified.csv'))
sm_header = sm_rows[0]
sm_data   = sm_rows[1:]

# 기존 CID 중복 체크
existing_cids = {r[0] for r in sm_data}
added_sm = 0
for entry in NEW_STAT_MODIFIED:
    if entry[0] not in existing_cids:
        sm_data.append(entry)
        existing_cids.add(entry[0])
        added_sm += 1
    else:
        print(f'  [StatModified] CID {entry[0]} 이미 존재 → 스킵')

sm_out = [sm_header] + sm_data
write_csv(os.path.join(DST, 'StatModified.csv'), sm_out)
print(f'✅ StatModified.csv: {added_sm}개 추가 → {len(sm_data)}행')

# ═══════════════════════════════════════════════════════════════════════════
# 2. ItemAdditionalOption.csv 수정
# ═══════════════════════════════════════════════════════════════════════════
iao_rows = read_csv(os.path.join(SRC, 'ItemAdditionalOption.csv'))
iao_header = iao_rows[0]
iao_data   = iao_rows[1:]

existing_iao = {r[0] for r in iao_data}
added_iao = 0
for entry in NEW_IAO:
    if entry[0] not in existing_iao:
        iao_data.append(entry)
        existing_iao.add(entry[0])
        added_iao += 1
    else:
        print(f'  [IAO] CID {entry[0]} 이미 존재 → 스킵')

iao_out = [iao_header] + iao_data
write_csv(os.path.join(DST, 'ItemAdditionalOption.csv'), iao_out)
print(f'✅ ItemAdditionalOption.csv: {added_iao}개 추가 → {len(iao_data)}행')

# ═══════════════════════════════════════════════════════════════════════════
# 3. ItemEquipment.csv 수정
# ═══════════════════════════════════════════════════════════════════════════
ie_rows = read_csv(os.path.join(SRC, 'ItemEquipment.csv'))
ie_header = ie_rows[0]
ie_data   = [list(r) for r in ie_rows[1:]]

# 헤더 인덱스 확인
IDX_CID     = ie_header.index('Cid')
IDX_KIND    = ie_header.index('Kind')
IDX_CAT     = ie_header.index('EquipmentCategory')
IDX_ADDOPT  = ie_header.index('ItemAdditionalOptionCids')
IDX_CMT     = ie_header.index('Comment')

updated = 0
skipped_nonempty = 0

for row in ie_data:
    cid  = row[IDX_CID]
    kind = row[IDX_KIND]
    cat  = row[IDX_CAT]
    current = row[IDX_ADDOPT].strip()

    new_val = None

    if kind == 'Weapon':
        prefix4 = cid[:4]
        if prefix4 in ('1102', '1103'):
            new_val = IE_MAP[prefix4]
        # T1 무기 (1101): 이미 설정됨 → 건드리지 않음

    elif kind == 'Armor':
        prefix4 = cid[:4]
        if prefix4 in ('1201', '1202', '1203'):
            new_val = IE_MAP[prefix4]

    elif kind == 'Accessory':
        if cid in ACCESSORY_MAP:
            new_val = ACCESSORY_MAP[cid][0]

    if new_val is not None:
        if current == '':
            row[IDX_ADDOPT] = new_val
            updated += 1
        else:
            # 이미 값이 있는 경우 덮어쓰지 않음 (단, 기존값이 새값과 다르면 경고)
            if current != new_val:
                print(f'  ⚠️ Cid={cid} 기존값={current} 신규값={new_val} → 기존값 유지')
            skipped_nonempty += 1

ie_out = [ie_header] + ie_data
write_csv(os.path.join(DST, 'ItemEquipment.csv'), ie_out)
print(f'✅ ItemEquipment.csv: {updated}개 업데이트, {skipped_nonempty}개 기존값 유지')

# ═══════════════════════════════════════════════════════════════════════════
# 검증 출력
# ═══════════════════════════════════════════════════════════════════════════
print()
print('=== StatModified 신규 항목 목록 ===')
for e in NEW_STAT_MODIFIED:
    print(f'  {e[0]} | {e[2]:35s} | {e[3]:25s} | {e[4]}')

print()
print('=== ItemAdditionalOption 신규 항목 ===')
for e in NEW_IAO:
    print(f'  Cid={e[0]:5s} | {e[3]:30s} | StatCids={e[4]} | Probs={e[5]}')

print()
print('=== ItemEquipment 샘플 확인 (수정본) ===')
ie_verify = read_csv(os.path.join(DST, 'ItemEquipment.csv'))
check_cids = ['11020001','11030001','12010001','12020001','12030001','13030001','13030002','13030003']
for row in ie_verify[1:]:
    if row[IDX_CID] in check_cids:
        print(f'  Cid={row[IDX_CID]}, AdditionalOpt={row[IDX_ADDOPT]}, Comment={row[IDX_CMT][:30]}')

print()
print('완료! 저장 경로:', DST)
