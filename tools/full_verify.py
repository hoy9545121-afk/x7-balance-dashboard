"""
constants.py SKILLS 전체 vs Excel 3T 데이터 완전 비교
모든 무기 × 모든 스킬 × 모든 레벨의 cd/mp/dmg 비교
"""
import sys, openpyxl
sys.path.insert(0, r'C:\AI_simulator')
from simulator.constants import SKILLS

BASE = r'C:\AI_simulator\기획서'
FILEPATH = fr'{BASE}\X7_무기_스킬.xlsx'

# 무기별 3T 데이터 시작 행 (스킬 데이터 첫 행 = Q Lv.1)
WEAPON_START_ROWS = {
    '양손검': 77,
    '한손검': 77,
    '활':     83,
    '지팡이': 125,
    '단검':   77,
}

wb = openpyxl.load_workbook(FILEPATH, read_only=True, data_only=True)

errors = []
ok_count = 0

for wpn, start_row in WEAPON_START_ROWS.items():
    ws = wb[wpn]

    # constants에서 3T 스킬만 추출 (평타 제외)
    skills_3t = [s for s in SKILLS[wpn] if s['cmd'] in ['Q','W','E','R']]

    cur_row = start_row
    for skill in skills_3t:
        cmd = skill['cmd']
        for lv_data in skill['levels']:
            lv  = lv_data['lv']
            exp_cd  = lv_data['cd']
            exp_mp  = lv_data['mp']
            exp_dmg_pct = lv_data['dmg']          # e.g. 200
            exp_dmg_ratio = round(exp_dmg_pct / 100, 4)  # e.g. 2.0

            # Excel 열: B=cmd(2), C=lv(3), D=cd(4), E=mp(5), F=type(6), G=dmg배율(7)
            xl_cd  = ws.cell(cur_row, 4).value
            xl_mp  = ws.cell(cur_row, 5).value
            xl_dmg = ws.cell(cur_row, 7).value

            # dmg는 배율(소수) 또는 정수(%) 둘 다 허용
            if xl_dmg is not None:
                # 정수면 /100 변환
                xl_dmg_norm = round(float(xl_dmg), 4)
                if xl_dmg_norm > 10:  # 배율이 아닌 % 형식
                    xl_dmg_norm = round(xl_dmg_norm / 100, 4)
            else:
                xl_dmg_norm = None

            ok = True
            notes = []
            if xl_cd != exp_cd:
                notes.append(f"cd: xl={xl_cd} → exp={exp_cd}")
                ok = False
            if xl_mp != exp_mp:
                notes.append(f"mp: xl={xl_mp} → exp={exp_mp}")
                ok = False
            if xl_dmg_norm is not None and abs(xl_dmg_norm - exp_dmg_ratio) > 0.001:
                notes.append(f"dmg: xl={xl_dmg}({xl_dmg_norm}) → exp={exp_dmg_ratio}")
                ok = False

            if ok:
                ok_count += 1
            else:
                errors.append(f"[{wpn}] {cmd} Lv{lv} (R{cur_row}): {', '.join(notes)}")

            cur_row += 1

wb.close()

print(f"=== 검증 결과 ===")
print(f"✅ 일치: {ok_count}개")
if errors:
    print(f"❌ 불일치: {len(errors)}개")
    for e in errors:
        print(f"  {e}")
else:
    print("❌ 불일치: 0개 — 모두 정확합니다!")

# ─── 추가: 스킬 리스트 시트 스킬명 확인 ────────────────────────────────────
print("\n=== 스킬 리스트 시트 (3번 스킬셋) ===")
FILEPATH2 = fr'{BASE}\X7_무기_스킬.xlsx'
wb2 = openpyxl.load_workbook(FILEPATH2, read_only=True, data_only=True)
ws_list = wb2['스킬 리스트']
# constants 스킬명 목록
const_names = {}
for wpn in ['양손검','한손검','활','지팡이','단검']:
    for s in SKILLS[wpn]:
        if s['cmd'] in ['Q','W','E','R']:
            const_names[s['name']] = wpn

for row in ws_list.iter_rows(values_only=True):
    if row[1] and '3번 스킬셋' in str(row[1]):
        skill_name = row[4] if len(row) > 4 else None
        cmd = row[2] if len(row) > 2 else None
        status = row[5] if len(row) > 5 else None
        if skill_name:
            matched = skill_name in const_names
            mark = '✅' if matched else '❌'
            print(f"  {mark} {row[1]} / {cmd} / {skill_name} / {status}")

wb2.close()
