"""
3T 스킬 데이터 집중 감사 (단검/지팡이 3T + 장비 능력치)
"""
import openpyxl

BASE = r'C:\AI_simulator\기획서'

def dump_rows(path, sheet, r_from, r_to):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb[sheet]
    print(f"\n--- {sheet} R{r_from}~R{r_to} ---")
    for r in range(r_from, r_to+1):
        vals = [ws.cell(row=r, column=c).value for c in range(2, 15)]
        if any(v is not None for v in vals):
            print(f"  R{r}: {vals}")
    wb.close()

SKILL = fr'{BASE}\X7_무기_스킬.xlsx'
EQUIP = fr'{BASE}\X7_장비_능력치_기획서.xlsx'

# 단검 3T 스킬 (R77~)
dump_rows(SKILL, '단검', 77, 120)

# 지팡이 3T 스킬
dump_rows(SKILL, '지팡이', 82, 140)

# 장비 능력치 시트들
print("\n\n=== X7_장비_능력치_기획서.xlsx ===")
for sheet in ['⚔ 무기 공격력', '🛡 방어구 방어력', '💍 악세사리', '📌 스탯 캡 & 공식']:
    dump_rows(EQUIP, sheet, 1, 60)

# 무기 비교 개요 시트
dump_rows(SKILL, '무기 비교 개요', 1, 50)
